$(document).ready(function(){
  $('.review-slide').slick({
    infinite: true,
    slidesToShow: 2,
    slidesToScroll: 2,
    prevArrow : "<button type='button' class='slick-prev'>Previous</button>",    
    nextArrow : "<button type='button' class='slick-next'>Next</button>",
  });
})