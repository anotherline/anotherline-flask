(function() {
  $(window).scroll(function() {
    var opacityVal;
    opacityVal = $(window).scrollTop() / 240;
    return $(".blur").css("opacity", opacityVal);
  });

}).call(this);