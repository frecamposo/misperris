from django.contrib import admin
# importar los modelos
from .models import Categoria, Mascota, Galeria

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Mascota) 
admin.site.register(Galeria)