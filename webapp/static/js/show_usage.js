let reloader = document.getElementById('reloader');

function change_view(d_entries) {
    let invisiform = document.createElement('input');
    invisiform.setAttribute('type', 'hidden');
    invisiform.setAttribute('name', 'd_entries');
    invisiform.setAttribute('value', d_entries);
    let entries = document.createElement('input');
    entries.setAttribute('type', 'hidden');
    entries.setAttribute('name', 'entries');
    entries.setAttribute('value', 'none');
    reloader.appendChild(invisiform);
    reloader.appendChild(entries)
}