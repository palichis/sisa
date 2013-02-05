# -*- coding: utf-8 -*-
from api.arduino import *
from django.http import HttpResponse
from api.models import tablero
import json
board = board()

#accion=1 cambia estado pin
#accion=0 lee estado pin

def api(request):
    global board
    if 'tablero' in request.GET and request.GET['tablero'] and request.GET['tablero'].isdigit():
        if 'tipo' in request.GET and request.GET['tipo'] and not request.GET['tipo'].isdigit():                
            pin = int(request.GET['pin'])
            tablero_num = int(request.GET['tablero'])
            tablero_db = tablero.objects.filter(id=tablero_num)
            if tablero_db:
                tablero_obj = tablero_db[0]
            else:
                return HttpResponse('{"error":"falta o inválido tablero"}')
            board_tipo = pyfirmata.boards.BOARDS[tablero_obj.placa.nombre]
            if 'pin' in request.GET and request.GET['pin'] and request.GET['pin'].isdigit() and pin in board_tipo['digital']:
                if 'accion' in request.GET and request.GET['accion'] and request.GET['accion'].isdigit():                    
                    if pin in board_tipo['disabled'] and request.GET['tipo'] == 'd':
                        return HttpResponse('{"error":"pin para uso de tablero interno"}')
                    accion = request.GET['accion']
                    if accion == '1' and request.GET['tipo'] == 'd':
                        #print board.tablero_pind[tablero_num][pin].mode
                        if board.tablero_pind[tablero_num][pin].mode == 0:
                            return HttpResponse('{"error":"falta o iválido acción para pin salida"}')
                        elif pin in board.tablero_pind[tablero_num]:
                            board.tablero_pind[tablero_num][pin].write(not board.tablero_pind[tablero_num][pin].value)
                        elif pin in board.tablero_pind[tablero_num]:
                            return HttpResponse('{"error":"pin no inicializado"}')
                        return HttpResponse('{"%s" : {"%s": "%s"}}'%(tablero_num,pin,board.tablero_pind[tablero_num][pin].value))
                    elif accion == '0':
                        if request.GET['tipo'] == 'd':
                            return HttpResponse('{"%s" : {"%s": "%s"}}'%(tablero_num,pin,board.tablero_pind[tablero_num][pin].value))
                        elif request.GET['tipo'] == 'a' and pin in board.tablero_pina[tablero_num]:
                            return HttpResponse('{"%s" : {"%s": "%s"}}'%(tablero_num,pin,board.tablero_pina[tablero_num][pin].read()))
                        elif request.GET['tipo'] not in ('a','d'):
                            return HttpResponse('{"error":"falta o inválido tipo"}')
                        elif pin not in board.tablero_pina[tablero_num]:
                            return HttpResponse('{"error":"pin no inicializado"}')
                    elif int(accion) > 1:
                        return HttpResponse('{"error":"fata o inválida acción"}')
                    else:
                        return HttpResponse('{"error":"falta o iválido acción para pin analogico"}')
                else:
                    return HttpResponse('{"error":"falta o iválido acción para pin"}')
            else:
                return HttpResponse('{"error":"falta o iválido pin"}')
        else:
            return HttpResponse('{"error":"falta o iválido tipo para pin"}')
    elif 'tablero' in request.GET:
         return HttpResponse('{"error":"falta o iválido tablero para pin"}')
    elif 'estado' in request.GET and request.GET['estado'] and request.GET['estado'].isdigit() and int(request.GET['estado']) in (0,1):
        if 'modo' in request.GET and request.GET['modo'] and request.GET['modo'].isdigit() and int(request.GET['modo']) in (0,1):
            if 'tipo' in request.GET and request.GET['tipo'] and not request.GET['tipo'].isdigit() and int(request.GET['tipo']) in ('a','d'):
                print 'j'
            else:
                return HttpResponse('{"error":"falta o iválido tipo"}')
        else:
            return HttpResponse('{"error":"falta o iválido modo"}')
    else:
        return HttpResponse('{"error":"falta o iválido estado"}')
        