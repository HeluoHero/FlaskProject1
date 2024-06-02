const RegisterHandler = function () {

}

RegisterHandler.prototype.listenSendCaptchaEvent = function () {
    const callback = function (event) {
        const $this = $(this)
        // 阻止默认的点击事情
        event.preventDefault();
        const email = $("input[name='email']").val()
        const reg = /^\w+((.\w+)|(-\w+))@[A-Za-z0-9]+((.|-)[A-Za-z0-9]+).[A-Za-z0-9]+$/;
        if (!email || !reg.test(email)) {
            alert('请输入正确的邮箱')
            return
        }
        zlajax.get({
            url: '/email/captcha?email=' + email,
            success: (result) => {
                if (result['code'] === 200) {
                    console.log('邮件发送成功')
                    $this.off('click')

                    $this.attr('disable', 'disable')
                    let countdown = 60
                    const timer = setInterval(() => {
                        countdown--
                        if (countdown === 0) {
                            $this.removeAttr('disable')
                            $this.on('click', callback)
                            countdown = 60
                            clearInterval(timer)
                            $this.text('发送验证码')
                        } else {
                            $this.text(countdown + '秒后重新发送')
                        }
                    }, 1000)
                } else {
                    alert(result['message'])
                }
            }
        })


    }
    $("#email-captcha-btn").on('click', callback)
}

RegisterHandler.prototype.listenGraphCaptchaEvent = function () {
    $("#captcha-img").on('click', function () {
        const $this = $(this);
        const src = $this.attr("src");
        // /graph/captcha
        // /graph/captcha?sign=Math.random()
        // 防止一些老的浏览器，在两次url相同的情况下，不会重新发送请求，导致图形验证码不会更新
        let new_src = zlparam.setParam(src, "sign", Math.random())
        $this.attr("src", new_src);
    })
}

RegisterHandler.prototype.listenSubmitEvent = function () {
    $("#submit-btn").on("click", function (event) {
        event.preventDefault();
        const email = $("input[name='email']").val();
        const email_captcha = $("input[name='email-captcha']").val();
        const username = $("input[name='username']").val();
        const password = $("input[name='password']").val();
        const repeat_password = $("input[name='repeat-password']").val();
        const graph_captcha = $("input[name='graph-captcha']").val();

        // 如果是商业项目，一定要先验证这些数据是否正确
        zlajax.post({
            url: "/register",
            data: {
                "email": email,
                "email_captcha": email_captcha,
                "username": username,
                password, // "password": password
                repeat_password,
                graph_captcha
            },
            success: function (result) {
                if (result['code'] === 200) {
                    window.location = "/login";
                } else {
                    alert(result['message']);
                }
            }
        })
    });
}

RegisterHandler.prototype.run = function () {
    this.listenSendCaptchaEvent()
    this.listenGraphCaptchaEvent()
    this.listenSubmitEvent()
}

$(function () {
    const handle = new RegisterHandler()
    handle.run()
})