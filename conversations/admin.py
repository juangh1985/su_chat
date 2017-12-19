from django.contrib import admin

# Register your models here.
from conversations.models import *

#~ Muy simple la administracion
#~ Se muestra en ambos casos los datos de cada uno de los modelos

class Conversations_admin(admin.ModelAdmin):
	list_display = ('sender', 'addressee', 'chat', 'registered')
admin.site.register(Conversations, Conversations_admin)

class Connections_admin(admin.ModelAdmin):
	list_display = ('sender', 'addressee', 'linked')
admin.site.register(Connected, Connections_admin)
