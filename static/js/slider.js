let sliderImage = document.querySelectorAll('.slider-image')
let arrowLeft = document.querySelector('.previous')
let arrowRight = document.querySelector('.next')
let curren = 0;
let timeOut = 0;

function reset() {
    for (let i = 0; i < sliderImage.length; i++) {
        sliderImage[i].style.display = 'none';
    }
}

function startSlide() {
    reset();
    if (curren === sliderImage.length - 1) {
        curren = -1;
    }
    sliderImage[curren + 1].style.display = 'block';
    curren++;
    timeOut = setTimeout(startSlide, 5000)
}


function showLeft() {
    reset();
    sliderImage[curren - 1].style.display = 'block';
    curren--;
    window.clearTimeout(timeOut);
    timeOut = setTimeout(startSlide, 5000);
}

function showRight() {
    reset();
    sliderImage[curren + 1].style.display = 'block';
    curren++;
    window.clearTimeout(timeOut);
    timeOut = setTimeout(startSlide, 5000);
}

arrowLeft.addEventListener('click', function () {
    if (curren === 0) {
        curren = sliderImage.length;
    }
    showLeft();
})

arrowRight.addEventListener('click', function () {
    if (curren === sliderImage.length - 1) {
        curren = -1;
    }
    showRight();
})

startSlide();


