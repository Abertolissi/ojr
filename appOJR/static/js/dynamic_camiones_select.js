(function($) {
    $(document).ready(function() {
        // Seleccionar el select del transporte y agregar el event listener para el cambio
        $('#id_remito_set-0-transporte').on('change', function() {
            var transporte_id = $(this).val();
            console.log('ID del transporte seleccionado: ' + transporte_id);

            if (transporte_id) {
                $.ajax({
                    url: '/appOJR/getCamiones/',  // Ajusta esta URL si es necesario
                    data: { 'transporte_id': transporte_id },
                    dataType: 'json',
                    success: function(data) {
                        console.log('Data (formatted): ' + JSON.stringify(data.camiones));
                        console.log('Data (object):', data.camiones);

                        // Seleccionar el select de camiones
                        var camionSelect = $('#id_remito_set-0-camion');
                        camionSelect.empty();  // Limpiar las opciones existentes

                        // Añadir una opción vacía al inicio
                        camionSelect.append($('<option></option>').attr('value', '').text('---------'));

                        // Poblar el select con las nuevas opciones
                        $.each(data.camiones, function(key, value) {
                            camionSelect.append($('<option></option>').attr('value', key).text(value));
                        });
                    },
                    error: function(xhr, status, error) {
                        console.error('Error:', error);
                    }
                });
            } else {
                console.log('No se ha seleccionado ningún transporte');
            }
        });
    });
})(django.jQuery || jQuery);
