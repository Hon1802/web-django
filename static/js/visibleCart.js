let cart = document.querySelector('#header li a[href*="cart.html"]')
let hoverCart = document.getElementById('cart-hover')
if ($(window).width() > 1024) {
    $(function () {
        $(cart).hover(function () {
            $(hoverCart).css('display', 'flex');
        });
    });

    $(function () {
        $('#li-cart').hover(function () {
            $(hoverCart).css('display', 'flex');
        }, function () {
            $(hoverCart).css('display', 'none');
        });
    });

    $(function () {
        $('#cart-hover').hover(function () {
            $(hoverCart).css('display', 'flex');
        }, function () {
            $(hoverCart).css('display', 'none');
        });
    });
}