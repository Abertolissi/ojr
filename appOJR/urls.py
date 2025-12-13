from django.urls import path, include
from appOJR import admin, views
from appOJR.views import BarcoDetalle,  BarcoActualizar, BarcoEliminar, CerrarSesion,ChoferActualizar, ChoferDetalle, ChoferEliminar, cargarCamionesView,  getCamiones, getRemolques



urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('getCamiones/', getCamiones, name='getCamiones'),
    path('getRemolques/', getRemolques, name='getRemolques'),
    path('cargarCamiones/', cargarCamionesView, name='cargarCamionesCsv'),
    path('cerrarsesion', CerrarSesion, name='cerrarsesion'),	
]





urlpatterns += [

     #Mostrar todos los registros en una tabla
    path('Barco/listar', views.BarcosListar.as_view(), name='listarBarcos'),
    #Mostrar una página con el detalle del registro
    path('Barco/detalle/<int:pk>', BarcoDetalle.as_view(template_name = "appOJR/detallesBarco.html"), name='detallesBarco'),
    #Mostrar formulario de alta de nuevo registro
    path('Barco/nuevo', views.BarcoCrear.as_view(), name='nuevoBarco'),
    #Mostrar formulario de modificación de registro
    path('Barco/editar/<int:pk>', BarcoActualizar.as_view(), name='actualizarBarco'), 
    #Eliminar un registro
    path('Barco/eliminar/<int:pk>', BarcoEliminar.as_view(), name='eliminarBarco'),    
    #Redirección a html Cerrar Sesión (logout.html)

]



urlpatterns += [

     #Mostrar todos los registros en una tabla
    path('Chofer/listar', views.ChoferesListar.as_view(), name='listarChoferes'),
    #Mostrar una página con el detalle del registro
    path('Chofer/detalle/<int:pk>', ChoferDetalle.as_view(), name='detallesChofer'),
    #Mostrar formulario de alta de nuevo registro
    path('Chofer/nuevo', views.ChoferCrear.as_view(), name='nuevoChofer'),
    #Mostrar formulario de modificación de registro
    path('Chofer/editar/<int:pk>', ChoferActualizar.as_view(), name='actualizarChofer'), 
    #Eliminar un registro
    path('Chofer/eliminar/<int:pk>', ChoferEliminar.as_view(), name='eliminarChofer'),    
    #Redirección a html Cerrar Sesión (logout.html)
    

]

urlpatterns += [

    #Mostrar todos los registros en una tabla
    path('Remito/listar', views.RemitosListar.as_view(),name='listarRemitos'),
    #Mostrar formulario de alta de nuevo registro
    path('RemitoCombustible/nuevo', views.RemitoCombustibleCrear.as_view(), name='nuevoRemitoCombustible'),
    #Mostrar formulario de alta de nuevo registro
    path('RemitoVarios/nuevo', views.RemitoVariosCrear.as_view(), name='nuevoRemitoVarios'),
    #Mostrar una página con el detalle del registro
    path('Remito/detalle/<int:pk>', views.RemitoDetalle.as_view(), name='detalleRemito'),
    #Mostrar formulario de modificación de registro
    path('Remito/editar/<int:pk>', views.RemitoActualizar.as_view(), name='actualizarRemito'), 
    #Eliminar un registro
    path('Remito/eliminar/<int:pk>', views.RemitoEliminar.as_view(), name='eliminarRemito'),    
    #Generar formularios de carga
    path('Remito/generarRemitoCombustible/<int:idRemito>/<str:impresora>', views.generarRemitoCombustible, name='generarRemitoCombustible'),
    
]

urlpatterns += [

    #Mostrar todos los registros en una tabla
    path('Carga/listar', views.CargaListar.as_view(),name='listarCargas'),
    #Mostrar formulario de alta de nuevo registro
    #Mostrar formulario de modificación de registro
    path('Carga/editar/<int:pk>', views.CargaActualizar.as_view(), name='actualizarCarga'), 
    #Eliminar un registro
    path('Carga/eliminar/<int:pk>', views.CargaEliminar.as_view(), name='eliminarCarga'),    
    #Generar formularios de carga
    path('Carga/generarDocumentoCarga/<int:idCarga>', views.generarDocumento, name='generarDocumentoCarga'),
    

    
]

urlpatterns += [

     #Mostrar todos los registros en una tabla
    path('Armadora/listar', views.ArmadorasListar.as_view(),name='listarArmadoras'),
     #Mostrar formulario de alta de nuevo registro
    path('Armadora/nuevo', views.ArmadoraCrear.as_view(), name='nuevaArmadora'),
    #Mostrar una página con el detalle del registro
    path('Armadora/detalle/<int:pk>', views.ArmadoraDetalle.as_view(), name='detalleArmadora'),
    #Mostrar formulario de modificación de registro
    path('Armadora/editar/<int:pk>', views.ArmadoraActualizar.as_view(), name='actualizarArmadora'), 
    #Eliminar un registro
    path('Armadora/eliminar/<int:pk>', views.ArmadoraEliminar.as_view(), name='eliminarArmadora'),    
   
]