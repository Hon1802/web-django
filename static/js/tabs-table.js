var buttons = document.getElementsByClassName('tablink');
var contents = document.getElementsByClassName('table-tabs');
function showContent(id){
    for (var i = 0; i < contents.length; i++) {
        contents[i].style.display = 'none';
    }
    var content = document.getElementById(id);
    content.style.display = 'flex';
}
for (var i = 0; i < buttons.length; i++) {
    let num = i;
    buttons[i].addEventListener("click", function(){
        var id = contents[num].id;
        for (var i = 0; i < buttons.length; i++) {
            buttons[i].classList.remove("active");
        }
        this.className += " active";
        showContent(id);
    });
}
showContent('table-dell');