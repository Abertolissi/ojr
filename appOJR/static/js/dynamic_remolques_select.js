(function($) {
    $(document).ready(function() {
        // Seleccionar el select del transporte y agregar el event listener para el cambio
        $('#id_remito_set-0-transporte').on('change', function() {
            var transporte_id = $(this).val();
            
            if (transporte_id) {
                $.ajax({
                    url: '/appOJR/getRemolques/',  // Ajusta esta URL si es necesario
                    data: { 'transporte_id': transporte_id },
                    dataType: 'json',
                    success: function(data) {
                        console.log('Data (formatted): ' + JSON.stringify(data.remolques));
                        console.log('Data (object):', data.remolques);

                        // Seleccionar el select de remolques
                        var remolqueSelect = $('#id_remito_set-0-remolque');
                        remolqueSelect.empty();  // Limpiar las opciones existentes

                        // Añadir una opción vacía al inicio
                        remolqueSelect.append($('<option></option>').attr('value', '').text('---------'));

                        // Poblar el select con las nuevas opciones
                        $.each(data.remolques, function(key, value) {
                            remolqueSelect.append($('<option></option>').attr('value', key).text(value));
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
