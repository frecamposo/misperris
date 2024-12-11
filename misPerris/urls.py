from django.contrib import admin
from django.urls import path, include
# importar los controladores "views"
from .views import insertar_galeria, devolver, admin_usuario, adoptar, modificacion,modificar_mascota, eliminar_mascota,crear_usuario, cerrar_sesion,login, filtro_cate,filtro_desc, buscar_nombre_mascota,filtro_categoria,index, galeria, formulario, registro,ficha_mascota

# agregar las rutas hacia los controladores
urlpatterns = [
    path('',index,name='IND'),
    path('galeria/',galeria,name='GALE'),
    path('formulario/',formulario,name='FORMU'),
    path('registro/',registro,name='REG'),
    path('ficha/<id>/',ficha_mascota,name='FICHAM'),
    path('filtro_categoria/',filtro_categoria,name='FILTROC'),
    path('buscar_nombre/',buscar_nombre_mascota,name='BUSCARN'),
    path('filtro_desc/',filtro_desc,name='FILTROD'),
    path('filtro_cate/<id>/',filtro_cate,name='FILTROCATE'),
    path('login/',login,name='LOGIN'),
    path('cerrar_sesion/',cerrar_sesion,name='CERRAR'),
    path('crear_usuario/',crear_usuario,name='CREARU'),
    path('eliminar_mascota/<id>/',eliminar_mascota,name='ELIM'),
    path('modi_mascota/<id>/',modificar_mascota,name='MODIM'),
    path('modificacion/',modificacion,name='MODIFICACION'),
    path('adoptar/<id>/',adoptar,name='ADOPTAR'),
    path('admin_usuario/',admin_usuario, name='ADMINUSUARIO'),
    path('devolver/<id>/',devolver,name='DEVOLVER'),
    path('insertar_galeria/',insertar_galeria, name='INSERTARG'),
]
# {% url '<nombre>' %}