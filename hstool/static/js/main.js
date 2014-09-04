$(function () {
    $('#add-modal').on('click', function () {
        var url = $(this).data('action');
        $.ajax({
            type: "GET",
            url: url,
            success: function (data) {
                $('.modal-body').html(data);
            },
            error: function (data) {
                alert(JSON.stringify(data))

                alert('Error launching the modal');
            }
        })
    });

    $('#add-modal-submit').on('click', function () {
        var url = $(this).data('action');
        $.ajax({
            type: "POST",
            url: url,
            data: $('#add-form').serialize(),
            success: function (data) {
                $('.modal-body').html(data);
            },
            error: function (data) {
                alert(JSON.stringify(data))
            }
        });
    });
});
