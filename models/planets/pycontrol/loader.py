# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The planet landing model
#
# Loader for the program simulation
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
import os
import importlib
import traceback
import zmq

USE_RLIMIT = False
MEMORY_LIMIT = 256 * 1024 * 1024
USE_SECCOMP = True


THIS_MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
API_PATH = os.path.abspath(os.path.join(THIS_MODULE_PATH, '..', 'api'))
sys.path.append(API_PATH)

if USE_RLIMIT:
    try:
        import resource
    except ImportError:
        USE_RLIMIT = False

if USE_SECCOMP:
    try:
        import mmap
        import signal
        import seccomp
    except ImportError:
        USE_SECCOMP = False

def send_to_controller(data, timeout=None):
    global request_queue
    if request_queue is None:
        return False
    try:
        request_queue.send_pyobj(data)
    except zmq.ZMQError:
        return False
    return True

def receive_from_controller(timeout=None):
    global response_queue # pylint: disable=W0603

    if response_queue is None:
        return None
    try:
        data = response_queue.recv_pyobj()
    except zmq.ZMQError:

        return None
    return data

if __name__ == '__main__':

    if len(sys.argv) < 3:
        sys.exit(1)
        
    REQUEST_PORT = int(sys.argv[1])
    RECEIVE_PORT = int(sys.argv[2])

    request_context = zmq.Context()
    response_context = zmq.Context()

    request_queue = request_context.socket(zmq.PUSH)
    request_queue.bind(f"tcp://*:{REQUEST_PORT}")

    response_queue = request_context.socket(zmq.PULL)
    response_queue.connect(f"tcp://localhost:{RECEIVE_PORT}")

    user_code = sys.stdin.read()
    
    user_globals = {}

    if len(sys.argv) >= 4:
        api_module_name = sys.argv[3]

        api_module = importlib.import_module(api_module_name)

        user_globals = api_module.build_globals(send_to_controller,
                                                receive_from_controller)
 
    if USE_RLIMIT:
        soft_limit, hard_limit = resource.getrlimit(resource.RLIMIT_AS)
        if ((hard_limit == resource.RLIM_INFINITY) or (hard_limit > MEMORY_LIMIT)):
            resource.setrlimit(resource.RLIMIT_AS,
                               (MEMORY_LIMIT, MEMORY_LIMIT))
            
    if USE_SECCOMP:
        syscall_filter = seccomp.SyscallFilter(seccomp.KILL)

        # Allocating memort
        malloc_match = seccomp.Arg(3, seccomp.EQ,
                                   mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS)
        syscall_filter.add_rule_exactly(seccomp.ALLOW, "mmap",
                                        malloc_match)
        syscall_filter.add_rule_exactly(seccomp.ALLOW, "munmap")
        syscall_filter.add_rule_exactly(seccomp.ALLOW, "brk")

        # Signals handling
        sigint_match = seccomp.Arg(0, seccomp.EQ, signal.SIGINT)
        syscall_filter.add_rule_exactly(seccomp.ALLOW, "rt_sigaction",
                                        sigint_match)
        syscall_filter.add_rule_exactly(seccomp.ALLOW, "rt_sigreturn")

        # Standard I/O
        stdin_match = seccomp.Arg(0, seccomp.EQ, sys.stdin.fileno())
        stdout_match = seccomp.Arg(0, seccomp.EQ, sys.stdout.fileno())
        stderr_match = seccomp.Arg(0, seccomp.EQ, sys.stderr.fileno())
        syscall_filter.add_rule_exactly(seccomp.ALLOW, "read",
                                        stdin_match)
        syscall_filter.add_rule_exactly(seccomp.ALLOW, "write",
                                        stdout_match)
        syscall_filter.add_rule_exactly(seccomp.ALLOW, "write",
                                        stderr_match)
        syscall_filter.add_rule_exactly(seccomp.ALLOW, "fstat",
                                        stdin_match)
        syscall_filter.add_rule_exactly(seccomp.ALLOW, "fstat",
                                        stdout_match)
        syscall_filter.add_rule_exactly(seccomp.ALLOW, "fstat",
                                        stderr_match)

        # Data exchange
        request_match = seccomp.Arg(0, seccomp.EQ, request_queue.mqd)
        response_match = seccomp.Arg(0, seccomp.EQ, response_queue.mqd)
        syscall_filter.add_rule_exactly(seccomp.ALLOW, "mq_timedsend",
                                        request_match)
        syscall_filter.add_rule_exactly(seccomp.ALLOW, "mq_timedreceive",
                                        response_match)

        # Closing descriptors
        syscall_filter.add_rule_exactly(seccomp.ALLOW, "close")

        # Exiting program
        syscall_filter.add_rule_exactly(seccomp.ALLOW, "exit_group")

        syscall_filter.load()

    send_to_controller('READY')

    status = 0

    try:
        exec(user_code, user_globals) # pylint: disable=W0122
    except Exception: #pylint: disable=W0703
        status = 1
        
        exc_type, exc_value, exc_tb = sys.exc_info()

        first_tb = exc_tb.tb_next
        current_tb = first_tb
        limit = 0

        while current_tb is not None:
            frame = current_tb.tb_frame

            file_name = frame.f_code.co_filename

            if file_name != '<string>':
                break

            limit += 1

            current_tb = current_tb.tb_next

        traceback.print_exception(exc_type, exc_value, first_tb, limit)
        
    request_queue.close()
    response_queue.close()

    sys.exit(status)
