let control_checkboxes = document.getElementById('control');
let search_input = document.getElementById('search').value;
let tbody = document.getElementById('tbody');
let tr = tbody.getElementsByTagName('tr');


let today = new Date();
let dd = today.getDate();
let mm = today.getMonth()+1; //January is 0!
let yyyy = today.getFullYear();
if(dd<10){
        dd='0'+dd
    }
    if(mm<10){
        mm='0'+mm
    }

function check_uncheck() {
    if (control_checkboxes.checked===true) {
        let inputs = document.getElementsByTagName('input');
        for (let i = 0; i < inputs.length; i++) {
            if (inputs[i].type === 'checkbox') {
                console.log(inputs[i]);
                if (inputs[i].style.display === '') {
                    console.log('none');
                    inputs[i].checked = true
                }
            }
        }
    } else if (control_checkboxes.checked===false) {
        let inputs = document.getElementsByTagName('input');
        for (let i = 0; i < inputs.length; i++) {
            if (inputs[i].type === 'checkbox') {
                console.log('works');
                inputs[i].checked = false
            }
        }
    }
}


today = yyyy+'-'+mm+'-'+dd;

function search() {
    for (let i = 0; i < tr.length; i++) {
        let td = tr[i].getElementsByClassName('dates')[0];
        let td_checkbox = tr[i].getElementsByTagName("input")[0];
        console.log(document.getElementById('search').value);
        console.log(search_input);
        if (td.innerHTML.indexOf(document.getElementById('search').value) > -1) {
            tr[i].style.display='';
            td_checkbox.style.display='';
        } else {
            tr[i].style.display='none';
            td_checkbox.style.display = 'none'
        }
    }
}