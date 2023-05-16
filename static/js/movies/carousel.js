$(document).ready(function(){
  $('.movie-slide-black').slick({
    infinite: false,
    slidesToShow: 5,
    slidesToScroll: 5,
    prevArrow : "<button type='button' class='slick-prev slick-index-prev'>Previous</button>",    
    nextArrow : "<button type='button' class='slick-next slick-index-next'>Next</button>",
  });
})

$(document).ready(function(){
  $('.movie-slide').slick({
    infinite: false,
    slidesToShow: 5,
    slidesToScroll: 5,
    prevArrow : "<button type='button' class='slick-prev'>Previous</button>",    
    nextArrow : "<button type='button' class='slick-next'>Next</button>",
  });
})

$(document).ready(function(){
  $('.collection-list').slick({
    infinite: false,
    slidesToShow: 4,
    slidesToScroll: 4,
    prevArrow : "<button type='button' class='slick-prev slick-index-prev'>Previous</button>",    
    nextArrow : "<button type='button' class='slick-next slick-index-next'>Next</button>",
  });
})