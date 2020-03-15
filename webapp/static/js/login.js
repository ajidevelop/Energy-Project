let modal = document.getElementById('modal');
let login_form = document.getElementById('login-form');
let create_account_form = document.getElementById('create-account-form');
let navbar_checkbox = document.getElementById('nav-toggle');
let verification_form = document.getElementById('verification-form');
let resend_verification_form = document.getElementById('resend-verification-form');
let temp_message = document.getElementById('tmp-message');

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

function change_modal_form(form, verify=false) {
    modal.style.display='block';
    login_form.style.display='none';
    form.style.display='block';
    if (form === temp_message) {
        setTimeout(function () {
            form.style.display = 'none';
            if (verify) {
                verification_form.style.display='block';
            } else {
                login_form.style.display = 'block';
            }
        }, 3000);
    }
}

function go_back(old_form, new_form=login_form) {
    new_form.style.display='block';
    old_form.style.display = 'none';
    if (new_form === login_form) {
        new_form.classList.remove('animate')
    }
}
