let btnAddCart = document.getElementById('them-vao-gio');
let iconCart = document.getElementById('icon-cart')
var countCart = 0

btnAddCart.onclick = function () {
    countCart++;
    iconCart.innerHTML = countCart;
    iconCart.style.display = 'flex'
}
