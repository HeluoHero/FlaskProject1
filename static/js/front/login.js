const LoginHandler = function () {
}

LoginHandler.prototype.listenSubmitEvent = function () {
    $('#submit-btn').on('click', function (event) {
        event.preventDefault()
        const email = $("input[name='email']").val()
        const password = $("input[name='password']").val()
        const remember = $("input[name='remember']").prop('checked')
        zlajax.post({
            url: '/login',
            data: {
                email: email,
                password: password,
                remember: remember ? 1 : 0
            },
            success: function (result) {
                if (result['code'] === 200) {
                    window.location = '/'
                } else {
                    alert(result['message'])
                }
            }
        })
    })
}

LoginHandler.prototype.run = function () {
    this.listenSubmitEvent()
}

$(function () {
    const handler = new LoginHandler();
    handler.run()
})



