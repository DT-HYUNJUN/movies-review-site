$(document).ready(function(){
  $('.profile-review-slide').slick({
    infinite: false,
    slidesToShow: 2,
    slidesToScroll: 2,
    prevArrow : "<button type='button' class='slick-prev'>Previous</button>",    
    nextArrow : "<button type='button' class='slick-next'>Next</button>",
  });
})

$(document).ready(function(){
  $('.collection-list').slick({
    infinite: false,
    slidesToShow: 4,
    slidesToScroll: 4,
    prevArrow : "<button type='button' class='slick-prev'>Previous</button>",    
    nextArrow : "<button type='button' class='slick-next'>Next</button>",
  });
})