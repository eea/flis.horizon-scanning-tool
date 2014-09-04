$(function () {
    $('.launch-modal').on('click', function () {
        var url = $(this).data('action');
        var title = $(this).data('title');
        $.ajax({
            type: "GET",
            url: url,
            success: function (data) {
                $('.modal-body').html(data);
                $('h4.modal-title').html(title)
                $('#add-modal-submit').data('action', url)
            },
            error: function (data) {
                alert('Error launching the modal')
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
                alert('Error saving the data')
            }
        });
    });
});
