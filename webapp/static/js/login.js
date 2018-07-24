let modal = document.getElementById('modal');
let modal_content = document.getElementById('modal-content');
let logon = document.getElementById('logon');
let create_account = document.getElementById('create-account');
let img = document.getElementById('sample-avatar');

window.onclick = function (event) {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
};

function load() {
    modal.style.display='block';
}

function reload() {
    modal.style.display='block';
    modal_content.classList.add('wrongpsw-animate')
}

function new_user() {
    logon.style.display='none';
    create_account.style.display='block';
    img.style.display='none'
}

function go_back() {
    logon.style.display='block';
    create_account.style.display='none';
    img.style.display='block'
}

