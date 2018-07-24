var modal = document.getElementById('modal');
var modal_content = document.getElementById('modal-content');

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

}

