viewImageProduct()

function viewImageProduct() {
    let imageItems = document.querySelectorAll('.details-image-item')
    let btnClose = document.getElementById('close-view-image-product')
    let viewImageProduct = document.getElementById('view-image-product')
    let bigImage = document.querySelector('.big-image-view-product')
    let itemImage = document.querySelectorAll('.item-image-view-product')


    for (let i = 0; i < itemImage.length; i++) {
        itemImage[i].addEventListener('click', function () {
            if (window.getComputedStyle(itemImage[i]).getPropertyValue('opacity') == 0.3) {
                for (let j = 0; j < itemImage.length; j++) {
                    if (window.getComputedStyle(itemImage[j]).getPropertyValue('opacity') == 1){
                        itemImage[j].style.opacity = '0.3';
                    }
                }
                itemImage[i].style.opacity = '1';
            }
            bigImage.style.backgroundImage = itemImage[i].style.backgroundImage;
        })
    }

    for (let i = 0; i < imageItems.length; i++) {
        imageItems[i].addEventListener('click', function () {
            viewImageProduct.style.display = 'flex'
            bigImage.style.backgroundImage = imageItems[i].style.backgroundImage;
            itemImage[i].style.opacity = '1';
        })
        btnClose.addEventListener('click', function () {
            viewImageProduct.style.display = 'none'
            itemImage[i].style.opacity = '0.3';
        })
    }
}