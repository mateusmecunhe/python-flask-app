let buttonMenu = document.querySelector('#nav-icon');
let menuOptions = document.querySelector('.menu-options');

buttonMenu.addEventListener('click', () => {
    menuOptions.classList.toggle('active');
    buttonMenu.classList.toggle('active');
})

menuOptions.addEventListener('click', () => {

    menuOptions.classList.remove('active');
    buttonMenu.classList.remove('active');
    btn.classList.toggle('open');

})


var btn = document.querySelector('#nav-icon');
btn.addEventListener('click', function() {
    this.classList.toggle('open');
})