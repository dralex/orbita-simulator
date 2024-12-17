#!/usr/bin/python3
# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
#
# The computing server
#
# Copyright (C) 2013      Nikolay Safronov <bfishh@gmail.com>
# Copyright (C) 2013-2024 Alexey Fedoseev <aleksey@fedoseev.net>
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
import os.path
from os.path import join
import datetime
import errno
import traceback
import random
from time import sleep
import configparser
import importlib
import simplejson as json

TASK_EXTENSION = '.xml'

def server_log(msg):
    if the_logfile:
        data = '%s [%d] %s\n' % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                 os.getpid(),
                                 msg)
        f = open(the_logfile, 'a')
        f.write(data)
        f.close()

def modification_date(filename):
    try:
        t = os.path.getmtime(filename)
    except OSError as e:
        server_log('Cannot get time for {} {} {}'.format(filename,
                                                         errno.errorcode[e.errno],
                                                         e.strerror))
        return datetime.datetime.now()
    return datetime.datetime.fromtimestamp(t)

def get_oldest_file(checkdir):
    files = os.listdir(checkdir)
    oldesttime = datetime.datetime.now()
    oldestfile = None

    for f in files:
        filename = join(checkdir, f)
        if os.path.isfile(filename) and filename.find(TASK_EXTENSION) > 0:
            filetime = modification_date(filename)
            if filetime < oldesttime:
                oldesttime = filetime
                oldestfile = f
    return oldestfile

def get_random_file(checkdir):
    files = os.listdir(checkdir)
    if len(files) == 0:
        return None
    f = random.choice(files)
    return f

def load_model(mdir, modelname):
    if not os.path.isdir(mdir):
        return {}
    ms = None
    mdirname = os.path.basename(mdir)
    models = os.listdir(mdir)
    if modelname not in models:
        server_log('error: cannot find model {}'.format(modelname))
    else:
        modelpath = join(mdir, modelname)
        if os.path.isdir(modelpath):
            model = importlib.import_module('{}.{}'.format(mdirname, modelname))
            if '__all__' in dir(model) and 'simulation' in model.__all__:
                sys.path.append(os.path.abspath(modelpath))
                pkgname = '{}.{}'.format(mdirname, modelname)
                ms = importlib.import_module('{}.simulation'.format(pkgname),
                                             pkgname)
            else:
                server_log('error: model {} has no simulation package'.format(modelname))
        else:
            server_log('error: cannol load model {}'.format(modelname))
    return ms

def take_file(f, fromdir, todir):
    try:
        os.rename(join(fromdir, f), join(todir, f))
    except OSError as e:
        server_log('Cannot process file: {} {} {}'.format(f,
                                                          errno.errorcode[e.errno],
                                                          e.strerror))
    return True

def take_add_files(name, fromdir, todir):
    try:
        additional_files = name + '.'
        for f in os.listdir(fromdir):
            if f.find(additional_files) == 0:
                os.rename(join(fromdir, f), join(todir, f))
    except OSError as e:
        server_log('Cannot process additional file: {} {} {}'.format(f,
                                                                     errno.errorcode[e.errno],
                                                                     e.strerror))
    return True

def write_shortfile_error(shortfile, msg):
    f = open(shortfile, 'w')
    f.truncate()
    f.write('<?xml version="1.0" encoding="utf-8"?>\n')
    f.write('<o:shortlog xmlns:o="orbita">\n')
    f.write('<status>error</status>\n')
    f.write('<result_message>{} (see server.log)</result_message>\n'.format(msg))
    f.write('</o:shortlog>\n')
    f.close()

def process_file(filename, modelname, model, idir, wdir, odir, imdir, language, debuglog):
    server_log('process file: {}'.format(filename))
    if not take_file(filename, idir, wdir):
        return -1
    task = filename.split('.')[0]
    server_log('process task {} with model {}'.format(task, modelname))
    take_add_files(task, idir, wdir)

    taskfile = join(wdir, filename)
    if debuglog:
        debugfile = join(odir, task + '-debug.log')
    else:
        debugfile = None
    logfile = join(odir, task + '-result.log')
    shortfile = join(wdir, task + '-short.xml')
    htmlfile = join(odir, task + '-full.html')
    imdir = imdir + '/'

    pid = os.fork()
    if pid == 0:
        try:
            model.run(task, taskfile, logfile, debugfile,
                      shortfile, imdir, htmlfile, language)
        except Exception as ex: # pylint: disable=W0703
            template = "general exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            server_log(message)
            server_log(traceback.format_exc())
            if shortfile:
                write_shortfile_error(shortfile, 'Critical error while starting model')
        try:
            if os.path.isfile(shortfile):
                os.rename(shortfile, join(odir, task + "-short.xml"))
        except Exception as ex: # pylint: disable=W0703
            template = 'general exception of type {0}: arguments:\n{1!r}'
            message = template.format(type(ex).__name__, ex.args)
            server_log(message)
            server_log(traceback.format_exc())
            sys.exit(1)
        sys.exit(0)
    else:
        server_log('starting child %d' % pid)
        return pid

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('usage: {} <config-file>'.format(sys.argv[0]))
        sys.exit(1)

    cfg = configparser.ConfigParser()
    cfg.read(sys.argv[1])

    if cfg.has_option('status', 'version'):
        version = cfg.get('status', 'version')
    else:
        print('server config has no server version\n')
        sys.exit(1)
    
    if cfg.has_option('status', 'logfile'):
        the_logfile = cfg.get('status', 'logfile')
    else:
        the_logfile = None
        
    indir = cfg.get('general', 'incoming')
    workdir = cfg.get('general', 'working')
    imgdir = cfg.get('general', 'images')
    outdir = cfg.get('general', 'result')

    max_process_num = int(cfg.get('general', 'max_processes'))
    lang = cfg.get('general', 'language')
    debug = cfg.get('general', 'debug').lower() in ('on', 'true', 'yes', '1')

    modelsdir = cfg.get('simulation', 'models')
    calcmodels = cfg.get('simulation', 'calc_models').split(' ')

    server_log("========= Orbita server started =========")
    server_log('version: {}'.format(version))
    server_log('in dir: {}'.format(indir))
    server_log('work dir: {}'.format(workdir))
    server_log('out dir: {}'.format(outdir))
    server_log('img dir: {}'.format(imgdir))
    server_log('')
    server_log('max process num: {}'.format(max_process_num))
    server_log('language: {}'.format(lang))
    server_log('debugging: {}'.format(debug))
    server_log('')
    server_log('models dir: {}'.format(modelsdir))
    server_log('models: {}'.format(calcmodels))

    sleep(random.random() + 0.1)

    models = {}
    child_procs = []

    try:
        model_dirs = {}
        for model in calcmodels:
            modelsim = load_model(modelsdir, model)
            if modelsim is None:
                server_log('no model {} available'.format(model))
                raise Exception('No model error')
            server_log('loaded model: {}'.format(model))
            models[model] = modelsim
            model_dirs[model] = {'indir': os.path.join(indir, model),
                                 'workdir': os.path.join(workdir, model),
                                 'outdir': os.path.join(outdir, model),
                                 'imgdir': os.path.join(imgdir, model)}
            for d in model_dirs[model].values():
                if not os.path.isdir(d):
                    os.mkdir(d)
                    server_log('model directory {} created'.format(d))
        
        while True:
            the_file = None
            the_model = None
            if len(child_procs) <= max_process_num:
                start_index = random.randint(0, len(calcmodels) - 1)
                for i in range(len(calcmodels)):
                    index = (start_index + i) % len(calcmodels) 
                    the_model = calcmodels[index]
                    the_file = get_oldest_file(model_dirs[the_model]['indir'])
                    if the_file is not None:
                        break
                if the_file is not None:
                    modelsim = models[the_model]
                    dirs = model_dirs[the_model]
                    chpid = process_file(the_file, the_model, modelsim,
                                         dirs['indir'], dirs['workdir'], dirs['outdir'], dirs['imgdir'],
                                         lang, debug)
                    if chpid > 0:
                        child_procs.append(chpid)
                    continue
            finished = False
            for p in child_procs:
                r = os.waitpid(p, os.WNOHANG)
                if r != (0, 0):
                    assert r[0] == p
                    server_log('finishing child process %d' % p)
                    child_procs.remove(p)
                    finished = True
            if not finished:
                sleep(0.1)

    except Exception as global_exc: # pylint: disable=W0703
        m = "general exception of type {0}: arguments:\n{1!r}".format(type(global_exc).__name__,
                                                                      global_exc.args)
        server_log(m)
        server_log(traceback.format_exc())

    for p in child_procs:
        os.waitpid(p, 0)
        server_log('finishing child process %d' % p)
        
    server_log("========= Orbita server finished =========")
