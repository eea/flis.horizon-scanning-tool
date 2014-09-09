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
        var form = $('#add-form');
        var url = $(this).data('action');
        var formdata = false;
        if (window.FormData){
            formdata = new FormData(form[0]);
        }
        $.ajax({
            url: url,
            data: formdata ? formdata : form.serialize(),
            cache: false,
            contentType: false,
            processData: false,
            type: "POST",
            success: function (data) {
                $('.modal-body').html(data);
            },
            error: function (data) {
                alert('Error saving the data')
            }
        });
    });
});
