/**
 * Created by daath on 16-4-28.
 */


//$(document).ready(function(){
//    $("form#signIn").submit(function(){
//        var account = $("#inputAccount").val();
//        var password = $("#inputPassword").val();
//        $.ajax({
//            url: "/admin/user/signIn/",
//            data: {
//                account: account,
//                password: password
//            },
//            async: false,
//            type: "POST",
//            dataType: "json",
//            success: function(data) {
//                switch (data['msgCode']) {
//                    case 1002:
//                        alert(data['msg']);
//                        break;
//                    case 1003:
//                        alert(data['msg']);
//                        break;
//                    case 1006:
//                        alert(data['msg']);
//                        break;
//                    case 4:
//                        alert(data['msg']);
//                        break;
//                }
//            }
//        });
//    });
//});

function signInCheck() {
    var account = $("#inputAccount").val();
    var password = $("#inputPassword").val();
    $.ajax({
        url: "/admin/user/signIn/",
        data: {
            account: account,
            password: password
        },
        async: false,
        type: "POST",
        dataType: "json",
        success: function(data) {
            switch (data['msgCode']) {
                case 1000:
                    alert("需要参数");
                    break;
                // 以上错误一般不会出现
                case 1002:
                    if ($("div#errorDisplay").length) { // 登录失效时候重定向
                        $("div#errorDisplay").text("此账号还没有注册");
                    } else {
                        $("div#errorDisplay1").show();
                        $("div#errorDisplay1").text("此账号还没有注册");
                    }
                    break;
                case 1003:
                    if ($("div#errorDisplay").length) {
                        $("div#errorDisplay").text("密码错误");
                    } else {
                        $("div#errorDisplay1").show();
                        $("div#errorDisplay1").text("密码错误");
                    }
                    break;
                case 1006:
                    if ($("div#errorDisplay").length) {
                        $("div#errorDisplay").text("此账号还正在申请权限中，请耐心等候");
                    } else {
                        $("div#errorDisplay1").show();
                        $("div#errorDisplay1").text("此账号还正在申请权限中，请耐心等候");
                    }
                    break;
                case 4:
                    if ($("div#errorDisplay").length) {
                        $("div#errorDisplay").removeClass("alert-danger");
                        $("div#errorDisplay").addClass("alert-success");
                        $("div#errorDisplay").text("登录成功，为您跳转控制台！");
                    } else {
                        $("div#errorDisplay1").show();
                        $("div#errorDisplay1").removeClass("alert-danger");
                        $("div#errorDisplay1").addClass("alert-success");
                        $("div#errorDisplay1").text("登录成功，为您跳转控制台！");
                    }
                    setTimeout(function() {
                        window.location.href = '/admin/user/adminCenter/';
                    }, 3000);
                    return true;
                    break;
            }
        }
    });
    return false;
}

function signUpCheck() {
    var account = $("#account").val();
    var password = $("#password").val();
    var confirmPassword = $("#confirmPassword").val();
    var realName = $("#realName").val();
    var nickname = $("#nickname").val();
    var phone = $("#phone").val();
    if (password != confirmPassword) {
        alert("确认密码不一致");
        //$("#confirmPassword").parent("div").addClass("has-error");
    } else {
        $.ajax({
            url: '/admin/user/signUp/',
            data: {
                account: account,
                password: password,
                realName: realName,
                nickname: nickname,
                phone: phone
            },
            async: false,
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                switch (data['msgCode']) {
                    case 1000:
                        alert("需要参数");
                        break;
                    // 以上错误一般不会出现
                    case 1001:
                        $("div#errorDisplay").show();
                        $("div#errorDisplay").text("此账号已经被注册");
                        $("#account").focus().end();
                        break;
                    case 0:
                        $("div#errorDisplay").removeClass("alert-danger");
                        $("div#errorDisplay").addClass("alert-success");
                        $("div#errorDisplay").show();

                        $("div#errorDisplay").text("注册成功！为您跳转登录页面");
                        setTimeout(function() {
                            window.location.href = '/admin/user/signIn/';
                        }, 1000);
                        break;
                }
            }
        })
    }
    return false;
}


