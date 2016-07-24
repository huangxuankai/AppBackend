/**
 * Created by daath on 16-4-30.
 */


function becomeGuide(id) {
    var guideId = id;
    $.ajax({
        url: '/admin/user/becomeGuide/',
        data: {id: guideId},
        async: false,
        type: 'POST',
        dataType: 'json',
        success: function(data) {
            switch (data['msgCode']) {
                case 1000:
                    alert("需要参数");
                    break;
                // 以上错误一般不会出现
                case 9:
                    alert("操作成功，此人已通过导游申请");
                    // 重新刷新
                    $.ajax({
                        url: '/admin/user/applyGuideLists/',
                        data: {},
                        async: false,
                        type: 'GET',
                        success: function(data) {
                            $("#displayContent").html(data);

                        }
                    });
                    break;
            }

        }
    });
}


function becomeAdmin(id) {
    var adminId = id;
    $.ajax({
        url: '/admin/user/becomeAdmin/',
        data: {id: adminId},
        async: false,
        type: 'POST',
        dataType: 'json',
        success: function(data) {
            switch (data['msgCode']) {
                case 1000:
                    alert("需要参数");
                    break;
                // 以上错误一般不会出现
                case 10:
                    alert("操作成功，此人已通过管理员申请");
                    // 重新刷新
                    $.ajax({
                        url: '/admin/user/applyAdminLists/',
                        data: {},
                        async: false,
                        type: 'GET',
                        success: function(data) {
                            $("#displayContent").html(data);

                        }
                    });
                    break;
            }

        }
    });
}






