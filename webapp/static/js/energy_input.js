let control_checkboxes = document.getElementById('control');
let tbody = document.getElementById('tbody');
let tr = tbody.getElementsByTagName('tr');
let cancel_button = document.getElementById('cancel');
let update_button = document.getElementById('update');
let d_usage = document.getElementsByName('usage_d');
let dates = document.getElementsByName('box-date');

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
                if (inputs[i].style.display === '') {
                    if (inputs[i] !== document.getElementById('nav-toggle')) {
                        inputs[i].checked = true
                    }
                }
            }
        }
    } else if (control_checkboxes.checked===false) {
        let inputs = document.getElementsByTagName('input');
        for (let i = 0; i < inputs.length; i++) {
            if (inputs[i].type === 'checkbox') {
                if (inputs[i] !== document.getElementById('nav-toggle')){
                    inputs[i].checked = false
                }
            }
        }
    }
}


today = yyyy+'-'+mm+'-'+dd;

function search() {
    for (let i = 0; i < tr.length; i++) {
        let td = tr[i].getElementsByClassName('dates')[0];
        let td_checkbox = tr[i].getElementsByTagName("input")[0];
        if (td.innerHTML.indexOf(document.getElementById('search').value) > -1) {
            tr[i].style.display='';
            td_checkbox.style.display='';
        } else {
            tr[i].style.display='none';
            td_checkbox.style.display = 'none'
        }
    }
}

function cancel() {
    for (let i = 0; i < d_usage.length; i++) {
        if (d_usage[i].value !== d_usage[i].defaultValue) {
            d_usage[i].value = d_usage[i].defaultValue
        }
    }
    cancel_button.style.display = 'none';
    update_button.style.display = 'none'
}

function update_table() {
    for (let i = 0; i < d_usage.length; i++) {
        if (d_usage[i].value !== d_usage[i].defaultValue) {
            let real_input = document.createElement('input');
            real_input.setAttribute('type', 'hidden');
            real_input.setAttribute('value', d_usage[i].value);
            real_input.setAttribute('name', 'd_usage');
            document.getElementById('update-table').appendChild(real_input);
            let real_date_input = document.createElement('input');
            real_date_input.setAttribute('type', 'hidden');
            real_date_input.setAttribute('value', dates[i].value);
            real_date_input.setAttribute('name', 'date-box');
            document.getElementById('update-table').appendChild(real_date_input);
        }
    }
}

function button_appear() {
    cancel_button.style.display = '';
    update_button.style.display = ''
}