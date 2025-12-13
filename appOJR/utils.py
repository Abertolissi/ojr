# utils.py
import csv
from datetime import datetime
from io import StringIO
from .models import Camion, Transporte

def actualizarCamionesDesdeCsv(file):
    # Poner habilitadoAFIP en False para todos los camiones
    Camion.objects.all().update(habilitadoAFIP=False)
    
    file_data = file.read().decode('utf-8')
    csv_data = csv.reader(StringIO(file_data), delimiter=';')

    # Salto las primeras dos filas
    for _ in range(2): 
        next(csv_data, None)

    hoy = datetime.now().date()
    
    for row in csv_data:
        cuit, razonSocial, seccion, vigenciaDesde, vigenciaHasta, fechaInhabilitacion, patente, nombre,anexo,estado, nada  = row  # Ajusta según el orden de tus columnas

        vigenciaDesde = datetime.strptime(vigenciaDesde, '%d/%m/%Y').date()
        vigenciaHasta = datetime.strptime(vigenciaHasta, '%d/%m/%Y').date()
        # Filtrar por seccion
        if seccion != '3.2' and vigenciaDesde <= hoy <= vigenciaHasta: 
            continue

        # Buscar el transporte por CUIT
        try:
            transporte = Transporte.objects.get(cuit=cuit)
        except Transporte.DoesNotExist:
            print(f"Transporte con CUIT {cuit} no encontrado. Saltando...")
            continue

        patente = patente.upper()

        # Actualizar el camion si existe
        updated = Camion.objects.filter(patente=patente.upper()).update(
            habilitadoAFIP=True
        )

        if not updated:
            print(f"Camión con patente {patente} no encontrado. Saltando...")

