# Logout

<script src='./app/tools.js'></script>

<script>


function logout() {
    tools.logout();
    location.replace(location.hash ? location.hash.slice(1) : "./");
}

window.addEventListener('load', logout);
</script>

Logging out ...
