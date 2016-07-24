/**
 * Created by daath on 16-4-29.
 */

function signOut() {
    window.location.href = '/admin/user/signOut/';
}

function toAdminCenter() {
    window.location.href = '/admin/user/adminCenter/'
}

function toAddScene() {
    $.ajax({
        url: '/admin/scene/add/',
        data: {},
        async: false,
        type: 'GET',
        success: function(data) {
            $("#displayContent").html(data)
        }
    })
}

function toQueryScene(id) {
    if (!id) {
        return;
    }
    var sceneId = id;
    $.ajax({
        url: '/admin/scene/query/',
        data: {
            id: sceneId
        },
        async: false,
        type: 'GET',    // 获取网页默认GET方法
        success: function(data) {
            $("#displayContent").html(data);
        }
    });
}

function toApplyGuideLists() {
    $("li#titleScene").removeClass("active");
    $("li#titleApply").addClass("active");
    $.ajax({
        url: '/admin/user/applyGuideLists/',
        data: {},
        async: false,
        type: 'GET',
        success: function(data) {
            $("#displayContent").html(data);

        }
    });
}

function toApplyAdminLists() {
    $("li#titleScene").removeClass("active");
    $("li#titleApply").addClass("active");
    $.ajax({
        url: '/admin/user/applyAdminLists/',
        data: {},
        async: false,
        type: 'GET',
        success: function(data) {
            $("#displayContent").html(data);

        }
    });
}

function updateStatus(id, status) {
    $.ajax({
        url: '/admin/scene/updateStatus/',
        data: {
            id: id,
            status: status
        },
        async: false,
        type: 'POST',
        dataType: 'json',
        success: function(data) {
            switch (data['msgCode']) {
                case 1000:
                    alert("需要参数");
                    break;
                // 以上错误一般不会出现
                case 1009:
                    alert("参数status的值有问题");
                    break;
                case 7:
                    alert("该景区上线成功");
                    toAdminCenter();
                    break;
                case 8:
                    alert("该景区下线了");
                    toAdminCenter();
                    break;
            }

        }
    });
}