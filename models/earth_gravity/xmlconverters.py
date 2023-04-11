# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# XML data file parsers and generators
#
# Copyright (C) 2015-2023 Alexey Fedoseev <aleksey@fedoseev.net>
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

from xml.sax.saxutils import escape

import pyxb
import venus.global_parameters
import venus.shortlog

from errors import CriticalError
from language import Language

_ = Language.get_tr()

def read_xml_file(f):
    return open(f).read()

xml_escape_table = {'"': "&quot;", "'": "&apos;"}

def xml_escape(text):
    return escape(text, xml_escape_table)

class XMLLoader:

    ORIGIN = None
    XML_FILE = None

    @classmethod
    def load(cls, lang, xml_file=None):
        try:
            _ = lang.get_tr()
            if xml_file is None:
                xml_file = cls.XML_FILE
            xmldata = read_xml_file(xml_file)
        except IOError:
            raise CriticalError(_("XML Error. Cannot load %s: cannot open file %s") %
                                (cls.ORIGIN, xml_file))
        try:
            return cls.decode(xmldata)
        except pyxb.BadDocumentError as e:
            raise CriticalError(_("XML Error. Cannot load %s: bad xml-document %s: %s") %
                                (cls.ORIGIN, xml_file, str(e)))
        except pyxb.ValidationError as e:
            raise CriticalError(_("XML Error. Cannot load %s: bad xml-документ %s: error in %s") %
                                (cls.ORIGIN, xml_file, str(e.location)))
        except pyxb.PyXBException:
            raise CriticalError(_("XML Error. Cannot load %s: bad xml document %s") %
                                (cls.ORIGIN, xml_file))

    @classmethod
    def decode(cls, xmldata): # pylint: disable=W0613
        return None

class GlobalParameters(XMLLoader):

    ORIGIN = _('parameters')
    XML_FILE = "parameters.xml"

    def __init__(self):
        self.Planets = {}
        self.G = None
        self.Orbasic = None

    @classmethod
    def decode(cls, xmldata):
        xml = venus.global_parameters.CreateFromDocument(xmldata)
        params = GlobalParameters()
        params.G = xml.G
        params.Orbasic = xml.orbasic
        for p in xml.planets.planet:
            if p.name in params.Planets:
                raise CriticalError(_("XML Error. Cannot load %s: there are two planets with the same name %s") % # pylint: disable=C0301
                                    (cls.ORIGIN, p.name))
            p.Models = {}
            for m in p.models.model:
                p.Models[m.order] = (m.kind, m.modelclass)
            p.Models = [p.Models[order] for order in sorted(p.Models.keys())]
            params.Planets[p.name] = p
            p.Atmosphere = None
        return params

    def debug_parameters(self, planet, logger):
        logger(_('Global Parameters:'))
        logger(_('\tG: %.4e kg m^3 / sec^2'), self.G)
        p = self.Planets[planet]
        logger(_('\tPlanet: %s'), planet)
        logger(_('\t\tRadius: %.4f км,'), p.radius / 1000.0)
        logger(_('\t\tMass: %.4e кг'), p.mass)
        logger(_('\tConstruction limits:'))
        logger(_('\t\tMax mass: %.2f кг'), p.probe.max_mass)
