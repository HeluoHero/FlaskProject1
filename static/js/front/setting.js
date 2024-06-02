const SettingHandler = function () {
}

SettingHandler.prototype.listenAvatarUploadEvent = function () {
    $("#avatar-input").on('change', function () {
        const image = this.files[0]
        const formData = new FormData()
        formData.append('image', image)
        zlajax.post({
            url: "/avatar/upload",
            data: formData,
            // 如果使用jQuery上传文件，那么还需要指定以下两个参数
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['code'] === 200) {
                    window.location.reload()
                } else {
                    zlalert.alertInfo(result['message'])
                }
            }
        })
    })
}

SettingHandler.prototype.listenSubmitEvent = function () {
    $("#submit-btn").on('click', function (event) {
        event.preventDefault()
        const signature = $("#signagure-input").val()
        if (!signature) {
            alert('提交成功')
            return;
        }
        if (signature && (signature.length > 100 || signature.length < 1)) {
            alert('签名长度应在2-100之间')
            return
        }
        zlajax.post({
            url: "/profile/edit",
            data: {signature},
            success: function (result) {
                if (result['code'] === 200) {
                    alert('提交成功')
                } else {
                    alert(result['message'])
                }
            }
        })
    })
}

SettingHandler.prototype.run = function () {
    this.listenAvatarUploadEvent()
    this.listenSubmitEvent()
}

$(function () {
    const handler = new SettingHandler()
    handler.run()
})