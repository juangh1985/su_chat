# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#~ Importando elementos necesarios
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpRequest,HttpResponse
from django.db.models import Q
#~ Lo mas importante aqui es el uso de los usuarios que trae el sistema por defecto.
from django.contrib.auth.models import User

from conversations.models import *
from conversations.forms import *


#~ Primera vista. Muy simple. 
#~ Aunque pudiera enviar directo a la plantilla los datos, queda la posibilidad de tener otros elementos para enviar.
def Presentations(request):
	#~ Seleccionar todo desde los usuarios y enviarlo a "presentation.html"
	u=User.objects.all()
	context = {'users':u,}
	return render(request, 'presentation.html', context)


#~ Esta vista se encarga de gestionar todo lo relacionado con las conecciones entre los usuarios
#~ Lo primero que se hace es atrapar "user_id"
#~ Si no viene nada en "user_id" entonces redirecciono para / en la linea 60
def Connections(request, user_id):
	if user_id:
		#~ Seleccion del usuario especifico enviado desde la presentacion
		u=User.objects.get(id=user_id)
		#~ Seleccion del resto de los usuarios excluyendo el usuario previo seleccionado
		allusers=User.objects.exclude(id=user_id)
		#~ Seleccion de las conecciones realizadas donde el remitente es el usuario seleccionado
		c=Connected.objects.filter(sender=u)

		#~ una vez accionado la opcion de realizar enlace con otro usuario
		if request.method=='POST':
			#~ atrapo la variable enviada de quien sera el nuevo vinculo
			addressee = request.POST.get ('addressee')
			#~ selecciono el usuario a la que pertenece
			a = User.objects.get(id=addressee)
			#~ realizo una validacion para ver si ya estaban conectados
			test = Connected.objects.filter(sender=u, addressee=a)
			#~ si estaban conectados, envio mensaje y recargo la pagina con los datos
			if test:
				message="Enlace realizado anteriormente."
				context = {'allusers':allusers,'user':u, 'connections':c, 'message':message}
				return render(request, 'connections.html', context)
			#~ sino creo el nuevo vinculo entre en remitente y el destinatario con una validacion de True en el boolean linked
			#~ y envio mensaje
			else:
				new = Connected(sender=u, addressee=a, linked=True)
				new.save()
				message="Enlace realizado correctamente."
				context = {'allusers':allusers,'user':u, 'connections':c, 'message':message}
				return render(request, 'connections.html', context)
		#~ mientras, muestro los datos y solo espero a que ocurra una accion
		context = {'allusers':allusers,'user':u, 'connections':c}
		return render(request, 'connections.html', context)
	else:
		return HttpResponseRedirect('/')


#~ la pagina del usuario donde ocurre el "chat"
#~ Lo primero es atrapar el usuario que solicita el chat "user_id" y el destinatario "addressee_id"
def UserPage(request, user_id, addressee_id):
	#~ reviso y valido que vengan los dos
	if user_id and addressee_id:
		#~ los selecciono
		u=User.objects.get(id=user_id)
		a=User.objects.get(id=addressee_id)
		#~ extraigo todas sus conversaciones en ambos sentidos
		#~ donde estan involucrados los dos usuarios
		#~ y lo ordeno por fecha
		c=Conversations.objects.filter( Q(addressee=u, sender=a) | Q(addressee=a, sender=u) ).order_by('-registered')

		#~ si viene algo por el post
		if request.method=='POST':
			#~ cargo el formulario del chat definido dentro del "forms.py" aunque alli solo fue necesario poner el texto que se envian.
			form_chat = conversations_forms(request.POST)
			if form_chat.is_valid():
				form = form_chat.save(commit=False)
				#~ con las selecciones previas
				#~ extraigo al remitente
				form.sender=u
				#~ y al destinatario
				form.addressee=a
				#~ por defecto, leido verdadero
				form.read=True
				#~ y salvo el formulario
				form.save()
				#~ redireccionando nuevamente a la misma pagina, cargando los dos usuarios
			return HttpResponseRedirect('/chat/%s/%s' % (user_id,addressee_id))
		else:
			form_chat = conversations_forms()
		context = {'user_id':user_id,'user':u,'addressee':a,'conversations':c,'form_chat':form_chat,}
		return render(request, 'user-page.html', context)

