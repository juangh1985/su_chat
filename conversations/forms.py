#~ Las importaciones de rigor
from django.forms import *
from django import forms
#~ importo los modelos desde la app
from conversations.models import *

#~ creo el formulario
class conversations_forms(ModelForm):
	class Meta:
		model = Conversations
		#~ definiendo los campos que quiero, en este caso, solo chat.
		fields = ['chat']
		#~ le doy estilo sobre la base de los css y js que estan cargados en el settings
		widgets = {
		'chat': TextInput(attrs={"type":"text","class":"form-control","placeholder":"Escribe un mensaje aqui"}),
		} 
