function returnLoginInfo() {
    const email = document.getElementById('email').value
    const password = document.getElementById('password').value

    const request = new Request("http://127.0.0.1:5000/api/authenticate", {
        "method":"POST",
        "body":{
            "email":email,
            "password":password
        }
    });

    console.log(request)
    fetch(request);
}