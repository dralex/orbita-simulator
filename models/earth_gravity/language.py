# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# The language module
#
# Copyright (C) 2023 Alexey Fedoseev <aleksey@fedoseev.net>
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

import os
import gettext

DEFAULT_LANGUAGE = 'en'
LANGUAGE_ORIGIN = 'sputnik'

class Language:

    Lang = DEFAULT_LANGUAGE
    __tr = gettext.gettext

    @classmethod
    def set_lang(cls, lang):
        if lang != DEFAULT_LANGUAGE:
            cls.Lang = lang
            t = gettext.translation(LANGUAGE_ORIGIN,
                                    os.path.dirname(os.path.abspath(__file__)),
                                    languages=[lang])
            cls.__tr = t.gettext
            t.install()

    @classmethod
    def get_tr(cls):
        return cls.__tr
