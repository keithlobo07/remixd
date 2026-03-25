function returnLoginInfo(url) {
    const fd = new FormData(document.getElementById('loginForm'));

    const request = new Request(url, {
        method:"POST",
        body:fd
    });

    fetch(request).then(response => {
        if (response.redirected) {
            window.location.href = response.url
        } else {
            // show email or password was incorrect message
        }
    });
}