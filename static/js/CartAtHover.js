// Thêm vào giỏ
var add_cart = document.getElementById('them-vao-gio')
var numProduct = 0;
let regex = /\d+/g;
add_cart.addEventListener('click', function (event) {

    var button = event.target;
    var product = button.parentElement.parentElement.parentElement.parentElement;
    var img = product.querySelector('.product-image').style.backgroundImage.slice(4, -1).replace(/"/g, "")
    var title = product.querySelector('.title-pro').innerHTML
    var price = product.querySelector('.price-product').innerHTML.match(regex).join('.') + " VND"
    numProduct++;
    addItemToCart(img, title, price, numProduct)
    updatecart()
})
// update cart
function updatecart() {
    let totalPriceCartItems = 0;
    let totalProductCart = 0;
    let price = 0;
    let quality = 0;
    let priceCartItems = document.querySelectorAll('.cart-item')
    let totalPrice = document.querySelector('.total-price');
    let totalProduct = document.querySelector('.total-product');
    console.log(priceCartItems)
    for (let i = 0; i < priceCartItems.length; i++) {
        totalPriceCartItems = parseFloat(priceCartItems[i].querySelector('.price-cart-item').innerHTML.match(regex).join(''))
        totalProductCart = parseInt(priceCartItems[i].querySelector('.num-cart-item').innerHTML.match(regex).join(''))
        totalPriceCartItems = totalProductCart * totalPriceCartItems;
        price += totalPriceCartItems
        quality += totalProductCart
    }
    price = price.toLocaleString('it-IT', {style: 'currency', currency: 'VND'})
    totalPrice.innerHTML = price;

    totalProduct.innerHTML = "Tổng tiền " + quality + " sản phẩm"
}


function addItemToCart(img, title, price, numProduct) {
    console.log(numProduct)
    var cartRow = document.createElement('div')
    let count = 0;
    // let quality = 1;
    var cartItems = document.querySelector('.cover-cart-item')
    var cart_items = cartItems.querySelectorAll('.cart-item')
    if (numProduct >= 2) {
        for (let i = 0; i < cart_items.length; i++) {
            if (cart_items[i].getElementsByClassName('infor-cart-item')[0].innerHTML == title) {
                numProduct = 1;
                let quality = cart_items[i].getElementsByClassName('num-cart-item')[0].innerHTML.match(regex).join('')
                cart_items[i].getElementsByClassName('num-cart-item')[0].innerHTML = "Số lượng: " + (parseInt(quality) + 1);
                count++
            } else {
                count = 0;
                numProduct = 1;
            }
        }
    }
    if (count <= 0) {
        var itemProduct = `<div class="cart-item">
            <div class="img-cart-item" style="background-image: url(${img})">

            </div>
            <div class="details-cart-item">
                <div class="infor-cart-item">${title}</div>
                <div class="num-cart-item">Số lượng: ${numProduct}</div>
                <div class="price-cart-item">${price}</div>
            </div>
        </div>`
        cartRow.innerHTML = itemProduct
        cartItems.append(cartRow)
    }
}


