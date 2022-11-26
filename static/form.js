import { io } from "https://cdn.socket.io/4.3.2/socket.io.esm.min.js";

var socket = io("/calculation");
var cached;

$(document).ready(() => {
    $('#form-plot').submit(function(e) {
        e.preventDefault();
        cached = $(this).serializeArray();
        $.ajax({
            url: $(this).attr('action'),
            type: "POST",
            data: $(this).serialize(),
            success: (data) => {
                cached.push({name: "array", value: data["array"]})
                $("#form-image").attr("src", `data:image/png;base64,${data["plot"]}`);
                $("#calculation-result").html('');
                $('#calculate-image').removeAttr('disabled').html("Calculate");
            },
            error: onError
        });
    });

    $("#form-calculate").submit(function(e) {
        e.preventDefault();
        $("#calculation-result").html('');
        $('#draw-plot').attr('disabled', true);
        $('#calculate-image').attr('disabled', true).html("Calculating");
        socket.emit("calculate", cached.concat($(this).serializeArray()));
    });

    socket.on('calculating', (data) => {
        var i = data['i']+1;
        if (i <= 0) i = 'final';
        var plot = data['plot'];
        $(`<div class="col-xs-6"><img class="figure-img img-fluid" src="data:image/png;base64,${plot}"><figcaption class="figure-caption text-center">Step ${i}</figcaption></div>`).appendTo('#calculation-result');
    });

    socket.on('calculated', () => {
        $('#calculate-image').html("Recalculate").removeAttr("disabled");
        $('#draw-plot').removeAttr('disabled');
    });
});

function onError(jXHR, textStatus, errorThrown) {
    alert(errorThrown);
}
