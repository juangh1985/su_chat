from __future__ import unicode_literals

from django.db import models

#~ Aprovechando el sistema de autenticacion de Django, me quedo con los usuarios
#~ Si se desea incorporar mas elementos como fotos u otros, es tan solo crear una nueva clase modelo y hacer la relacion
from django.contrib.auth.models import User


from django.conf import settings

#~ una primera clase donde se guardaran los vinculos de los usuarios
class Connected(models.Model):
	#~ ambos tienen sus related_name
	sender = models.ForeignKey(User, related_name="connection_sender")
	addressee = models.ForeignKey(User, related_name="connection_addressee")
	linked = models.BooleanField('linked', max_length=3, blank=True)
	#~ se define ademas, que la relacion entre remitente y destinatario es unica
	class Meta:
		unique_together = ('sender', 'addressee',)

#~ clase conversaciones
class Conversations(models.Model):
	#~ id del remitente y del destinatario
	sender = models.ForeignKey(User, related_name="sender")
	addressee = models.ForeignKey(User, related_name="addressee")
	#~ texto con posibilidad de contar hasta 2048 caracteres
	chat=models.CharField('Chat',max_length=2048, blank=True)
	read = models.BooleanField('Read', max_length=3, blank=True)
	#~ la fecha en que fue escrito
	registered=models.DateTimeField('Registered',max_length=256, auto_now=True, blank=True)

