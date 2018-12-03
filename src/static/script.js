$(document).ready( function () {
    var trigger = null;

    var table = $('#datatable').DataTable({
        "ajax": {
            "url": "api/datatable?limit=1000",
            "error": function (data) {
                clearInterval(trigger);
            }
        },
        "order": [[ 0, "desc" ]]
     });

    trigger = setInterval( function () {
        table.ajax.reload( null, false);
    }, 1000 );
});

function submit_url() {
    if ($("#url_input_box").val() != "") {
        $.ajax({
            url: 'api/list',
            type: 'post',
            data: JSON.stringify({url: $("#url_input_box").val()}),
            contentType: 'application/json',
            dataType: 'json',
            success: function (data) {
                console.log(data);
            }
        });
    }
}
