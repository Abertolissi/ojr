from django.urls import path
from appOJR import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('getCamiones/', views.getCamiones, name='getCamiones'),
    path('getRemolques/', views.getRemolques, name='getRemolques'),
    path('cargarCamiones/', views.cargarCamionesView, name='cargarCamionesCsv'),
    path('cerrarsesion', views.CerrarSesion, name='cerrarsesion'),

    # --- BARCOS ---
    path('Barco/listar', views.BarcosListar.as_view(), name='listarBarcos'),
    path('Barco/nuevo', views.BarcoCrear.as_view(), name='nuevoBarco'),
    path('Barco/editar/<int:pk>', views.BarcoActualizar.as_view(), name='actualizarBarco'),
    path('Barco/eliminar/<int:pk>', views.BarcoEliminar.as_view(), name='eliminarBarco'),
    path('Barco/detalle/<int:pk>', views.BarcoDetalle.as_view(), name='detallesBarco'),

    # --- CHOFERES ---
    path('Chofer/listar', views.ChoferesListar.as_view(), name='listarChoferes'),
    path('Chofer/nuevo', views.ChoferCrear.as_view(), name='nuevoChofer'),
    path('Chofer/editar/<int:pk>', views.ChoferActualizar.as_view(), name='actualizarChofer'),
    path('Chofer/eliminar/<int:pk>', views.ChoferEliminar.as_view(), name='eliminarChofer'),
    path('Chofer/detalle/<int:pk>', views.ChoferDetalle.as_view(), name='detallesChofer'),

    # --- ARMADORAS ---
    path('Armadora/listar', views.ArmadorasListar.as_view(), name='listarArmadoras'),
    path('Armadora/nuevo', views.ArmadoraCrear.as_view(), name='nuevaArmadora'),
    path('Armadora/editar/<int:pk>', views.ArmadoraActualizar.as_view(), name='actualizarArmadora'),
    path('Armadora/eliminar/<int:pk>', views.ArmadoraEliminar.as_view(), name='eliminarArmadora'),
    path('Armadora/detalle/<int:pk>', views.ArmadoraDetalle.as_view(), name='detalleArmadora'),

    # --- AGENCIAS MARITIMAS ---
    path('AgenciaMaritima/listar', views.AgenciaMaritimaListar.as_view(), name='listarAgenciasMaritimas'),
    path('AgenciaMaritima/nuevo', views.AgenciaMaritimaCrear.as_view(), name='nuevaAgenciaMaritima'),
    path('AgenciaMaritima/editar/<int:pk>', views.AgenciaMaritimaActualizar.as_view(), name='actualizarAgenciaMaritima'),
    path('AgenciaMaritima/eliminar/<int:pk>', views.AgenciaMaritimaEliminar.as_view(), name='eliminarAgenciaMaritima'),

    # --- PUERTOS ---
    path('Puerto/listar', views.PuertoListar.as_view(), name='listarPuertos'),
    path('Puerto/nuevo', views.PuertoCrear.as_view(), name='nuevoPuerto'),
    path('Puerto/editar/<int:pk>', views.PuertoActualizar.as_view(), name='actualizarPuerto'),
    path('Puerto/eliminar/<int:pk>', views.PuertoEliminar.as_view(), name='eliminarPuerto'),

    # --- CONTACTOS AGENCIA ---
    path('ContactoAgencia/listar', views.ContactoAgenciaListar.as_view(), name='listarContactosAgencia'),
    path('ContactoAgencia/nuevo', views.ContactoAgenciaCrear.as_view(), name='nuevoContactoAgencia'),
    path('ContactoAgencia/editar/<int:pk>', views.ContactoAgenciaActualizar.as_view(), name='actualizarContactoAgencia'),
    path('ContactoAgencia/eliminar/<int:pk>', views.ContactoAgenciaEliminar.as_view(), name='eliminarContactoAgencia'),

    # --- CLIENTES ---
    path('Cliente/listar', views.ClienteListar.as_view(), name='listarClientes'),
    path('Cliente/nuevo', views.ClienteCrear.as_view(), name='nuevoCliente'),
    path('Cliente/editar/<int:pk>', views.ClienteActualizar.as_view(), name='actualizarCliente'),
    path('Cliente/eliminar/<int:pk>', views.ClienteEliminar.as_view(), name='eliminarCliente'),

    # --- TRANSPORTES ---
    path('Transporte/listar', views.TransporteListar.as_view(), name='listarTransportes'),
    path('Transporte/nuevo', views.TransporteCrear.as_view(), name='nuevoTransporte'),
    path('Transporte/editar/<int:pk>', views.TransporteActualizar.as_view(), name='actualizarTransporte'),
    path('Transporte/eliminar/<int:pk>', views.TransporteEliminar.as_view(), name='eliminarTransporte'),

    # --- CAMIONES ---
    path('Camion/listar', views.CamionListar.as_view(), name='listarCamiones'),
    path('Camion/nuevo', views.CamionCrear.as_view(), name='nuevoCamion'),
    path('Camion/editar/<int:pk>', views.CamionActualizar.as_view(), name='actualizarCamion'),
    path('Camion/eliminar/<int:pk>', views.CamionEliminar.as_view(), name='eliminarCamion'),

    # --- REMOLQUES ---
    path('Remolque/listar', views.RemolqueListar.as_view(), name='listarRemolques'),
    path('Remolque/nuevo', views.RemolqueCrear.as_view(), name='nuevoRemolque'),
    path('Remolque/editar/<int:pk>', views.RemolqueActualizar.as_view(), name='actualizarRemolque'),
    path('Remolque/eliminar/<int:pk>', views.RemolqueEliminar.as_view(), name='eliminarRemolque'),

    # --- PRODUCTOS ---
    path('Producto/listar', views.ProductoListar.as_view(), name='listarProductos'),
    path('Producto/nuevo', views.ProductoCrear.as_view(), name='nuevoProducto'),
    path('Producto/editar/<int:pk>', views.ProductoActualizar.as_view(), name='actualizarProducto'),
    path('Producto/eliminar/<int:pk>', views.ProductoEliminar.as_view(), name='eliminarProducto'),

    # --- RANCHOS ---
    path('Rancho/listar', views.RanchoListar.as_view(), name='listarRanchos'),
    path('Rancho/nuevo', views.RanchoCrear.as_view(), name='nuevoRancho'),
    path('Rancho/editar/<int:pk>', views.RanchoActualizar.as_view(), name='actualizarRancho'),
    path('Rancho/eliminar/<int:pk>', views.RanchoEliminar.as_view(), name='eliminarRancho'),

		# --- COMBUSTIBLES ---
    path('Combustible/listar', views.CombustibleListar.as_view(), name='listarCombustibles'),
    path('Combustible/nuevo', views.CombustibleCrear.as_view(), name='nuevoCombustible'),
    path('Combustible/editar/<int:pk>', views.CombustibleActualizar.as_view(), name='actualizarCombustible'),
    path('Combustible/eliminar/<int:pk>', views.CombustibleEliminar.as_view(), name='eliminarCombustible'),


    # --- CARGAS ---
    path('Carga/listar', views.CargaListar.as_view(),name='listarCargas'),
    path('Carga/editar/<int:pk>', views.CargaActualizar.as_view(), name='actualizarCarga'),
    path('Carga/eliminar/<int:pk>', views.CargaEliminar.as_view(), name='eliminarCarga'),
    path('Carga/generarDocumentoCarga/<int:idCarga>', views.generarDocumento, name='generarDocumentoCarga'),

    # --- REMITOS ---
    path('Remito/listar', views.RemitosListar.as_view(),name='listarRemitos'),
    path('RemitoCombustible/nuevo', views.RemitoCombustibleCrear.as_view(), name='nuevoRemitoCombustible'),
    path('RemitoVarios/nuevo', views.RemitoVariosCrear.as_view(), name='nuevoRemitoVarios'),
    path('Remito/detalle/<int:pk>', views.RemitoDetalle.as_view(), name='detalleRemito'),
    path('Remito/editar/<int:pk>', views.RemitoActualizar.as_view(), name='actualizarRemito'),
    path('Remito/eliminar/<int:pk>', views.RemitoEliminar.as_view(), name='eliminarRemito'),
    path('Remito/generarRemitoCombustible/<int:idRemito>/<str:impresora>', views.generarRemitoCombustible, name='generarRemitoCombustible'),

]