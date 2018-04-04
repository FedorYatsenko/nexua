$(function () {
    "use strict";

    $(".button_filter").click(function() {
        $(this).addClass('active').siblings().removeClass('active');
        $('#random_file_list').load(
            $('#random_file_list').attr('url') + "?ttl=" + $(this).attr('name')
        );
    });
});