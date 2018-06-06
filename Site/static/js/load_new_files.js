$(function () {
    "use strict";

    var index = 2;

    $(window).scroll(function(){
        if($(window).scrollTop() + $(window).height() + 250 >= $(document).height() && index < $('#last_files').attr('files_count')){
            $('#last_files').append('<div id="files' + index + '">');
            $('#files' + index).load(
                $('#last_files').attr('url') + "?index=" + index
            );
            index += 2;
        }
    });
});