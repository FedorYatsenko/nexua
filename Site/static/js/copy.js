$(function () {
    "use strict";

    $("#copy_button").on("click", function copy_button_click() {
        var $temp = $("<input>");
        $("body").append($temp);
        $temp.val($("#link").text()).select();
        document.execCommand("copy");
        $temp.remove();

        $("#buttons").append("<div class=\"alert alert-warning alert-dismissible fade show mt-2 \" role=\"alert\">" +
            "  Link was successfuly copied" +
            "  <button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\">" +
            "  <span aria-hidden=\"true\">&times;</span>" +
            "  </button>" +
            "</div>");
    })
});