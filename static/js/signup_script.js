function returnSignupInfo() {
    var email = document.getElementById("email").value;
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var confPassword = document.getElementById("confPassword").value;
    console.log({ email, username, password, confPassword });
}