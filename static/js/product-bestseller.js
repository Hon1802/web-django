$('.product-bestseller').slick({
    // dots: true,
    // infinite: true,
    speed: 1000,
    slidesToShow: 5,
    slidesToScroll: 3,
    autoplay: true,
    autoplaySpeed: 2000,
    responsive: [{
        breakpoint: 1024,
        settings: {
            slidesToShow: 3,
            slidesToScroll: 3,
            // infinite: true,
            dots: true
        }
    },
        {
            breakpoint: 600,
            settings: {
                slidesToShow: 2,
                slidesToScroll: 2
            }
        },
        {
            breakpoint: 480,
            settings: {
                slidesToShow: 2,
                slidesToScroll: 1
            }
        }
    ],
    prevArrow:"<button type='button' class='slick-prev pull-left'><i class='fa fa-angle-left' aria-hidden='true'></i></button>",
    nextArrow:"<button type='button' class='slick-next pull-right'><i class='fa fa-angle-right' aria-hidden='true'></i></button>"
});

$(window).resize(function(e){
    if(window.innerWidth < 740) {
        if(!$('.outstand-product').hasClass('slick-initialized')){
            $('.outstand-product').slick({
                slidesToShow: 1,
                slidesToScroll: 1,
                prevArrow:"<button type='button' class='slick-prev pull-left'><i class='fa fa-angle-left' aria-hidden='true'></i></button>",
                nextArrow:"<button type='button' class='slick-next pull-right'><i class='fa fa-angle-right' aria-hidden='true'></i></button>"
            });
        }
    }
    else{
        if($('.outstand-product').hasClass('slick-initialized')){
            $('.outstand-product').slick('unslick');
        }
    }
});