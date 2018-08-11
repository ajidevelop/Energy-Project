let reloader = document.getElementById('reloader');
let all_time = document.getElementById('all-time');
let month_one = document.getElementById('month-1');
let month_two = document.getElementById('month-2');
let month_three = document.getElementById('month-3');
let month_six = document.getElementById('month-6');
let month_twelve = document.getElementById('month-12');

function change_view(d_entries, w_entries) {
    let invisiform = document.createElement('input');
    invisiform.setAttribute('type', 'hidden');
    invisiform.setAttribute('name', 'd_entries');
    invisiform.setAttribute('value', d_entries);
    let w_entries_input = document.createElement('input');
    w_entries_input.setAttribute('type', 'hidden');
    w_entries_input.setAttribute('name', 'w_entries');
    w_entries_input.setAttribute('value', w_entries);
    let entries = document.createElement('input');
    entries.setAttribute('type', 'hidden');
    entries.setAttribute('name', 'entries');
    entries.setAttribute('value', 'none');
    reloader.appendChild(invisiform);
    reloader.appendChild(entries);
    reloader.appendChild(w_entries_input);
}

function button_hide(button_hide, button_show) {
    button_hide.style.display = 'none';
    button_show.style.display = ''
}