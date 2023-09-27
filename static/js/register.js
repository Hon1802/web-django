const btnLogin = document.querySelector('.js-btn-login')
const loginForm = document.querySelector('.js-login')
const loginContainer = document.querySelector('.js-login-container')

const btnForgot = document.querySelector('.js-forgot-pass')
const forgotForm = document.querySelector('.js-forgot')
const forgotContainer = document.querySelector('.js-forgot-container')
const btnComeback = document.querySelector('.js-come-back')

const closeIcon = document.querySelector('.js-close-icon')
const registerForm = document.querySelector('.js-register')
const registerContainer = document.querySelector('.js-register-container')
const btnNewAccount = document.querySelector('.js-new-account')

function showRegister() {
    registerForm.classList.add('open')
}

function closeRegister() {
    registerForm.classList.remove('open')
}

function showLogin() {
    loginForm.classList.add('open')
}

function closeLogin() {
    loginForm.classList.remove('open')
}

function showForgot() {
    forgotForm.classList.add('open')
}

function closeForgot() {
    forgotForm.classList.remove('open')
}

btnLogin.addEventListener('click', showLogin)
loginForm.addEventListener('click', closeLogin)
loginContainer.addEventListener('click', function (event) {
    event.stopPropagation()
})

btnForgot.addEventListener('click', closeLogin)
btnForgot.addEventListener('click', showForgot)
forgotForm.addEventListener('click', closeForgot)
btnComeback.addEventListener('click', closeForgot)
btnComeback.addEventListener('click', showLogin)
forgotContainer.addEventListener('click', function (event) {
    event.stopPropagation()
})

btnNewAccount.addEventListener('click', showRegister)
btnNewAccount.addEventListener('click', closeLogin)
closeIcon.addEventListener('click', closeRegister)
registerContainer.addEventListener('click', function (event) {
    event.stopPropagation()
})