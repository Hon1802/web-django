let productImage = document.getElementById('product-image')
let originImage = productImage.style.backgroundImage;
let imageItems = document.querySelectorAll('.details-image-item')
for (let i = 0; i < imageItems.length; i++) {
    imageItems[i].addEventListener("mouseover", function () {
        productImage.style.backgroundImage = imageItems[i].style.backgroundImage;
    })
}