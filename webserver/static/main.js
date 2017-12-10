function readURL(input) {
            if (input.files && input.files[0]) {
                var reader = new FileReader();

                reader.onload = function (e) {
                    $('#preview_image')
                        .attr('src', e.target.result);
                };

                reader.readAsDataURL(input.files[0]);
                $('#preview_image').show();
            }
        }


$(function () {
    $('#upload-file-btn').click(function () {
        var form_data = new FormData($('#upload-file')[0]);
        $image = $('#loading_image');
        $results = $('#results');
        $btn = $('#upload-file-btn');

        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            beforeSend: function (data) {
                $btn.prop("disabled",true);
                $btn.html("Loading...");
                $image.show();
                $results.html("");
            },
            error: function (data) {
                $btn.prop("disabled",false);
                $btn.html("Upload");
                $image.hide();
                $results.html("<li>Error during inference, try again</li>");

            },
            success: function (data) {
                $btn.prop("disabled",false);
                $btn.html("Upload");
                $image.hide();
                if (data[0] == "error") {
                    $results.html("<li>Error during inference, try again</li>");
                } else {
                    $results.html("");
                    data.forEach(function (element) {
                        $results.append("<li>" + element + "</li>")
                    })
                }
            },
        });
    });


});