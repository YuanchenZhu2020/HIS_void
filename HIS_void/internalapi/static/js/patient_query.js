// 格式化字符串
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

// 医生信息
function QueryGH(date, department) {
    let URL = '/PatientViewAPI';
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            information: 'GH',
            KS_id: department.id,
            date: date,
        },
        success: function (data) {
            alert('弹出对话框.');
            for (let i = 0; i < data.length; i++) {
                console.log(data);
                // 医生信息对象
                let doctorInfo = data[i];
                // 创建医生姓名行
                let doctor_name_td = $("<td></td>");
                // 添加医生姓名
                doctor_name_td.text(doctorInfo.doctor_name);
                // 创建上午挂号按钮行
                let AM_remain_td = $("<td></td>");
                // 创建下午按钮挂号行
                let PM_remain_td = $("<td></td>");
                // 创建上午挂号按钮
                let AM_btn = $("<button type='button' class='btn btn-outline-primary' data-toggle='modal' data-target='#GHask'></button>");
                // 创建下午挂号按钮
                let PM_btn = $("<button type='button' class='btn btn-outline-primary' data-toggle='modal' data-target='#GHask'></button>");
                // 在按钮上添加剩余人数
                AM_btn.text(doctorInfo.AM);
                PM_btn.text(doctorInfo.PM);
                // 如果剩余人数为0，则禁用按钮
                if (doctorInfo.AM === 0) {
                    AM_btn.attr('disabled', true);
                }
                if (doctorInfo.PM === 0) {
                    PM_btn.attr('disabled', true);
                }
                // 向按钮行中添加按钮
                AM_remain_td.append(AM_btn);
                PM_remain_td.append(PM_btn);
                //
                console.log(department.name);
                console.log(doctorInfo.doctor_name);
                AM_btn.attr('onclick', StringFormat("registration_confirm('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')", department.id, department.name, date, 'AM', doctorInfo.doctor_id, doctorInfo.doctor_name));
                PM_btn.attr('onclick', StringFormat("registration_confirm('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')", department.id, department.name, date, 'PM', doctorInfo.doctor_id, doctorInfo.doctor_name));
                // 创建行
                let tr = $("<tr></tr>");
                tr.append(doctor_name_td);
                tr.append(AM_remain_td);
                tr.append(PM_remain_td);
                $("#" + department.id + '_' + date).append(tr);
            }
        },
        error: function (err) {
            alert("请求服务器失败！");
        }
    });
}

// 挂号按钮，点击可以挂号

function registration_confirm(department_id, department_name, date, AM_PM, doctor_id, doctor_name) {
    // console.log(department);
    // console.log(date);
    // console.log(AM_PM);
    // console.log(doctorInfo);
    let regis_time;
    if (AM_PM === "PM") regis_time = "上午";
    else regis_time = "下午";
    $("#modal-body").empty();
    let note = '<strong>' + date + regis_time + ' ' + department_name + " " + doctor_name + "医生" + '</strong>';
    console.log(note);
    $("#modal-body").append(note);
    $("#registration").attr("onclick", StringFormat("registration('{0}', '{1}', '{2}', '{3}')", department_id, date, 'AM', doctor_id));
}

function registration(department_id, regis_date, regis_AM_PM, doctor_id) {
    let regis_form = $("<form action='#'></form>");
    let department_id_input = $("<input>");
    department_id_input.attr('name', 'department_id');
    department_id_input.attr('value', department_id);
    let regis_date_input = $("<input>");
    regis_date_input.attr('name', 'regis_date');
    regis_date_input.attr('value', regis_date);
    let regis_AM_PM_input = $("<input>");
    regis_AM_PM_input.attr('name', 'regis_AM_PM');
    regis_AM_PM_input.attr('value', regis_AM_PM);
    let doctor_id_input = $("<input>");
    doctor_id_input.attr('name', 'doctor_id');
    doctor_id_input.attr('value', doctor_id);
    regis_form.submit();
}
