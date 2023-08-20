# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The planet landing model
#
# Program simulation worker
#
# Copyright (C) 2013-2023 Alexey Fedoseev <aleksey@fedoseev.net>
# Copyright (C) 2016-2023 Ilya Tagunov <tagunil@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see https://www.gnu.org/licenses/
# -----------------------------------------------------------------------------

import sys
import time
import os
import subprocess
import threading
import atexit
from collections import deque
import gettext
import zmq

_ = gettext.gettext

THIS_MODULE_PATH = os.path.dirname(os.path.abspath(__file__))

WORKER_LAUNCH_COMMAND = [sys.executable,
                         '-B',
                         os.path.join(THIS_MODULE_PATH,
                                      'loader.py')]

WORKER_LAUNCH_TIMEOUT = 5.0

DEFAULT_PARAMS_MAX_LINES = 1000
DEFAULT_PARAMS_MAX_INIT_TIME = 1.0
DEFAULT_PARAMS_MAX_STEP_TIME = 0.1

STDOUT_BUFFER_LINES = 4096
STDERR_BUFFER_LINES = 64
MAX_LINE_LENGTH = 256

RECEIVE_PORT = 5454
REQUEST_PORT = 4545

def buffer_to_message(buf):
    msg = ''
    for b in buf:
        msg += b.decode('utf-8')
    return msg

class ControlError(Exception):
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg = msg

    def __str__(self):
        return self.msg

class WorkerError(ControlError):
    def __init__(self, msg):
        ControlError.__init__(self, msg)

class SecurityError(ControlError):
    def __init__(self, msg):
        ControlError.__init__(self, msg)

class FinishError(ControlError):
    def __init__(self, msg):
        ControlError.__init__(self, msg)

class ProgramError(ControlError):
    def __init__(self, msg, dump):
        ControlError.__init__(self, msg)
        self.dump = dump


class Program:
    def __init__(self,
                 runtime,
                 api_module_name,
                 code_lines,
                 lang,
                 params_max_lines=DEFAULT_PARAMS_MAX_LINES,
                 params_max_init_time=DEFAULT_PARAMS_MAX_INIT_TIME,
                 params_max_step_time=DEFAULT_PARAMS_MAX_STEP_TIME):
        global _ # pylint: disable=W0603
        _ = lang.get_tr()

        if len(code_lines) > params_max_lines:
            raise SecurityError(_('Program was not run because contains more than {} lines').format(params_max_lines)) # pylint: disable=C0301

        self._runtime = runtime
        self._api_module_name = api_module_name
        self._code = '\n'.join(code_lines)

        self._max_init_time = params_max_init_time
        self._max_step_time = params_max_step_time

        self._worker = None
        self._first_step = True
        self._deferred_response = None

        self._stdout_buffer = deque([], STDOUT_BUFFER_LINES)
        self._stderr_buffer = deque([], STDERR_BUFFER_LINES)

        self._stdout_reader = None
        self._stderr_reader = None

        self._request_queue = None
        self._response_queue = None

        atexit.register(self._destroy_worker)

        self.reset()

    def __del__(self):
        self._destroy_worker()

    def _destroy_worker(self):
        if self._worker is not None:
            if self._worker.poll() is None:
                self._worker.terminate()
                self._worker.wait()

            self._worker = None

        if self._stdout_reader is not None:
            self._stdout_reader.join()
            self._stdout_reader = None

        if self._stderr_reader is not None:
            self._stderr_reader.join()
            self._stderr_reader = None

        if self._request_queue is not None:
            self._request_queue.close()
            self._request_queue = None

        if self._response_queue is not None:
            self._response_queue.close()
            self._response_queue = None

    def reset(self):
        self._destroy_worker()

        self._request_context = zmq.Context()
        self._response_context = zmq.Context()

        

        self._response_queue = self._request_context.socket(zmq.PUSH)
        self._response_queue.bind(f"tcp://*:{RECEIVE_PORT}")

        self._request_queue = self._request_context.socket(zmq.PULL)
        self._request_queue.connect(f"tcp://localhost:{REQUEST_PORT}")

        self._first_step = True
        self._deferred_response = None

        command = (WORKER_LAUNCH_COMMAND +
                   [str(REQUEST_PORT),
                    str(RECEIVE_PORT)])
        
        
        if self._api_module_name is not None:
            command += [self._api_module_name]
        
        self._worker = subprocess.Popen(command,
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        
        def reader_task(pipe, queue_):
            while True:
                line = pipe.readline(MAX_LINE_LENGTH)
                if len(line) == 0:
                    break

                queue_.append(line)

        self._stdout_reader = threading.Thread(target=reader_task,
                                               args=(self._worker.stdout,
                                                     self._stdout_buffer))
        self._stderr_reader = threading.Thread(target=reader_task,
                                               args=(self._worker.stderr,
                                                     self._stderr_buffer))
        
        self._stdout_reader.daemon = True
        self._stderr_reader.daemon = True
        
        self._stdout_reader.start()
        self._stderr_reader.start()
        
        self._worker.stdin.write(self._code.encode('utf-8'))
        self._worker.stdin.close()
        
        time.sleep(3)


        if self._receive_from_worker(WORKER_LAUNCH_TIMEOUT) != b'READY':
            self._destroy_worker()
            raise WorkerError('Child worker does not respond')

                
            

    def _send_to_worker(self, data, timeout):
        try:
            self._response_queue.send_pyobj(data)
        except zmq.ZMQError:
            return False

        return True

    def _receive_from_worker(self, timeout):
        try:
            data = self._request_queue.recv_pyobj()
        except zmq.ZMQError:
            return None
        return data

    def run(self):
        if self._worker is not None:
            # TODO: implement monotone time
            previous_time = time.time()
            if self._first_step:
                remaining_time = self._max_init_time
            else:
                remaining_time = self._max_step_time

            next_step = False

            if not self._first_step:
                self._send_to_worker(self._deferred_response, remaining_time)

                current_time = time.time()
                remaining_time -= current_time - previous_time
                previous_time = current_time

                self._deferred_response = None

            while remaining_time >= 0:
                request = self._receive_from_worker(remaining_time)
               
                if request is None:
                    break

                current_time = time.time()
                remaining_time -= current_time - previous_time
                previous_time = current_time

                if self._runtime is not None:
                    response, next_step = self._runtime.process_call(request)

                else:
                    response = ''
                    next_step = True

                if next_step:
                    if self._first_step:
                        next_step = False
                        self._first_step = False

                        previous_time = time.time()
                        remaining_time = self._max_step_time

                if next_step:
                    self._deferred_response = response
                    break

                success = self._send_to_worker(response, remaining_time)
              
                if not success:
                    break

                current_time = time.time()
                remaining_time -= current_time - previous_time
                previous_time = current_time

            if not next_step:
                ret_code = self._worker.poll()
                self._destroy_worker()
                if ret_code is not None:
                    if ret_code < 0:
                        raise SecurityError(_('The program was terminated due to unacceptable operation')) # pylint: disable=C0301
                    if ret_code > 0:
                        raise ProgramError(_('The program finished unexpectedly\nError:'),
                                           buffer_to_message(self._stderr_buffer))
                    raise FinishError(_('The program finished'))
                if self._first_step:
                    time_without_answer = self._max_init_time
                else:
                    time_without_answer = self._max_step_time
                raise SecurityError(_('The program was terminated because did not respond for {:01} sec').format(time_without_answer)) # pylint: disable=C0301

    def print_stdout(self):
        print(_('\nStdout buffer:\n'))
        print(buffer_to_message(self._stdout_buffer))

    def print_stderr(self):
        print(_('\nStderr buffer:\n'))
        print(buffer_to_message(self._stderr_buffer))

if __name__ == '__main__':

    if len(sys.argv) < 2:
        sys.exit(1)

    filename = sys.argv[1]
    lines = open(filename).readline()
    p = Program(None, None, lines)

    try:
        p.run()
    except WorkerError as e:
        print(str(e))
    except SecurityError as e:
        print(str(e))
    except FinishError as e:
        print(str(e))
    except ProgramError as e:
        print(str(e))
        print(e.dump)
    except ControlError as e:
        print(str(e))

    p.print_stdout()
    p.print_stderr()
