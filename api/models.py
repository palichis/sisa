##############################################################################
#
#    Models module
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
from django.db import models

#Modelo del sistema

serie_placa = (
            ('arduino','UNO'),
            ('arduino_mega','MEGA'),
            )

class placa(models.Model):
    nombre = models.CharField(max_length=20, choices=serie_placa)
    pin_digital = models.SmallIntegerField()
    pin_pwm = models.SmallIntegerField()
    pin_analogico = models.SmallIntegerField()
    def __unicode__(self):
        return self.nombre  
    
class puerto(models.Model):
    nombre = models.CharField(max_length=20)
    def __unicode__(self): 
        return self.nombre

class tablero(models.Model):
    placa = models.ForeignKey(placa)
    puerto = models.ForeignKey(puerto, unique=True)
    tablero = models.IntegerField(unique=True)
    descripcion = models.CharField(max_length=30)
    def __unicode__(self):
        return u'%s %s %s'%(self.tablero,self.placa,self.puerto)

pin_modo = (
            ('output','Salida'),
            ('input','Entrada'),
            )
pin_tipo = (
            ('digital','Digital'),
            ('analogo','Analogo'),
            )

class pin_placa(models.Model):
    tablero = models.ForeignKey(tablero)
    pin = models.SmallIntegerField()
    modo = models.CharField(max_length=10, choices=pin_modo)
    tipo = models.CharField(max_length=10, choices=pin_tipo)
    def __unicode__(self):
        return u'%s %s %s %s'%(self.tablero,self.pin,self.modo,self.tipo)
    def clean(self):
        from django.core.exceptions import ValidationError
        # Don't allow draft entries to have a pub_date.
        if self.tipo == 'analogo' and self.modo == 'output':
            raise ValidationError('Modo solo puede ser Salida con tipo analogo.')            

pin_control = (
            ('off_auto','Apagago'),
            ('on_auto','Encendido'),
            )

class combinacion_pin(models.Model):
    pin_entrada = models.ForeignKey(pin_placa, related_name="entrada", null=True, blank=True)
    pin_salida = models.ForeignKey(pin_placa, related_name="salida", null=True, blank=True)
    pin_movimiento = models.ForeignKey(pin_placa, related_name="movimiento", null=True, blank=True)
    pin_manejo = models.CharField(max_length=10, choices=pin_control, null=True, blank=True)
    def __unicode__(self):
        return u'%s, %s, {mov %s : %s}'%(self.pin_entrada,self.pin_salida,self.pin_movimiento,self.pin_manejo)
    def clean(self):
        from django.core.exceptions import ValidationError
        # Don't allow draft entries to have a pub_date.
        if self.pin_entrada:
            if self.pin_entrada.modo == 'output':
                raise ValidationError('No puede seleccionar un pin Salida para el campo Pin entrada.')
            if self.pin_entrada.tipo == 'digital' and not self.pin_salida:
                raise ValidationError('Pin salida no puede estar en blanco cuando selecciona pin entrada modo digital.')
        if self.pin_salida:
            if self.pin_salida.modo == 'input':
                raise ValidationError('No puede seleccionar un pin Entrada para el campo Pin salida.')
        if self.pin_movimiento and not self.pin_manejo:
            raise ValidationError('Debe seleccionar el tipo de manejo para Pin Movimiento')
        if not self.pin_movimiento and self.pin_manejo:
            raise ValidationError('Debe seleccionar el pin movimiento para Pin manejo')

