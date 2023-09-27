let btnFilter = document.querySelectorAll('.filter-item')
let checked = document.querySelectorAll('.tick')
clickFilter()

function clickFilter() {
    for (let i = 0; i < btnFilter.length; i++) {
        btnFilter[i].addEventListener('click', function () {
            if ($(checked[i]).css('display') === 'block') {
                btnFilter[i].classList.remove("filter-class-add");
                checked[i].style.display = 'none';
            } else {
                btnFilter[i].classList.add("filter-class-add");
                checked[i].style.display = 'block';
            }
        })
    }
}

let checkedAnother = document.querySelectorAll('.tick-another')
let btnFilterAnother = document.querySelectorAll('.filter-item-another')
let inputFilter = document.querySelectorAll('.input-filter-product')
for (let i = 0; i < inputFilter.length; i++) {
    // let value = inputFilter[i].value;
    $(inputFilter[i]).bind('keyup paste', function () {
        // this.value = Number(this.value).toLocaleString('it-IT' )
        this.value = new Intl.NumberFormat().format(this.value.replaceAll(/[^0-9]/g, '')).replace(/^0+/, '')
        if(isNaN(this.value))
        document.querySelector('.btn-search-filter').style.display = 'block'
        // this.value = value.match(regex)
    });
}
clickFilterAnother()

function clickFilterAnother() {
    for (let i = 0; i < btnFilterAnother.length; i++) {
        btnFilterAnother[i].addEventListener('click', function () {
            if ($(checkedAnother[i]).css('display') === 'none') {
                for (let j = 0; j < btnFilterAnother.length; j++) {
                    if ($(checkedAnother[j]).css('display') === 'block') {
                        btnFilterAnother[j].classList.remove("filter-class-add");
                        checkedAnother[j].style.display = 'none';
                    }
                }
                btnFilterAnother[i].classList.add("filter-class-add");
                checkedAnother[i].style.display = 'block';
            } else {
                btnFilterAnother[i].classList.remove("filter-class-add");
                checkedAnother[i].style.display = 'none';
            }
        })
    }
}
