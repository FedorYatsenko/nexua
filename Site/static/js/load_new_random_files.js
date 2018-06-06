$(function () {
    "use strict";

    $(".button_filter").click(function() {
        if (!$(this).hasClass('active')) {
            $(this).addClass('active').siblings().removeClass('active');
            $('#random_file_list').load(
                $('#random_file_list').attr('url') + "?ttl=" + $(this).attr('name')
            );
        }
    });

    $("#button_new").click(function() {
        $('#random_file_list').load(
                $('#random_file_list').attr('url') + "?ttl=" + $("#filters").children(".active").attr("name")
            );
    });
});