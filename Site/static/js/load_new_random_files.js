$(function () {
    "use strict";

    $("#button_hour").click(function() {
        $(this).addClass('active').siblings().removeClass('active');
        $('#random_file_list').load(
            $('#random_file_list').attr('url') + "?ttl=hour"
        );
    });

    $("#button_day").click(function() {
        $(this).addClass('active').siblings().removeClass('active');
        $('#random_file_list').load(
            $('#random_file_list').attr('url') + "?ttl=day"
        );
    });

    $("#button_week").click(function() {
        $(this).addClass('active').siblings().removeClass('active');
        $('#random_file_list').load(
            $('#random_file_list').attr('url') + "?ttl=week"
        );
    });

    $("#button_all").click(function() {
        $(this).addClass('active').siblings().removeClass('active');
        $('#random_file_list').load(
            $('#random_file_list').attr('url') + "?ttl=all"
        );
    });
});