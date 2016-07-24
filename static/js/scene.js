/**
 * Created by daath on 16-4-29.
 */


function addSceneInfo() {
    $("form#add").ajaxSubmit({
        url: '/admin/scene/add/',
        type: 'POST',
        success: function(data) {
            switch (data['msgCode']) {
                case 1000:
                    alert("需要参数");
                    break;
                case 1008:
                    alert("请给景区添加一张图片");
                    break;
                // 以上错误基本不会出现，因为前台已经
                case 1005:
                    alert("更新的坐标有问题");
                    break;
                case 1007:
                    alert("此景区名已经存在了");
                    break;
                case 5:
                    alert("景区已经添加，请查看");
                    window.location.href = '/admin/user/adminCenter/';
                    break;
            }

        }
    });
    return false;
}


function updateSceneInfo() {

    $.ajax({
        url: '/admin/scene/update/',
        data: $("form#updateScene").serialize(),
        async: false,
        type: 'POST',
        dataType: 'json',
        success: function(data) {
            switch (data['msgCode']) {
                case 1000:
                    alert("需要参数");
                    break;
                // 以上错误基本不会出现，因为前台已经
                case 1005:
                    alert("更新的坐标有问题");
                    break;
                case 1007:
                    alert("此景区名已经存在了");
                    break;
                case 6:
                    alert("此景区信息已经更新");
                    break
            }
        }
    });
    return false;
}
