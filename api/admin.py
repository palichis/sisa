##############################################################################
#
#    
#    Copyright (C) 2013 Katarisoft  All Rights Reserved
#    palichis@katarisoft.com
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from django.contrib import admin
from api.models import *

admin.site.register(placa)
admin.site.register(pin_placa)
admin.site.register(puerto)
admin.site.register(tablero)
admin.site.register(combinacion_pin)
