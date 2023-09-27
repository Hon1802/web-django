let header = document.getElementById('header')
let mobileMenu = document.getElementById('mobile-menu')
let headerList = document.getElementById('header-list-id')
let menuItems = document.querySelectorAll('#header .header_list .header_sub-list a')


let bool = true
let count = 0
mobileMenu.onclick = function () {
    count++
    if (bool == true && count > 0) {
        headerList.style.display = 'block';
        bool = false;
    } else {
        headerList.style.display = 'none';
        bool = true;
    }
}

$(window).resize(function (e) {
    if ($(document).width() > 740) {
        headerList.style.display = 'block';
    } else {
        headerList.style.display = 'none';
    }
});
// $(window).resize(function (e) {
        for (let i = 0; i < menuItems.length; i++) {
            let menuItem = menuItems[i];

            menuItem.onclick = function () {
                if ($(document).width() < 740) {
                headerList.style.display = 'none';
                bool = true;
                count = 0;
            }
        }
    }
// })