// Connexion.js
// Version: 1.0 - 6666/66/66
function connect() {
    var users = ['admin', 'root', 'superuser'];
    // #RockYou.txt ne pourra jamais m'avoir je pense
    var passwords = ['ODEwMzY0NWQwZDg5Y2NhNDVmYTkwNmQyOTAzMTc4ZTRlZDBlZDI5NA==', 'OTkwZGRiOWIwYjdiNzZhMGYyMWFhMDhmNTQ5NTkwNDY5ZjJiZjA3ZA==', 'ZmNmMDk5YWEwZWQ1OTE5Yzk0MzQyZjA2MzU1NTllMjI4ZmNkOTRhZg=='];
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    if (username === 'propos') {
        alert('Propos a pas de compte, il est trop fort pour ça');
        return;
    }

    if (users.indexOf(username) !== -1) {
        var index = users.indexOf(username);
        var hash = passwords[index];
        var true_hash = atob(hash);
        var hash2 = sha1(password);
        if (true_hash === hash2) {
            window.location.href = password + '.html';
        }
        else {
            alert('Invalid username or password');
        }
    }
    else {
        alert('Invalid username or password');
    }
}

function attach() {
    document.getElementById('connect').addEventListener('click', connect);
}

username = document.getElementById('username');
password = document.getElementById('password');

if (username === "propos") {
    alert('Propos a pas de compte, il est trop fort pour ça');

}
else {
    connect();
}

