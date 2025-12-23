import datetime
from django.db import models

# Create your models here.

from django.utils import timezone




#Clase "AgenciaMaritima" 
class AgenciaMaritima(models.Model):
	nombre = models.CharField(max_length=100, null=False, verbose_name="nombre")
	telefono = models.CharField(max_length=100, null=False, verbose_name="telefono", default="")
	def __str__(self):
		return self.nombre

	class Meta:
		 db_table = 'AgenciaMaritima' # Nombre que tendrá la tabla que se creará en la base de datos en la Base de Datos

# Clase "Puerto" 
class Puerto(models.Model):
	nombre  = models.CharField(max_length=100, null=False, verbose_name="Nombre", default="")
	codigoAduana = models.IntegerField(null=True, verbose_name="codigoAduana")
	fecha_alta = models.DateTimeField(auto_now_add=True)
	fecha_actualizacion = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.nombre

	class Meta:
		db_table = 'Puerto' # Nombre que tendrá la tabla que se creará en la base de datos en la Base de Datos
		ordering = ["nombre"]

class ContactoAgencia(models.Model):
	nombre = models.CharField(max_length=100, null=False, verbose_name="nombre")
	apellido = models.CharField(max_length=100, null=False, verbose_name="apellido")
	telefono = models.CharField(max_length=100, null=False, verbose_name="telefono", default="")
	agenciaMaritima = models.ForeignKey('AgenciaMaritima', on_delete=models.CASCADE)
	correoElectronico = models.EmailField(max_length=50, verbose_name="emailContacto", default="")
	enviaRancho = models.BooleanField(default = False)
	def __str__(self):
		return self.nombre + " " +  self.apellido

	class Meta:
		 db_table = 'ContactoAgencia' # Nombre que tendrá la tabla que se creará en la base de datos en la Base de Datos


# Clase "Armadora" 
class Armadora(models.Model):
	nombre = models.CharField(max_length=100, null=False, verbose_name="nombre")
	direccion = models.CharField(max_length=150, blank=True, verbose_name="direccion", default="")
	cuit = models.CharField(max_length=13, blank=True, verbose_name="cuit", default="")
	telefono =  models.CharField(max_length=100, null=False, verbose_name="telefono", default="")
	puertos = models.ManyToManyField('Puerto', through='ArmadoraPuerto')
	agenciaMaritima = models.ForeignKey('AgenciaMaritima', on_delete=models.CASCADE)
	fecha_alta = models.DateTimeField(auto_now_add=True)
	fecha_actualizacion = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.nombre

	class Meta:
		db_table = 'Armadora' # Nombre que tendrá la tabla que se creará en la base de datos en la Base de Datos
		ordering = ["nombre"]

class ArmadoraPuerto(models.Model):
	armadora = models.ForeignKey(Armadora, on_delete=models.CASCADE)
	puerto = models.ForeignKey(Puerto, on_delete=models.CASCADE)
	agenciaMaritima = models.ForeignKey(AgenciaMaritima, on_delete=models.CASCADE)
    # Otros campos adicionales que necesites para la relación intermedia
	fecha_alta = models.DateTimeField(auto_now_add=True)
	fecha_actualizacion = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'ArmadoraPuerto'
		unique_together = (('armadora', 'puerto'),)

# Clase "Barcos" 
class Barco(models.Model):
	nombre = models.CharField(max_length=100, null=False, verbose_name="nombre", default="")
	tipo = models.CharField(max_length=15, null=False, verbose_name="tipo", default="")
	matricula =models.CharField(max_length=15, null=False, verbose_name="matricula", default="")
	bandera = models.CharField(max_length=30, null=False, verbose_name="bandera", default="")
	eslora = models.DecimalField(max_digits=10, decimal_places=2,null=True, verbose_name="eslora", default="")
	manga = models.DecimalField(max_digits=10, decimal_places=2,null=True, verbose_name="manga", default="")
	puntal = models.DecimalField(max_digits=10, decimal_places=2,null=True, verbose_name="puntal", default="")
	armadora = models.ForeignKey('Armadora', on_delete=models.CASCADE)
	fecha_alta = models.DateTimeField(auto_now_add=True)
	fecha_actualizacion = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.nombre

	class Meta:
		db_table = 'Barco' # Nombre que tendrá la tabla que se creará en la base de datos en la Base de Datos
		ordering = ["nombre"]

class Cliente(models.Model):
	denominacion = models.CharField(max_length=100, null=False, verbose_name="denominacion", default="")
	cuit = models.CharField(max_length=13, blank=True, verbose_name="cuit", default="")
	fecha_alta = models.DateTimeField(auto_now_add=True)
	fecha_actualizacion = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.denominacion

	class Meta:
		 db_table = 'Cliente' # Nombre que tendrá la tabla que se creará en la base de datos en la Base de Datos

class Transporte(models.Model):
	abreviatura = models.CharField(max_length=10, null=False, verbose_name="abreviatura", default="")
	nombre = models.CharField(max_length=100, null=False, verbose_name="nombre", default="")
	cuit = models.CharField(max_length=13, blank=True, verbose_name="cuit", default="")
	def __str__(self):
		return self.abreviatura

	class Meta:
		 db_table = 'Transporte' # Nombre que tendrá la tabla que se creará en la base de datos en la Base de Datos



class Combustible(models.Model):
	nombre = models.CharField(max_length=100, null=False, verbose_name="nombre", default="")
	fecha_alta = models.DateTimeField(auto_now_add=True)
	fecha_actualizacion = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.nombre

	class Meta:
		db_table = 'Combustible' # Nombre que tendrá la tabla que se creará en la base de datos en la Base de Datos
		ordering = ["nombre"]


class Chofer(models.Model):
	apellido = models.CharField(max_length=100, null=False, verbose_name="apellido", default="")
	nombre = models.CharField(max_length=100, null=False, verbose_name="nombre", default="")
	dni = models.CharField(max_length=10, null=True, verbose_name="dni", default="")
	telefono =  models.CharField(max_length=50, null=False, verbose_name="telefono", default="")
	domicilio = models.CharField(max_length=100, null=False, verbose_name="domicilio", default="")
	nacionalidad = models.CharField(max_length=100, null=False, verbose_name="nacionalidad", default="")
	pna = models.CharField(max_length=20, null=True, verbose_name="pna", default="")
	fecha_alta = models.DateTimeField(auto_now_add=True)
	fecha_actualizacion = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.nombre + ' ' + self.apellido

	class Meta:
		db_table = 'Chofer' # Nombre que tendrá la tabla que se creará en la base de datos en la Base de Datos

class Camion(models.Model):
	marca = models.CharField(max_length=100, null=False, verbose_name="marca", default="")
	patente = models.CharField(max_length=15, null=False, verbose_name="patente", default="")
	transporte = models.ForeignKey(Transporte, on_delete=models.CASCADE)
	habilitadoAFIP = models.BooleanField(default = False)
	fecha_alta = models.DateTimeField(auto_now_add=True)
	fecha_actualizacion = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.patente

	class Meta:
		 db_table = 'Camion' # Nombre que tendrá la tabla que se creará en la base de datos en la Base de Datos

class Remolque(models.Model):
	marca = models.CharField(max_length=100, null=False, verbose_name="marca", default="")
	patente = models.CharField(max_length=15, null=False, verbose_name="patente", default="")
	transporte = models.ForeignKey(Transporte, on_delete=models.CASCADE)
	fecha_alta = models.DateTimeField(auto_now_add=True)
	fecha_actualizacion = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.patente

	class Meta:
		 db_table = 'Remolque' # Nombre que tendrá la tabla que se creará en la base de datos en la Base de Datos

Impresora_CHOICES = (
	('LaserNuria', 'LaserNuria'),
    ('Brother' ,'Brother'))



class Configuracion(models.Model):
	empresa = models.CharField(max_length=100, null=False, verbose_name="empresa", default="")
	titularEmpresa =models.CharField(max_length=100, null=False, verbose_name="titularEmpresa", default="")
	direccionEmpresa =  models.CharField(max_length=100, null=False, verbose_name="direccionEmpresa", default="")
	cuitEmpresa = models.CharField(max_length=15, null=False, verbose_name="cuitEmpresa", default="")
	telefonoEmpresa =  models.CharField(max_length=100, null=False, verbose_name="telefonoEmpresa", default="")
	emailEmpresa = models.EmailField(max_length=50, null=True,verbose_name="emailEmpresa", default="")
	certificadoInscripcion =models.CharField(max_length=20, null=False, verbose_name="certificadoInscripcion", default="")
	vencimientoCertificadoInscripcion =  models.DateTimeField(verbose_name="vencimientoCertificadoInscripcion",default=timezone.now)
	aseguradoraChoferes=models.CharField(max_length=20, null=False, verbose_name="aseguradoraChoferes", default="")
	vencimientoAseguradora=models.DateTimeField(verbose_name="vencimientoAseguradora",default=timezone.now)
	impresoraRemitos = models.CharField(max_length=20, choices=Impresora_CHOICES)
	fecha_actualizacion = models.DateTimeField(auto_now=True)
	class Meta:
		db_table = 'Configuracion' # Nombre que tendrá la tabla que se creará en la base de datos en la Base de Datos


SitioPuerto_CHOICES = (
	(' ', ' '),
    ('1' ,'1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
    ('MUELLE NUEVO','MUELLE NUEVO'),
    ('MUELLE CONARPESA','MUELLE CONARPESA'),
    ('MUELLE JUAN GRANADA','MUELLE JUAN GRANADA'),
	('MUELLE JUAN GRANADA 3','MUELLE JUAN GRANADA 3'),
    ('MUELLE CABO VIRGENES','MUELLE CABO VIRGENES'),
    ('MUELLE CAMARONES','MUELLE CAMARONES' ),
    ('MUELLE S.A.O', 'MUELLE S.A.O' ),
    ('MUELLE S.A.E', 'MUELLE S.A.E'))

Empresa_CHOICES = (
	('OJR', 'OJR'),
    ('NAO' ,'NAO')
	)

class Carga(models.Model):
    
	combustible = models.ForeignKey(Combustible, on_delete=models.CASCADE)
	barco = models.ForeignKey(Barco, on_delete=models.CASCADE)
	puerto = models.ForeignKey(Puerto, on_delete=models.CASCADE)
	sitioPuerto = models.CharField(max_length=50,null=False, choices=SitioPuerto_CHOICES,verbose_name="sitioPuerto", default="") 
	densidad = models.DecimalField(max_digits=10, decimal_places=4,null=True, verbose_name="densidad", default="1")
	temperatura = models.DecimalField(max_digits=10, decimal_places=2,null=True, verbose_name="temperatura", default="1")
	exentoRancho = models.BooleanField(default = False)
	nroRancho = models.IntegerField(null=True, blank = True, verbose_name="nroRancho")
	letraRancho = models.CharField(null=True, blank = True, max_length=1,verbose_name="letraRancho")
	ordenCompra =  models.CharField(null=True, blank = True, max_length=100,verbose_name="ordenCompra")
	fechaInicio = models.DateField(default=timezone.now)
	horaInicio = models.TimeField(null=True, blank=True)
	class Meta:
		db_table = 'Carga' # Nombre que tendrá la tabla que se creará en la base de datos en la Base de Datos


Transporte_CHOICES = (
	('OJR ', 'Orlando Jorge Robert'),
    ('NAO' ,'NAO'),
	('VESPRINI','Vesprini'),
	('TRC' ,'Transcont'))

class Remito(models.Model):
        carga = models.ForeignKey(Carga, db_column='carga_id', on_delete= models.SET_NULL, null=True)
        empresa = models.CharField(max_length=10,null=False, choices=Empresa_CHOICES,verbose_name="empresa", default="")
        transporte = models.ForeignKey(Transporte, on_delete=models.CASCADE, null=True)
        numero = models.IntegerField(null=True, verbose_name='numero', default='1')
        chofer = models.ForeignKey(Chofer, on_delete=models.CASCADE, null=True)
        camion = models.ForeignKey(Camion, on_delete=models.CASCADE, null=True)
        remolque = models.ForeignKey(Remolque, on_delete=models.CASCADE, null=True)
        cantidadBarco = models.DecimalField(null=True, verbose_name='cantidadBarco', default='1', max_digits=30,decimal_places=2)
        cantidadDeposito = models.DecimalField(null=True, verbose_name="cantidadDeposito", default="1",max_digits=30,decimal_places=2)

        class Meta:
                db_table = 'Remito' # Nombre que tendrá la tabla que se creará en la base de datos en la Base de Datos


class Deposito(models.Model):
    nombre = models.CharField(max_length=100, null=False, verbose_name="nombre", default="")
    direccion = models.CharField(max_length=100, blank=True, verbose_name="direccion", default="")
    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'Deposito'
        ordering = ["nombre"]

class TransferenciaDeposito(models.Model):
        fecha = models.DateTimeField(default=timezone.now, verbose_name="fecha")
        combustible = models.ForeignKey(Combustible, on_delete=models.CASCADE)
        deposito_origen = models.CharField(max_length=100, null=False, verbose_name="deposito_origen", default="")
        deposito_destino = models.CharField(max_length=100, null=False, verbose_name="deposito_destino", default="")
        deposito_origen_ref = models.ForeignKey(Deposito, on_delete=models.SET_NULL, null=True, blank=True, related_name='transferencias_origen', verbose_name="deposito_origen_ref")
        deposito_destino_ref = models.ForeignKey(Deposito, on_delete=models.SET_NULL, null=True, blank=True, related_name='transferencias_destino', verbose_name="deposito_destino_ref")
        cantidad = models.DecimalField(max_digits=30, decimal_places=2, null=True, verbose_name="cantidad", default="0")
        chofer = models.ForeignKey(Chofer, on_delete=models.CASCADE, null=True)
        camion = models.ForeignKey(Camion, on_delete=models.CASCADE, null=True)
        observaciones = models.CharField(max_length=255, null=True, blank=True, verbose_name="observaciones", default="")

        def __str__(self):
                return f"Transferencia {self.combustible.nombre} {self.deposito_origen} -> {self.deposito_destino}"

        class Meta:
                db_table = 'TransferenciaDeposito'


Unidad_CHOICES = (
        ('TN ', 'TN'),
    ('LTS' ,'LTS'),
	('MT2' ,'MT2'))

IVA_CHOICES = (
	('RI ', 'Responsable Inscripto'),
    ('CF' ,'Consumidor Final'),
	('EX ', 'Exento'))

TransporteRemito_CHOICES = (
	('OJR ', 'Orlando Jorge Robert'),
    ('JPM' ,'Juan Pedro Mairal'),
	('VESPRINI','Vesprini'),
	('TRC' ,'Transcont')
	)

class Producto(models.Model):
	denominacion = models.CharField(max_length=100, null=False, verbose_name="denominacion", default="")
	fecha_alta = models.DateTimeField(auto_now_add=True)
	fecha_actualizacion = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.denominacion

	class Meta:
		 db_table = 'Producto' # Nombre que tendrá la tabla que se creará en la base de datos en la Base de Datos


class RemitoVarios(models.Model):
	empresa = models.CharField(max_length=10,null=False, choices=Empresa_CHOICES,verbose_name="empresa", default="") 
	transporte = models.CharField(max_length=10,null=False, choices=TransporteRemito_CHOICES,verbose_name="transporte", default="") 
	destinatario = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True)
	producto = models.CharField(max_length=100,null=False, verbose_name="producto", default="") 
	lugarEntrega = models.CharField(max_length=100,null=False, verbose_name="lugarEntrega", default="") 
	IVA = models.CharField(max_length=5,null=False, choices=IVA_CHOICES, verbose_name="IVA", default="") 
	cantidad = models.DecimalField(null=True, verbose_name="cantidad", default="1", max_digits=30,decimal_places=2)
	unidad =  models.CharField(max_length=10,null=False, choices=Unidad_CHOICES,verbose_name="unidad", default="") 
	numero = models.IntegerField(null=True, verbose_name="numero", default="1")
	chofer = models.ForeignKey(Chofer, on_delete=models.CASCADE, null=True)
	remolque = models.ForeignKey(Remolque, on_delete=models.CASCADE, null=True)
	camion = models.ForeignKey(Camion, on_delete=models.CASCADE, null=True)
	rancho = models.BooleanField(default = False)
	observacion = models.CharField(max_length=100,null=True, verbose_name="observacion", default="") 
	fecha =  models.DateTimeField(default=timezone.now)

	class Meta:
		db_table = 'RemitoVarios' # Nombre que tendrá la tabla que se creará en la base de datos en la Base de Datos

	
class Rancho(models.Model):
    
	barco = models.ForeignKey(Barco, on_delete=models.CASCADE)
	puerto = models.ForeignKey(Puerto, on_delete=models.CASCADE)
	fechaCarga = models.DateTimeField(default=timezone.now)
	combustible = models.ForeignKey(Combustible, on_delete=models.CASCADE)
	litros = models.IntegerField(verbose_name="litros", default="1" )
	empresa = models.CharField(max_length=10,null=False, choices=Empresa_CHOICES,verbose_name="empresa", default="") 
	origenMercaderia = models.CharField(max_length=20,verbose_name="OrigenMercaderia", default="Neuquen") 
	densidad = models.DecimalField(max_digits=10, decimal_places=4,null=True, verbose_name="densidad", default="0.810")
	azufre = models.IntegerField(verbose_name="azufre", default="300" )
	precio =models.DecimalField(max_digits=20, decimal_places=2,null=True, verbose_name="precio" )
	impuestos =models.DecimalField(max_digits=20, decimal_places=2,null=True, verbose_name="impuestos" )
	emailEnviado = models.BooleanField()
	
	class Meta:
		db_table = 'Rancho' # Nombre que tendrá la tabla que se creará en la base de datos en la Base de Datos




