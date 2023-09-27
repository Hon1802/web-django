let allItems = document.querySelectorAll('.hover-all-product');
let countAllProduct = 0;
// let test = document.querySelectorAll('.dots-slick button')
// console.log(test)
for (let i = 0; i < allItems.length; i++) {
    countAllProduct++;
}
if (countAllProduct <= 30) {
    $('.all-product-cover').slick('unslick');
} else {
    for (let i = 0; i < allItems.length; i++) {
        allItems[i].style.maxWidth = 'inherit'
    }
    $('.all-product-cover').slick({
        dots: true,
        infinite: false,
        speed: 1000,
        slidesToShow: 6,
        slidesToScroll: 6,
        rows: 6,
        arrows : false,
        // variableWidth: true,
        appendDots: $('.dots-slick'),
        responsive: [
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
        prevArrow: "<button type='button' class='slick-prev pull-left'><i class='fa fa-angle-left' aria-hidden='true'></i></button>",
        nextArrow: "<button type='button' class='slick-next pull-right'><i class='fa fa-angle-right' aria-hidden='true'></i></button>"
    });

    $(window).resize(function (e) {
        if (window.innerWidth < 740) {
            if (!$('.all-product-cover').hasClass('slick-initialized')) {
                $('.all-product-cover').slick({
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    prevArrow: "<button type='button' class='slick-prev pull-left'><i class='fa fa-angle-left' aria-hidden='true'></i></button>",
                    nextArrow: "<button type='button' class='slick-next pull-right'><i class='fa fa-angle-right' aria-hidden='true'></i></button>"
                });
            }
        } else {
            if ($('.all-product-cover').hasClass('slick-initialized')) {
                $('.all-product-cover').slick('unslick');
            }
        }
    });
}