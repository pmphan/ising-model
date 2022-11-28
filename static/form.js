var socket = io("/calculation");
var cached;

$(document).ready(() => {
    // On submitting first form
    $('#plot-form').submit(function(e) {
        e.preventDefault();
        cached = $(this).serializeArray();
        $.ajax({
            url: $(this).attr('action'),
            type: "POST",
            data: $(this).serialize(),
            success: (data) => {
                cached.push({name: "array", value: data["array"]})
                $("#plot-image").attr("src", `data:image/png;base64,${data["plot"]}`);
                $("#calculation-frame").html('');
                $("#calculation-button").removeAttr('disabled');
            },
            error: onError
        });
    });

    // On submitting second form
    $("#calculation-form").submit(function(e) {
        e.preventDefault();
        $("#calculation-frame").html('');
        $(':button').attr('disabled', true);
        $('#stop-anim-button').removeAttr('disabled');
        socket.emit("calculate", cached.concat($(this).serializeArray()));
    });

    // On receiving calculation result
    socket.on('calculating', (data) => {
        let i = data['i']+1;
        if (i <= 0) i = 'final';
        let src = `data:image/png;base64,${data['plot']}`;

        // Add animation
        $("#calculation-window").fadeOut(0, function () {
            $(this).attr('src', src);
            $(this).fadeIn(0);
        });

        // Add preview images
        $(`
            <div style="width: 10%;">
               <img class="preview-image figure-img img-fluid" src="${src}">
               <figcaption class="figure-caption text-center">Step ${i}</figcaption>
            </div>
        `).appendTo('#calculation-frame');
    });

    // On finishing calculation
    socket.on('calculated', () => {
        $(':button').removeAttr("disabled");
        $('#stop-anim-button').attr('disabled', true).html('Stop');
        makeClickablePreview();
    });
});

function onError(jXHR, textStatus, errorThrown) {
    alert(errorThrown);
}

function makeClickablePreview() {
    $(".preview-image").click(function () {
        $("#calculation-window").attr('src', $(this).attr('src'));
    }).css('cursor', 'pointer');
}

function stopAnimation() {
    socket.emit("stop");
    $("#stop-anim-button").html("Stopping...");
}
