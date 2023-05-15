$('#color-picker').spectrum({
  type: "color",
  change: function(color) {
    color.toHexString(); // #ff0000
    $(".banner").css("background-color", color.toHexString());
}

});

