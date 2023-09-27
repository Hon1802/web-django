let mybutton = document.getElementById('myBtn');

var id_button = '#myBtn';

// Kéo xuống khoảng cách 220px thì xuất hiện button
var offset = 500;

// THời gian di trượt là 0.5 giây
var duration = 500;

// Thêm vào sự kiện scroll của window, nghĩa là lúc trượt sẽ
// kiểm tra sự ẩn hiện của button
jQuery(window).scroll(function() {
    if (jQuery(this).scrollTop() > offset) {
        jQuery(id_button).fadeIn(duration);
    } else {
        jQuery(id_button).fadeOut(duration);
    }
});
mybutton.addEventListener('click', () => {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
});