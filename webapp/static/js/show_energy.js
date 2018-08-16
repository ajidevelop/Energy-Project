let control_checkboxes = document.getElementById('control');
let tbody = document.getElementById('tbody');
let tr = tbody.getElementsByTagName('tr');
let cancel_button = document.getElementById('cancel');
let update_button = document.getElementById('update');
let d_usage = document.getElementsByName('usage_d');
let dates = document.getElementsByName('box-date');
let reloader = document.getElementById('reloader');
window.onload = function() {
    let applybtn = document.getElementsByClassName('applyBtn btn btn-sm btn-primary');
    applybtn[0].setAttribute('form', 'reloader');
    applybtn[0].setAttribute('type', 'submit');
};

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

function change_view_range(start_date, end_date) {
    let s_date = document.createElement('input');
    s_date.setAttribute('type', 'hidden');
    s_date.setAttribute('name', 'start-date');
    s_date.setAttribute('value', start_date);
    let e_date = document.createElement('input');
    e_date.setAttribute('type', 'hidden');
    e_date.setAttribute('name', 'end-date');
    e_date.setAttribute('value', end_date);
    let entries = document.createElement('input');
    entries.setAttribute('type', 'hidden');
    entries.setAttribute('name', 'entries');
    entries.setAttribute('value', 'none');
    reloader.appendChild(s_date);
    reloader.appendChild(entries);
    reloader.appendChild(e_date);
}