let modal = document.getElementById('modal');
let login_form = document.getElementById('login-form');
let create_account_form = document.getElementById('create-account-form');
let navbar_checkbox = document.getElementById('nav-toggle');

window.onclick = function (event) {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
};

function load() {
    modal.style.display='block';
    navbar_checkbox.checked=false;
}

function reload(form) {
    modal.style.display='block';
    if (form !== login_form) {
        login_form.style.display = 'none';
        form.style.display = 'block';
        form.classList.add('wrongpsw-animate');
    } else if (form === login_form) {
        login_form.classList.add('wrongpsw-animate')
    }

}

function new_user() {
    login_form.style.display='none';
    create_account_form.style.display='block';
}

function go_back(form) {
    login_form.style.display='block';
    form.style.display = 'none';
    login_form.classList.remove('animate')
}

