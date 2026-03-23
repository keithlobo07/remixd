function returnLoginInfo(url, redirect) {
    const fd = new FormData(document.getElementById('loginForm'));

    const request = new Request(url, {
        method:"POST",
        body:fd
    });

    fetch(request).then(response => {window.location.replace(redirect)});
}