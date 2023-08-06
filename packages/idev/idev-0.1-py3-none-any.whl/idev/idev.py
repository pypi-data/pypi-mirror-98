import os
import subprocess
import json
import re
### diálogo
#api text
class dialog:

###dialogo
    def text(interior,titulo):
        variable = (subprocess.check_output(['termux-dialog','text','-m','-i',interior,'-t',titulo]))
        js = (variable)
        vari = (json.loads(js))
        mensaje = (vari['text'])
        return (mensaje)
###number      
    def number(interior,titulo):
        variable = (subprocess.check_output(['termux-dialog','text','-n','-i',interior,'-t',titulo]))
        js = (variable)
        vari = (json.loads(js))
        mensaje = (vari['text'])
        return (mensaje)
        
##speech
    def speech(interior,titulo):
        variable = (subprocess.check_output(['termux-dialog','speech','-i',interior,'-t',titulo]))
        js = (variable)
        vari = (json.loads(js))
        mensaje = (vari['text'])
        return (mensaje)
        
###confirm
    def confirm(interior,titulo):
        variable = (subprocess.check_output(['termux-dialog','confirm','-i',interior,'-t',titulo]))
        js = (variable)
        vari = (json.loads(js))
        mensaje = (vari['text'])
        return (mensaje)

###time
    def time(titulo):
        variable = (subprocess.check_output(['termux-dialog','time','-t',titulo]))
        js = (variable)
        vari = (json.loads(js))
        mensaje = (vari['text'])
        return (mensaje)
#counter
    def counter(titulo):
        variable = (subprocess.check_output(['termux-dialog','counter','-r','1,50,25','-t',titulo]))
        js = (variable)
        vari = (json.loads(js))
        mensaje = (vari['text'])
        return (mensaje)
        
    def check(opciones,titulo):
        variable = (subprocess.check_output(['termux-dialog','checkbox','-v',opciones,'-t',titulo]))
        js = (variable)
        vari = (json.loads(js))
        mensaje = (vari['text'])
        valor = (re.sub(r'[\[\]]', "", mensaje))
        return (valor)
        
#api counter        
####>>>>>))))
class clipboard:
##clipboard get 
    def get():
        variable = (subprocess.check_output(['termux-clipboard-get']))
        variable1 = str(variable)
        mensaje = ((variable1.replace("b'","")))
        #uso :
        # print (TERMUX_API.clipboard.get().decode('utf-8'))
        return (variable)
        
### clipboard set 
    def _set(valor):
        variable = (subprocess.check_output(['termux-clipboard-set',valor]))
       
       
class brightness:
    def b(valor):
        variable = (subprocess.check_output(['termux-brightness',valor]))
        
        
class notification:
    def n(texto):
        variable = (subprocess.check_output(['termux-notification','-c',texto]))
        
  
        
class tts:
    def speak(valor):
        variable = (subprocess.check_output(['termux-tts-speak',valor]))
        
        
        
        
class youtube:
  
  
    def url(link):
        
        resultado = (subprocess.check_output(['url',link]))
        
        return (resultado)
        
    def descripcion(des):
        
        resultado = (subprocess.check_output(['descripcion',des]))
        
        return (resultado)
        
    def titulo(title):
        
        resultado = (subprocess.check_output(['titulo',title]))
        
        return (resultado)
        
        
    def yt(busqueda):
        
        buscar = (subprocess.check_output(['buscar',busqueda]))
        
        return (buscar)