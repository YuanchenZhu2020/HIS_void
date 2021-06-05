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

// 日期字符串格式化
function YmdToMd(date) {
    return date.split('-').slice(1,3).join('-');
}

function YmdToStr(date) {
    return StringFormat("{0} 年 {1} 月 {2} 日", ...date.split('-'));
}


// 获取挂号医生信息
function QueryGH(date, department) {
    let URL = "/PatientRegisterAPI";
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            KS_id: department.id,
            date: date,
        },
        success: function (data) {
            // let patient_id = data["query_source"];
            let query_data = data["query_data"];
            let token = data["token"];
            let submit_url = data["submit_url"];
            // 科室名称、医生姓名、crsf_token、医生ID、挂号日期、AM/PM、提交地址
            let registration_confirm_str = "registration_confirm(this, '{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')";
            // 清除原有数据行
            $("#" + department.id + '-' + YmdToMd(date)).children().remove();
            // 插入新的数据行
            for (let i = 0; i < query_data.length; i++) {
                // 医生信息对象
                let DoctorInfo = query_data[i];
                // 创建医生姓名行
                let doctor_name_td = $("<td></td>");
                // 添加医生姓名
                doctor_name_td.text(DoctorInfo.doctor_name);
                // 创建上午挂号按钮行
                let AM_remain_td = $("<td></td>");
                // 创建下午按钮挂号行
                let PM_remain_td = $("<td></td>");
                // 创建上午挂号按钮
                let AM_btn = $("<button type='button' class='btn btn-sm btn-block btn-outline-primary' data-toggle='modal' data-target='#GHask'></button>");
                // 创建下午挂号按钮
                let PM_btn = $("<button type='button' class='btn btn-sm btn-block btn-outline-primary' data-toggle='modal' data-target='#GHask'></button>");
                // 在按钮上添加剩余人数
                AM_btn.text(DoctorInfo.AM);
                PM_btn.text(DoctorInfo.PM);
                // 在按钮上添加挂号费用
                AM_btn.attr("data-price", DoctorInfo.price);
                PM_btn.attr("data-price", DoctorInfo.price);
                // 如果剩余人数为0，则禁用按钮
                if (DoctorInfo.AM === 0) {
                    AM_btn.attr('disabled', true);
                }
                if (DoctorInfo.PM === 0) {
                    PM_btn.attr('disabled', true);
                }
                // 向按钮行中添加按钮
                AM_remain_td.append(AM_btn);
                PM_remain_td.append(PM_btn);
                AM_btn.attr('onclick', StringFormat(
                    registration_confirm_str,
                    department.name, DoctorInfo.doctor_name,
                    token, DoctorInfo.doctor_id, date, 'AM', submit_url
                ));
                PM_btn.attr('onclick', StringFormat(
                    registration_confirm_str,
                    department.name, DoctorInfo.doctor_name,
                    token, DoctorInfo.doctor_id, date, 'PM', submit_url
                ));
                // 创建行
                let tr = $("<tr></tr>");
                tr.append(doctor_name_td);
                tr.append(AM_remain_td);
                tr.append(PM_remain_td);
                $("#" + department.id + '-' + YmdToMd(date)).append(tr);
            }
        },
        error: function (err) {
            alert("请求服务器失败！");
        }
    });
}


// 挂号确认弹窗
function registration_confirm(
    event_obj, department_name, doctor_name, token, patient_id, doctor_id, reg_date, AM_PM, submit_url
) {
    let reg_time, reg_time_str, reg_datetime;
    let price = event_obj.dataset.price;
    if (AM_PM === "AM"){
        reg_time = "08:00:00";
        reg_time_str = "上午 8:00 - 11:00";
    }
    else {
        reg_time = "13:00:00";
        reg_time_str = "下午 13:00 - 18:00";
    }
    reg_datetime = reg_date + " " + reg_time;
    $("#modal-body").empty();
    let note = StringFormat(
        "<strong>{0}{1}，{2}，{3}医生</strong>",
        YmdToStr(reg_date), reg_time_str, department_name, doctor_name
    );
    $("#modal-body").append(note);
    $("#registration").attr("onclick", StringFormat(
        "post_registration('{0}', '{1}', '{2}', '{3}');",
        token, doctor_id, reg_datetime, submit_url
    ));
}


// POST 提交挂号表单
function post_registration(csrf_token, doctor_id, reg_datetime, submit_url) {
    let data = {
        'doctor_id': doctor_id,
        'reg_datetime': reg_datetime
    };
    $.ajax({
        url: submit_url,
        type: 'POST',
        dataType: 'text',
        data: JSON.stringify(data), // 注意这里要将发送的数据转换成字符串
        processData: false,// tell jQuery not to process the data
        contentType: false,// tell jQuery not to set contentType
        beforeSend: function (xhr, setting) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        },
        success: function (data) {
            data = JSON.parse(data);
            let success = data.status;
            let status = "error";
            let alert_title = "提交失败";
            let alert_text = data.msg;
            if (success) {
                console.log(success);
                status = "success";
                alert_title = "提交成功";
            }
            submitAlert(alert_title, alert_text, status);
            console.log(data.redirect_url);
            $(".swal2-actions").attr(
                'onclick',
                StringFormat("window.location.href = '{0}'", data.redirect_url)
            );
        },
        error: function (callback) {
            console.log(callback);
            alert('提交失败');
        }
    })
}


// 快速挂号，获取指定医生在指定日期的剩余挂号数
function QueryDocReg(doctor_id, doctor_name, date) {
    let URL = "/PatientFastRegisterAPI";
    $.ajax({
        type: "GET",
        url: URL,
        data: {
            "doctor_id": doctor_id,
            "reg_date": date,
        },
        success: function(data) {
            // 获取返回信息，包括上午和下午的剩余挂号数
            let query_data = data["query_data"];
            let token = data["token"];
            let submit_url = data["submit_url"];
            if (query_data !== null) {
                // 清除原有数据行
                $("#" + YmdToMd(date)).children().remove();
                // 创建待插入的行
                let doctor_name_td = $("<td></td>");
                doctor_name_td.text(doctor_name);
                let AM_remain_td = $("<td></td>");
                let PM_remain_td = $("<td></td>");
                let AM_btn = $("<button type='button' class='btn btn-sm btn-block btn-outline-primary' data-toggle='modal' data-target='#GHask'></button>");
                let PM_btn = $("<button type='button' class='btn btn-sm btn-block btn-outline-primary' data-toggle='modal' data-target='#GHask'></button>");
                // 在按钮上添加剩余人数
                AM_btn.text(query_data.AM);
                PM_btn.text(query_data.PM);
                // 如果剩余人数为0，则禁用按钮
                if (query_data.AM === 0) {
                    AM_btn.attr('disabled', true);
                }
                if (query_data.PM === 0) {
                    PM_btn.attr('disabled', true);
                }
                // 向按钮行中添加按钮
                AM_remain_td.append(AM_btn);
                PM_remain_td.append(PM_btn);
                // 在按钮上添加挂号费用
                AM_btn.attr("data-price", query_data.price);
                AM_btn.attr("data-price", query_data.price);
                // 添加事件
                AM_btn.attr('onclick', StringFormat(
                    "registration_confirm('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')", 
                    query_data.dept_name, doctor_name, token, doctor_id, date, 'AM', submit_url
                ));
                PM_btn.attr('onclick', StringFormat(
                    "registration_confirm('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')", 
                    query_data.dept_name, doctor_name, token, doctor_id, date, 'PM', submit_url
                ));
                // 创建行
                let tr = $("<tr></tr>");
                tr.append(doctor_name_td);
                tr.append(AM_remain_td);
                tr.append(PM_remain_td);
                $("#" + YmdToMd(date)).append(tr);
            }
        },
        error: function(error) {
            console.log(error);
            alert("无法获取数据，请检查您是否联网");
        }
    })
}


// 获取挂号信息详情
function diagnosis_detail(reg_id) {
    let URL = "/PatientTreatmentDetailAPI"
    $.ajax({
        type: "GET",
        url: URL,
        data: {
            "reg_id": reg_id,
            "type": "REG"
        },
        success: data => {
            $("#" + reg_id + "-ap-date").children("span").text(data["ap_date"]);
            $("#" + reg_id + "-reg-class").children("span").text(data["reg_class"]);
            $("#" + reg_id + "-ill-date").children("span").text(data["ill_date"]);
            $("#" + reg_id + "-chief-complaint").children("span").text(data["chief_complaint"]);
            $("#" + reg_id + "-diag-result").children("span").text(data["diag_result"]);
        },
        error: error => {
            console.log(error);
            alert("无法获取数据，请检查您是否联网");
        }
    })
}


// 获取检查信息详情
function check_detail(reg_id, test_id) {
    let URL = "/PatientTreatmentDetailAPI"
    $.ajax({
        type: "GET",
        url: URL,
        data: {
            "reg_id": reg_id,
            "test_id": test_id,
            "type": "CHE"
        },
        success: data => {
            let pre_id = StringFormat("#{0}-{1}-", reg_id, test_id);
            $(pre_id + "test-name").children("span").text(data["test_name"]);
            $(pre_id + "doctor-name").children("span").text(data["doctor_name"]);
            $(pre_id + "issue-date").children("span").text(data["issue_date"]);
            $(pre_id + "result").children("span").text(data["result"]);
        },
        error: error => {
            console.log(error);
            alert("无法获取数据，请检查您是否联网");
        }
    })
}


// 患者缴费函数
function third_party_pay(csrf_token, item, price, pk_str, subject, return_url) {
    let URL = "/PaymentAPI/";
    // 目前只支持支付宝支付
    let pay_type = "alipay";
    $.ajax({
        type: "POST",
        url: URL,
        dataType: 'json',
        data: {
            "type": pay_type,
            "item": item,
            "price": price,
            "pk": pk_str,
            "subject": subject,
            "return_url": return_url,
        },
        beforeSend: function (xhr, setting) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        },
        success: data => {
            console.log(data);
            window.location.href = data["url"];
        },
        error: error => {
            console.log(error);
            alert("暂不能进行支付，请稍后再试！")
        }
    })
}
