const URL = '/NurseAPI/';

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

function clear_patient_card_style() {
    $('[name=patient_card]').each(function (i, tag) {
        $(tag).find('tr').each(function (j, tr) {
            $(tr).removeAttr('style');
        })
    })
}

// 住院患者查询
function QueryInpatients() {
    console.log(URL);
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            get_param: 'INPATIENTS_QUERY'
        },
        success: function (data) {
            let $inpatients_card = $('#inpatisnts_card');
            $inpatients_card.empty();
            console.log(data);/** */
            for (let i = 0; i < data.length; i++) {
                let patient_info = data[i];
                let td = StringFormat('<td>{0}</td><td>{1}</td>', patient_info.name, patient_info.care_level);
                /** */
                let tr = $(StringFormat(
                    "<tr name='inpatient' onclick='QueryPatientInfo({0}, {1})'></tr>",
                    patient_info.regis_id,
                    'this'
                ));
                tr.append(td);
                $inpatients_card.append(tr);
            }
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);/** */
        }
    });
}

// 待收患者查询
function QueryWaitingPatients() {
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            'get_param': 'WAITING_QUERY'
        },
        success: function (data) {
            console.log(data);
            let $waiting_patients_card = $('#waiting_patients_card');
            $waiting_patients_card.empty();
            for (let i = 0; i < data.length; i++) {
                let patient_info = data[i];
                let td = StringFormat('<td>{0}</td><td>{1}</td>', patient_info.name, patient_info.gender);
                let tr = $(StringFormat(
                    "<tr name='waiting_patient' onclick='QueryPatientInfo({0}, {1})'></tr>",
                    patient_info.regis_id,
                    'this'
                ));
                tr.append(td);
                $waiting_patients_card.append(tr);
            }
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        }
    });
}

function clear_all_info() {
    $('#no').removeAttr('placeholder');
    $('#name').removeAttr('placeholder');
    $('#age').removeAttr('placeholder');
    $('#gender').removeAttr('placeholder');
    $('#medical_advice').html('<p class="col-12">今日暂无医嘱</p>');
    $('#medicine_info').html('<p class="col-12">今日暂无药品信息</p>');
    $('#test_item').html('<p class="col-12">今日暂无检查检验项目</p>');
    $('input, textarea').each(function (i, tag) {
        if ($(tag).attr('name') !== 'post_param')
            $(tag).val('');
    })
}

// 患者基础信息查询
function QueryPatientInfo(regis_id, event) {
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            'regis_id': regis_id,
            'get_param': 'PATIENT_INFO_QUERY'
        },
        success: function (data) {
            clear_all_info();
            if ($(event).attr("style")) {
                $(event).removeAttr('style');
                return;
            }
            clear_patient_card_style();
            $(event).attr('style', 'background-color: #d7dae3');
            console.log("入院登记QueryPegisterPatient函数")
            console.log(data);
            $("#no").attr('placeholder', data.regis_id);
            $("#name").attr('placeholder', data.name);
            $("#gender").attr('placeholder', data.gender);
            $("#age").attr('placeholder', data.age);
            $('input[name=regis_id]').each(function (i, tags) {
                $(tags).val(data.regis_id);
            })

            document.getElementById("care_level").options.selectedIndex = 0; //回到初始状态
            $("#care_level").selectpicker('refresh');//对searchPayState这个下拉框进行重置刷新
            QueryMedicalAdviceProcess(data.regis_id)

        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        },
    })
}

// 医嘱处理查询
function QueryMedicalAdviceProcess(regis_id) {
    console.log(URL);
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            regis_id: regis_id,
            get_param: 'MEDICAL_ADVICE_QUERY'
        },
        success: function (data) {

            console.log(data);
            /** */
            let $medical_advice = $('#medical_advice');
            let $medicine_info = $('#medicine_info');
            let $test_item = $('#test_item');
            if (data.medicine_info.length) $medical_advice.empty();
            if (data.medical_advice_info.length) $medicine_info.empty();
            if (data.inspect_info.length) $test_item.empty();
            for (let i = 0; i < data.medicine_info.length; i++) {
                let medicine = data.medicine_info[i];
                $medicine_info.append(StringFormat(
                    '<p class="col-6">{0}</p><span class="col-6">数量：{1}</span>',
                    medicine[1],
                    medicine[0]
                ));
            }
            for (let i = 0; i < data.medical_advice_info.length; i++) {
                $medical_advice.append(StringFormat(
                    '<p class="col-12">{0}</p>',
                    data.medical_advice_info[i]
                ))
            }

            for (let i = 0; i < data.inspect_info.length; i++) {
                $test_item.append(StringFormat(
                    '<p class="col-12">{0}</p>',
                    data.inspect_info[i]
                ))
            }

            document.getElementById("MedicalAdviceProcess").click();
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);/** */
        },
    })
}

// 床位选择
function BedSelect() {
    let BED = $("input[name='BED']:checked").val();
    console.log(document.getElementById('AreaBed')); /**/
    if (BED !== undefined) {
        document.getElementById('AreaBed').value = BED;
    } else {
        document.getElementById('AreaBed').value = '';
    }
}

// 可用床位查询
function QueryBed() {
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            get_param: 'BED_QUERY'
        },
        success: function (data) {
            $("#areas").empty();
            // 生成病区分页按钮
            for (let i in data) {
                let format_str = '<li class="nav-item"><a href="#{0}" class="nav-link {1}" data-toggle="tab" aria-expanded="false">病区{0}</a></li>'
                is_active = ''
                if (i == 0) {
                    is_active += 'active ';
                }
                let areas = StringFormat(format_str, data[i].AREA, is_active)
                $("#areas").append(areas)
            }
            $("#beds").empty();
            // 生成病区分页页面
            for (let i in data) {
                // 床位 labels
                let labels_html = ''
                let format_str_inside = '<label class="radio-inline mr-3"><input type="radio" value="{0}{1}" name="BED">{0}{1}</label>'
                for (let bed in data[i].BED) {
                    labels_html += StringFormat(format_str_inside, data[i].AREA, bed)
                }
                // 床位 html
                let format_str = '<div id="{0}" class="tab-pane fade {1}"><div class="card-body"><div class="form-group mb-0">{2}</div></div></div>'
                is_active = ''
                if (i == 0) {
                    is_active += 'show active'
                }
                let beds = StringFormat(format_str, data[i].AREA, is_active, labels_html)
                $("#beds").append(beds);
            }
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        }
    });
}

// 提交护理记录
function postNursingRecord(csrf_token) {
    let data = $('#nursing_record_form').serialize();
    console.log(data);
    if ($('#no').attr('placeholder') === undefined) {
        submitAlert('提交失败', '未选择病人', 'error');
        return;
    }
    $.ajax({
        type: 'POST',
        url: URL,
        data: data,
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        },
        success: function (callback) {
            if (callback.status === 0) {
                submitAlert('提交成功', callback.message, 'success');
            } else {
                submitAlert('提交失败', callback.message, 'error');
            }
        },
        error: function () {
            alert('提交护理记录失败');
        }
    })
}

// 提交入院登记
function postHospitalRegistration(csrf_token) {
    let data = $('#hospital_registration_form').serialize();
    console.log(data);
    if ($('#no').attr('placeholder') === undefined) {
        submitAlert('提交失败', '未选择病人', 'error');
        return;
    }
    $.ajax({
        type: 'POST',
        url: URL,
        data: data,
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        },
        success: function (callback) {
            if (callback.status === 0) {
                submitAlert('提交成功', callback.message, 'success');
                $('.swal2-confirm').attr('onblur', 'window.location.reload()');
            } else {
                submitAlert('提交失败', callback.message, 'error');
            }
        },
        error: function () {
            alert('入院登记记录失败');
        }
    })
}

QueryInpatients()
QueryWaitingPatients()


/*
function queryWaitingRegistrationPatient() {
    $.ajax({
        url: URL,
        dataType: 'json',
        data: {'information': 'WAITING_QUERY'},
        success:function(data){
            console.log(data);
        }
    })
}
*/

