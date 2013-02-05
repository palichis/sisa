##############################################################################
#
#    arduino module
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
#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
import pyfirmata
import time
#import rasplcd
from api.models import *

class board():
    estado = False
    board = False
    tablero_pind = {}
    tablero_pina = {}
    close = False
    analog = {}
    tablero_db = tablero.objects.all()
    #pin_obj = pin_placa.objects.all()
    def __init__(self):
        try:
            for ard in self.tablero_db:
                pin = {}
                pintemp = {}
                print "conexion con placa %s"%ard.descripcion
                if ard.placa.nombre == 'arduino':
                    self.board = pyfirmata.Arduino(ard.puerto.nombre)
                else:
                    self.board = pyfirmata.ArduinoMega(ard.puerto.nombre)
                it = pyfirmata.util.Iterator(self.board)
                it.start()
                print "establecida"
                pin_db = pin_placa.objects.filter(tablero=ard.id)
                for pin_obj in pin_db:
                    if pin_obj.tipo == "digital":
                        pin[pin_obj.pin] = self.board.get_pin("d:%s:%s"%(str(pin_obj.pin),str(pin_obj.modo[0])))
                        if str(pin_obj.modo[0]) == 'o':
                            pin[pin_obj.pin].write(False)
                    else:
                        pintemp[pin_obj.pin] = self.board.get_pin('a:%s:i'%pin_obj.pin)
                        print "temperature calculate %s"%pin_obj.pin
                self.tablero_pind[ard.tablero] = pin
                self.tablero_pina[ard.tablero] = pintemp
                #print self.tablero_pina
                #print self.tablero_pind
                temperatura = threading.Thread(target=self.temperatura)
                temperatura.start()
                hlectura = threading.Thread(target=self.lectura)
                hlectura.start()
                #temperatura = threading.Thread(target=self.temperatura)
                #temperatura.start()
        except pyfirmata.util.serial.SerialException:
            print "bad"
                #return False

    def temperatura(self):
        import pdb
        pin_read_db = pin_placa.objects.filter(modo='input', tipo='analogo')
        while True:
            for pin_read in pin_read_db:
            #self.temp1[pinnumero] = pintemp.read()
                temp = self.tablero_pina[pin_read.tablero.id][pin_read.pin].read()
                if not temp:
                    temp = 0.0
                self.analog[pin_read.pin] = 100.0 * float(temp) * 5.00
            time.sleep(2.0)
        
#   def lectura(self):
#        value_tablero = {}
#        newvalue_tablero = {}
#        tablero_db = tablero.objects.all()
#        for tablero_obj in tablero_db:
#            pins = {}
#            pin_read = pin_placa.objects.filter(modo='input', tipo='digital', tablero=tablero_obj.id)
#            print pin_read
#            for npi in pin_read:
#                #szpin = sub_zona.objects.filter(pin_entrada=npi.id)[0]
#                print npi
#                pin_combinacion_ob = combinacion_pin.objects.filter(pin_entrada=npi.id)
#                if pin_combinacion_ob:
#                    pin_combinacion_ob = pin_combinacion_ob[0]
#                    pins[npi.pin] = pin_combinacion_ob.pin_salida.pin
#            value_tablero[tablero_obj.id] = pins
#            print value_tablero
#            for es in pins:
#                #if self.pin[es].read():
#                value[es] = self.pin[es].read()	
#        while True:
#            for es in pins:
#                newvalue[es] = self.pin[es].read()
#                if value[es] != newvalue[es]:
#                    if newvalue[es] > 0.5:
#                        self.pin[pins[es]].write(not self.pin[pins[es]].value)
#                value[es] = newvalue[es]
#            time.sleep(0.01)
            
    def lectura(self):
        value = {}
        newvalue = {}
        combinacionpin_db = combinacion_pin.objects.all()
        for combinacion_obj in combinacionpin_db:
            if combinacion_obj.pin_entrada and combinacion_obj.pin_salida:
                print "id value %s, tablero %s, pin %s"%(combinacion_obj.id, combinacion_obj.pin_entrada.tablero.id,combinacion_obj.pin_entrada.pin)
                value[combinacion_obj.id] = self.tablero_pind[combinacion_obj.pin_entrada.tablero.id][combinacion_obj.pin_entrada.pin].read()
        while True:
            for combinacion_obj in combinacionpin_db:
                if combinacion_obj.pin_entrada and combinacion_obj.pin_salida:
                    newvalue[combinacion_obj.id] = self.tablero_pind[combinacion_obj.pin_entrada.tablero.id][combinacion_obj.pin_entrada.pin].read()
                    if newvalue[combinacion_obj.id] != value[combinacion_obj.id]:
                        if newvalue[combinacion_obj.id] > 0.5:
                            self.tablero_pind[combinacion_obj.pin_salida.tablero.id][combinacion_obj.pin_salida.pin].write(not self.tablero_pind[combinacion_obj.pin_salida.tablero.id][combinacion_obj.pin_salida.pin].value)
                    value[combinacion_obj.id] = newvalue[combinacion_obj.id]
            time.sleep(0.01)
                
    def close(self):
        self.board.exit()
