# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator RESTful API
#
# The server API implementation
# Copyright (C) 2024 Alexey Fedoseev <aleksey@fedoseev.net>
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

import time
import os
import configparser
import re
import simplejson as json

PARAMETERS_FILE = 'parameters-ru.xml'
DEVICES_FILE = 'devices-ru.xml'
TASK_EXTENSION = '.xml'

class OrbitaNotFoundException(Exception):
    pass
class OrbitaBadRequestException(Exception):
    pass

class OrbitaServerAPI:
    def __init__(self, configfile, tmpdir, resurl, imgurl):
        cfg = configparser.ConfigParser()
        cfg.read(configfile)

        self.server_version = cfg.get('status', 'version')
        self.indir = cfg.get('general', 'incoming')
        self.workdir = cfg.get('general', 'working')
        self.imgdir = cfg.get('general', 'images')
        self.outdir = cfg.get('general', 'result')
        self.modelsdir = cfg.get('simulation', 'models')
        self.calcmodels = cfg.get('simulation', 'calc_models').split(' ')

        self.outurl = resurl
        self.imgurl = imgurl
        
        self.encoder = json.encoder.JSONEncoder()

        self.temp_dir = tmpdir
        self.start_id = int(time.time() * 1e6)
        self.re_id = re.compile(r'\d+')
        
    def server(self):

        result = {
            'version': self.server_version,
            'models': self.calcmodels,
            'tasks': self.__calculate_tasks()
        }

        return self.encoder.encode(result)

    def parameters(self, model):
        self.__check_model(model)

        f = open(os.path.join(self.modelsdir, model, PARAMETERS_FILE))
        data = f.read()
        f.close()

        return data
    
    def devices(self, model):
        self.__check_model(model)

        f = open(os.path.join(self.modelsdir, model, DEVICES_FILE))
        data = f.read()
        f.close()

        return data
        
    def calculation(self, model, xml):
        self.__check_model(model)
        if len(xml) == 0:
            raise OrbitaBadRequestException()

        task_id = self.__generate_id()
        temp_file = self.__write_temp_file(task_id, xml)
        os.rename(os.path.join(self.temp_dir, temp_file),
                  os.path.join(self.indir, model, temp_file))

        result = {
            'id': task_id
        }

        return self.encoder.encode(result)

    def status(self, model, task_id):
        self.__check_model(model)
        self.__check_id(task_id)

        if os.path.isfile(os.path.join(self.workdir, model, task_id + TASK_EXTENSION)):
            if os.path.isfile(os.path.join(self.outdir, model, task_id + '-short.xml')):
                status = 'completed'
            else:
                status = 'working'
        else:
            status = 'not found'

        result = {
            'status': status
        }

        return self.encoder.encode(result)

    def result(self, model, task_id):
        self.__check_model(model)
        self.__check_id(task_id)

        shortxml = os.path.join(self.outdir, model, task_id + '-short.xml')
        if not os.path.isfile(shortxml):
            raise OrbitaNotFoundException()
        shortxml = shortxml.replace(self.outdir, self.outurl)
        logfile = os.path.join(self.outdir, model, task_id + '-result.log')
        if os.path.isfile(logfile):
            logfile = logfile.replace(self.outdir, self.outurl)
        else:
            logfile = None
        images = []
        imgdir = os.path.join(self.imgdir, model)
        for imgfile in os.listdir(imgdir):
            if imgfile.find(task_id) == 0:
                imgpath = os.path.join(imgdir, imgfile)
                if os.path.isfile(imgpath):
                    images.append(imgpath.replace(self.imgdir, self.imgurl))

        result = {
            'xml': shortxml,
            'images': images
        }
        if logfile:
            result['log'] = logfile

        return result

    def __generate_id(self):
        result = self.start_id
        self.start_id += 1
        return str(result)

    def __write_temp_file(self, task_id, task_data):
        filename = task_id + TASK_EXTENSION
        filepath = os.path.join(self.temp_dir, filename)
        f = open(filepath, 'w')
        f.truncate()
        f.write(task_data)
        f.close()
        return filename

    def __calculate_tasks(self):
        result = 0
        for m in self.calcmodels:
            d = self.workdir + '/' + m
            files = os.listdir(d)
            for f in files:
                filename = os.path.join(d, f)
                if os.path.isfile(filename) and filename.find(TASK_EXTENSION) > 0:
                    result += 1
        return result

    def __check_model(self, model):
        if model not in self.calcmodels:
            raise OrbitaNotFoundException()

    def __check_id(self, num):
        if re.match(self.re_id, num) is None:
            raise OrbitaBadRequestException()
