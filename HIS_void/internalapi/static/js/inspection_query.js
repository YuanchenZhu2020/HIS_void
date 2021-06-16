// 字符串格式化函数
function StringFormat() {
    if (arguments.length == 0)
        return null;
    var str = arguments[0];
    for (var i = 1; i < arguments.length; i++) {
        var re = new RegExp('\\{' + (i - 1) + '\\}', 'gm');
        str = str.replace(re, arguments[i]);
    }
    return str;
}

// 检验信息查询
function QueryInspectionInfo(obj, inspection_id) {
    let URL = '/InspectionAPI';
    // console.log(URL);
    $.ajax({
        type: "GET",
        url: URL,
        dataType: 'json',
        data: {
            inspection_id: inspection_id,
            info: "INSPECTION"
        },
        success: data => {
            // 初始化待检患者样式
            ClearFocusStyle();
            // 更改选中患者的样式
            FocusStyle(obj);
            $("#inspection_id").val(data.inspection_id);
            $("#patient_id").val(data.patient_id);
            $("#name").val(data.name);
            $("#gender").val(data.gender);
            $("#age").val(data.age);
            $("#inspection_name").val(data.inspection_name);
            $("#issue_time").val(data.issue_time);
            $("#staff_name").val(data.medical_staff);
            $("#JYXX_a").click();
        },
        error: error => {
            alert("请求服务器失败！");
            console.log(error);
        },
    })
}

// 待检患者查询
function QueryWaitingInspect() {
    let URL = '/InspectionAPI';
    $.ajax({
        type: "GET",
        url: URL,
        dataType: 'json',
        data: {
            info: "WAITING"
        },
        success: data => {
            // console.log(data);
            for (let i = 0; i < data.length; i++) {
                let patient = data[i];
                let tdn = '<td>' + patient.name + '</td>';
                let tds = '<td><span class="badge badge-light light">等待中</span></td>'
                let inspection_id = patient.inspection_id;
                let tr = $(StringFormat("<tr onclick='QueryInspectionInfo(this, {0});'></tr>", inspection_id));
                tr.append(tdn);
                tr.append(tds);
                $("#inspectingPatient").append(tr);
            }
        },
        error: error => {
            alert("请求服务器失败！");
            console.log(error);
        }
    });
}

// 初始化全部待检患者样式
function ClearFocusStyle() {
    $($("#inspectingPatient").children()).each(function(index, element) {
        $($($(element).children()[1]).children()[0]).removeClass("badge-primary").addClass("badge-light").text("等待中")
    });
}

// 点击待检患者后改变显示样式
function FocusStyle(obj) {
    $($($(obj).children()[1]).children()[0]).removeClass("badge-light").addClass("badge-primary").text("检查中");
}

// 检查报告提交
function PostInspectionResult(csrf_token) {
    let URL = "/InspectionAPI/";
    let result = $('textarea[name="inspection_result"]').val()
    let inspection_id = $('#inspection_id').val();
    
    if (inspection_id == '') {
        submitAlert("无法提交", "未选择患者！", "error");
        return ;
    }
    if ($.trim(result) == '') {
        submitAlert("无法提交", "请填写检查结果！", "error");
        return ;
    }

    $.ajax({
        type: "POST",
        url: URL,
        dataType: "JSON",
        data: {
            inspection_id: inspection_id, 
            result: result, 
            post_param: 'RESULT'
        },
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        },
        success: data => {
            status = data.status;
            msg = data.msg;
            if (status == -1) {
                submitAlert("提交失败", msg, "error");
            } else {
                submitAlert("提交成功", msg, "success");
                window.location.reload();
            }
        },
        error: error => {
            alert("提交失败！请检查是否连接到服务器！");
            console.log(error);
        }
    })
}

QueryWaitingInspect()
