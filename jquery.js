    // Función para agregar una nueva fila de remito
    function agregarRemito() {
        var table = document.getElementById("remitosTable");
        var row = table.insertRow();
        var cell1 = row.insertCell();
        var cell2 = row.insertCell();
        var cell3 = row.insertCell();
        var cell4 = row.insertCell();
        var cell5 = row.insertCell();
        var cell6 = row.insertCell();
        var cell7 = row.insertCell();
        var cell8 = row.insertCell();
        cell1.innerHTML = '<input type="text" name="remito_numero[]" class="form-control">';
        cell2.innerHTML = '<input type="text" name="remito_chofer[]" class="form-control">';
        cell3.innerHTML = '<input type="text" name="remito_camion[]" class="form-control">';
        cell4.innerHTML = '<input type="text" name="remito_remolque[]" class="form-control">';
        cell5.innerHTML = '<input type="number" name="remito_cantidad_m2_barco[]" class="form-control">';
        cell6.innerHTML = '<input type="number" name="remito_cantidad_m2_deposito[]" class="form-control">';
        cell7.innerHTML = '<input type="number" name="remito_densidad[]" class="form-control">';
        cell8.innerHTML = '<input type="number" name="remito_temperatura[]" class="form-control">';
    }

    // Función para eliminar la última fila de remito
    function eliminarRemito() {
        var table = document.getElementById("remitosTable");
        var rowCount = table.rows.length;
        if (rowCount > 1) {
            table.deleteRow(rowCount - 1);
        }
    }
