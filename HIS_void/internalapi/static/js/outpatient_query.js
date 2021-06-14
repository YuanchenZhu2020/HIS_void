// 该文件只会向OutpatientAPI交互数据，因此设置URL为本文件的全局变量
const URL = '/OutpatientAPI/';

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

// 清空医生工作区信息
function clear_all_info() {
    // 清除最上方病人信息
    $('#patient_basic_info').find('input').each(function (i, tag) {
        $(tag).val('');
        $(tag).removeAttr('placeholder');
    });
    // 清空病历首页的内容
    $('#history_sheet_form').find('input:visible, textarea').each(function (i, tag) {
        $(tag).val('');
        $(tag).removeAttr('placeholder');
    })
    $('#inspection_text').empty();
    $('#inspection_text_copy').empty();
    $('#medicine_tbody').empty();
    $('#diagnosis_results').val('');
    $('#medical_advice').val('');
    $('#medicine_count').text(0);
    $('#medicine_copy_total_price').text(0);
    $('#inspection_count').text(0);
    $('#medicine_copy_tbody').empty();
    $('#inspection_cost_body').empty();
}

// 待诊患者查询
function query_waiting_diagnosis_patients() {
    $.ajax({
        type: "GET",
        url: URL,
        dataType: 'json',
        data: {
            get_param: 'waiting_diagnosis'
        },
        success: function (data) {
            // console.log(data);
            let $waiting_diagnosis_card = $('#waiting_diagnosis');
            $waiting_diagnosis_card.empty();
            for (let i = 0; i < data.length; i++) {
                let patient = data[i];
                let td = '<td>' + patient.name + '</td>';
                let td1 = '<td>' + patient.gender + '</td>';
                let id = patient.id
                let tr = $("<tr name='patient_card_tr' onclick='QueryPatientBaseInfo(" + id + ", this)'></tr>");
                tr.append(td);
                tr.append(td1);
                $waiting_diagnosis_card.append(tr);
            }
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        }
    });
}

// 查询患者所有的需要的信息
function QueryPatientBaseInfo(regis_id, event) {
    if ($(event).attr('style')) {
        clear_patient_card_style();
        clear_all_info();
        return;
    }
    $.ajax({
        type: "GET",
        url: URL,
        dataType: 'json',
        data: {
            regis_id: regis_id,
            get_param: 'patient_base_info',
        },
        success: function (data) {
            clear_patient_card_style();
            $(event).attr('style', 'background-color: #d7dae3');
            // 设置最上面显示的患者信息
            $("#no").attr('placeholder', regis_id);
            $("#name").attr('placeholder', data.name);
            $("#gender").attr('placeholder', data.gender);
            $("#age").attr('placeholder', data.age);
            // 给每一个需要提交的表格设置挂号记录编号
            $("input[name='regis_id']").each(function (i, value) {
                $(value).val(regis_id);
            })
            /*
            其他需要的信息：
                - 已经选择的检验项目
                - 患者账单
            */
            QueryHistorySheet(regis_id);
            QueryTestResults(regis_id);
            QueryDiagnosisResults(regis_id);
            QueryMedicalAndAdvice(regis_id);
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        },
    })
}

// 输入框改变后样式改变
function clear_this_style(event) {
    $(event).removeAttr('style');
    $(event).removeAttr('onkeyup');
    $(event).removeAttr('onchange');
}

// 清除患者队列样式
function clear_patient_card_style() {
    $('[name=patient_card_tr]').each(function (i, tag) {
        $(tag).removeAttr('style');
    })
}

// 设置 textarea 样式
function init_style(id_selector) {
    $(id_selector).find('input:visible, textarea, tr').each(function (i, tag) {
        // console.log(tag);
        if ($(tag).val())
            $(tag).attr('style', 'color: #a2a5a8;');
        $(tag).attr('onkeyup', 'clear_this_style(this);')
        $(tag).attr('onchange', 'clear_this_style(this);')
    })
}

// 病历首页查询
function QueryHistorySheet(regis_id) {
    $.ajax({
        type: "GET",
        url: URL,
        dataType: 'json',
        data: {
            regis_id: regis_id,
            get_param: 'history_sheet'
        },
        success: function (data) {
            // console.log("病历首页数据")
            // console.log(data);
            $("#chief_complaint").val(data.chief_complaint);
            $("#past_illness").val(data.past_illness);
            $("#allegic_history").val(data.allegic_history);
            $("#illness_date").val(data.illness_date);
            init_style('#history_sheet_form');
            $("#togo_history_sheet").click();
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        },
    })
}

// 查询诊中患者
function QueryInDiagnosisPatient() {
    $.ajax({
        type: "GET",
        url: URL,
        dataType: 'json',
        data: {
            get_param: 'in_diagnosis'
        },
        success: function (data) {
            let $in_diagnosis_card = $("#in_diagnosis");
            console.log(data);
            data.sort(function (a, b) {
                return b.progress - a.progress;
            })
            for (let i = 0; i < data.length; i++) {
                let patient = data[i];
                let progress = '<div class="progress"><div class="progress-bar {1}"' +
                    ' aria-valuenow="{0}" aria-valuemin="0" ' +
                    'aria-valuemax="100" style="width:{0}%; height:10px;" role="progressbar"></div></div>'
                if (patient.progress === 100) {
                    progress = StringFormat(progress, patient.progress, 'bg-success')
                } else {
                    progress = StringFormat(progress, patient.progress, 'bg-info progress-bar-striped')
                }
                // console.log(progress)
                let tr = StringFormat(
                    '<tr name="patient_card_tr" onclick="QueryPatientBaseInfo({0}, this)"><td>{1}</td><td>{2}</td></tr>',
                    patient.regis_id,
                    patient.name,
                    progress
                );
                $in_diagnosis_card.append(tr);
            }
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        }
    });
}

// 检查结果查询
function QueryTestResults(regis_id) {
    $.ajax({
        type: "GET",
        url: URL,
        dataType: 'json',
        data: {
            regis_id: regis_id,
            get_param: 'test_results'
        },
        success: function (data) {
            // 添加检查结果到检查检验及门诊确诊
            let $inspection_text = $('#inspection_text')
            $inspection_text.empty();
            for (let i = 0; i < data.length; i++) {
                if (data[i].test_results == null) {
                    data[i].test_results = '暂无结果'
                }
                let $inspection_result_p = $(StringFormat(
                    '<p class="mb-0"><strong>{0}：</strong>{1}</p><hr class="mt-0"/>',
                    data[i].inspect_name,
                    data[i].test_results
                ));
                $inspection_text.append($inspection_result_p);
            }
            copy_inspection_results();
            // 添加检查金额到患者账单
            let $inspection_cost_body = $('#inspection_cost_body');
            $inspection_cost_body.empty();
            for (let i = 0; i < data.length; i++) {
                let inspect_info = data[i];
                $inspection_cost_body.append(StringFormat(
                    '<tr style="color: #a2a5a8;"><td>{0}</td><td>{1}</td><td name="inspection_price">{2}</td></tr>',
                    inspect_info.inspect_type_name,
                    inspect_info.inspect_name,
                    inspect_info.inspect_price
                ))
            }
            inspectionTotalPrice();
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        },
    })
}

// 确诊结果查询
function QueryDiagnosisResults(regis_id) {
    $.ajax({
        type: "GET",
        url: URL,
        data: {
            regis_id: regis_id,
            get_param: 'diagnosis_results',
        },
        dataType: 'json',
        success: function (data) {
            $('#diagnosis_results').val(data['diagnosis_results']);
            init_style('#diagnosis_results_form');
        },
        error: function (data) {
            alert("无法连接服务器");
        }
    })
}

// 药品医嘱查询
function QueryMedicalAndAdvice(regis_id) {
    $.ajax({
        type: "GET",
        url: URL,
        data: {
            regis_id: regis_id,
            get_param: 'medical_advice',
        },
        dataType: 'json',
        success: function (data) {
            // console.log(data);
            $('#medicine_tbody').empty();
            for (let i = 0; i < data['medicine'].length; i++) {
                addMedicine(data['medicine'][i], data['medicine'][i].medicine_quantity)
            }
            $('#medical_advice').val(data['medical_advice']);
            init_style('#medical_advice_form');
        },
        error: data => {
            alert("无法连接服务器");
        }
    })
}

// 住院申请
function ApplicationInhospital(dept_id) {
    let regis_id = $('#no').attr('placeholder');
    if (regis_id === undefined) {
        submitToastr('您未选择病人', '提交失败！', 'error');
        return;
    } else {
        $.ajax({
            type: "GET",
            url: URL,
            data: {
                regis_id: regis_id,
                get_param: 'application_inhospital',
                dept_id: dept_id
            },
            success: function (callback) {
                if (callback.status === -1) {
                    submitAlert('提交失败', callback.message, 'error');
                    return;
                } else {
                    submitAlert('提交成功', callback.message, 'success');
                    $('.swal2-confirm').attr('onblur', 'window.location.reload()');
                }
            },
            error: function () {
                alert('入院申请提交失败！');
            }
        })
    }
}

// 复制检查结果元素
function copy_inspection_results() {
    let inpspection_results_source = $('#inspection_text');
    let inpspction_results_copy = $(inpspection_results_source.clone()).children();
    let inspection_position = $("#inspection_text_copy");
    inspection_position.empty();
    inspection_position.append(inpspction_results_copy);
}

// 搜索框中查询药品
function QueryMedicine() {
    $.ajax({
        type: "GET",
        url: URL,
        dataType: 'json',
        cache: true,
        data: {
            get_param: 'medicine_info'
        },
        success: function (data) {
            if (data.length > 0) {
                let keyWords = [];
                // 获取所有的药品名
                for (let i = 0; i < data.length; i++) {
                    keyWords[i] = data[i]['medicine_name'];
                }
                // 删除匹配元素 div，以免有数据时仍然存在 div 边框
                display_delete();
                let txt = document.getElementById('txt');
                // 定义临时数组用来存储用户与之相匹配的句子
                let tempArr = [];
                // 获取用户所输入的文本框内容
                let text = txt.value;
                for (let i = 0; i < keyWords.length; i++) {
                    // 将用户输入的文本框内容与数组进行比对，输入内容在数组中匹配到，并且开头的值存入临时数组中
                    if (keyWords[i].indexOf(text) !== -1) {
                        tempArr.push(keyWords[i]);
                    }
                }
                // console.log(tempArr);
                // 创建一个 div 用来放提示的语句
                let dvObj = document.createElement("div");
                dvObj.setAttribute('class', 'offset-2 basic-list-group col-md-4');
                document.getElementById("box").appendChild(dvObj);
                dvObj.id = "dv";
                // 当文本框中有内容或者临时数组中没有元素时，删除 div
                if (txt.value.length === 0 || tempArr.length === 0) {
                    display_delete();
                } else {
                    document.getElementById('txt').setAttribute(
                        "style", "border-radius: 0.7rem 0.7rem 0 0; border-bottom:none"
                    );
                    let ulObj = document.createElement("ul");
                    ulObj.setAttribute('class', 'list-group');
                    dvObj.append(ulObj);
                    // 创建临时数组长度个的 p 元素用来显示提示的语句
                    for (let i = 0; i < tempArr.length; i++) {
                        let liObj = document.createElement("li");
                        liObj.setAttribute('class', 'list-group-item');
                        liObj.setAttribute('onclick', 'add_name(this)');
                        ulObj.appendChild(liObj);
                        liObj.innerHTML = '&emsp;' + tempArr[i];
                    }
                }
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            // 状态码
            alert(XMLHttpRequest.status);
        }
    })
}

// 通过点击提示框中 li 元素将药品名添加到 input 中
function add_name(e) {
    // console.log(e)
    document.getElementById('txt').value = e.innerText.trim();
    display_delete();
}

// 删除提示框，用于选定药品后或者输入框失去焦点后
function display_delete() {
    if (document.getElementById("dv")) {
        document.getElementById("box").removeChild(document.getElementById("dv"));
        $("#txt").attr("style", '');
    }
}

// 添加药品按钮，收集药品名和药品数量
function collect_medicine() {
    $.ajax({
        type: "GET",
        url: URL,
        dataType: 'json',
        data: {
            get_param: 'medicine_info'
        },
        success: function (data) {
            let medicine_name = document.getElementById('txt').value;
            let num = document.getElementById('num').value;
            if (data.length > 0) {
                // 获取所有的药品名
                for (let i = 0; i < data.length; i++) {
                    if (data[i]["medicine_name"] === medicine_name) {
                        if ((/(^[1-9]\d*$)/.test(num))) {
                            addMedicine(data[i], num);
                            document.getElementById('txt').value = '';
                            document.getElementById('num').value = '';
                            return;
                        } else {
                            submitToastr('药品数量不是正整数', '药品数量错误！', 'error');
                            return;
                        }
                    }
                }
                submitToastr('药品不存在', '药品名称错误！', 'error');

            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            // 状态码
            alert(XMLHttpRequest.status);
        }
    });
}

// 添加药品
function addMedicine(medicine_obj, medicine_num) {
    console.log(medicine_obj)
    // 药品行
    let $medicine_tr = $('<tr></tr>');
    // 在药品行中添加药品id和药品数量medicine_num
    $medicine_tr.attr('data-medicine-no', medicine_obj.medicine_info_id);
    $medicine_tr.attr('data-medicine-num', medicine_num);
    $medicine_tr.attr('name', 'medicine');
    // 药品名列
    let $medicine_name_td = $('<td></td>');
    $medicine_name_td.text(medicine_obj.medicine_name);
    // 药品数量列
    let $medicine_num_td = $('<td></td>');
    $medicine_num_td.text(medicine_num);
    // 药品单价列
    let $medicine_price_td = $('<td></td>');
    $medicine_price_td.text(medicine_obj.retail_price);
    // 药品总价列
    let $medicine_total_price = $('<td></td>');
    let total_price = parseFloat(medicine_obj.retail_price) * medicine_num;
    total_price = parseFloat((total_price.toFixed(2)));
    $medicine_total_price.text(total_price);
    $medicine_total_price.attr('name', 'total_price');
    let $medicine_delete_td = $('<td></td>');
    $medicine_delete_td.append(
        '<a onclick="deleteMedicine(this)" data-toggle="tooltip" data-placement="top" title="Close"><i class="fa fa-close color-danger"></i></a>'
    );
    $medicine_tr.append(
        $medicine_name_td, $medicine_num_td, $medicine_price_td,
        $medicine_total_price, $medicine_delete_td
    );
    $('#medicine_tbody').append($medicine_tr);
    medicineTotalPrice();
}

// 删除药品
function deleteMedicine(event) {
    $(event).parent().parent().remove();
    medicineTotalPrice();

}

// 计算总价
function medicineTotalPrice() {
    copyMedicine();
    let total_prices = document.getElementsByName('total_price');
    let total = 0;
    for (let i = 0; i < total_prices.length; i++) {
        total += parseFloat(total_prices[i].innerText);
    }
    $("#medicine_count").text(total.toFixed(2));
    $('#medicine_copy_total_price').text(total.toFixed(2));
}

// 提交提示框
function submitToastr(content, title, status) {
    let func = toastr.info
    if (status === 'success') {
        func = toastr.error;
    } else if (status === 'error') {
        func = toastr.error;
    }
    func(content, title, {
        positionClass: "toast-top-center",
        timeOut: 5e3,
        closeButton: !0,
        debug: !1,
        newestOnTop: !0,
        progressBar: !0,
        preventDuplicates: !0,
        onclick: null,
        showDuration: "300",
        hideDuration: "1000",
        extendedTimeOut: "1000",
        showEasing: "swing",
        hideEasing: "linear",
        showMethod: "fadeIn",
        hideMethod: "fadeOut",
        tapToDismiss: !1
    })
}

// 复制药品结果到患者账单处
function copyMedicine() {
    $('#medicine_copy_tbody').empty();
    let medicine_tbody = document.getElementById('medicine_tbody');
    let all_medicines = medicine_tbody.childNodes;
    for (let i = 0; i < all_medicines.length; i++) {
        let $tr = $('<tr></tr>');
        let all_td = all_medicines[i].childNodes;
        for (let j = 0; j < all_td.length - 1; j++) {
            let $td = $('<td></td>');
            $td.text(all_td[j].innerText);
            $tr.append($td);
        }
        $('#medicine_copy_tbody').append($tr);
    }
}

// 复制检查项目到患者账单
function copyInspection(event) {
    let $event = $(event);
    // 检查类型
    let inspection_type = $($event).data('type');
    // 检查名称
    if ($('#inspection_cost_body').find('[name=' + inspection_type + ']').html()) {
        $('#inspection_cost_body').find('[name=' + inspection_type + ']').remove();
    }
    $event.find('option:selected').each(function (i, val) {
        let inspection_name = $(val).data('name');
        let inspection_price = $(val).data('price');

        console.log(inspection_name);
        console.log(inspection_type);
        console.log(inspection_price);

        let $tr = $("<tr></tr>");
        $tr.attr('name', inspection_type);
        let $inspection_type_td = $('<td></td>');
        $inspection_type_td.text(inspection_type);

        let $inspection_name_td = $('<td></td>');
        $inspection_name_td.text(inspection_name);

        let $inspection_price_td = $('<td></td>');
        $inspection_price_td.attr('name', 'inspection_price');
        $inspection_price_td.text(inspection_price);

        $tr.append($inspection_type_td);
        $tr.append($inspection_name_td);
        $tr.append($inspection_price_td);

        $('#inspection_cost_body').append($tr);
    })
    inspectionTotalPrice();
}

// 计算检查检验总价
function inspectionTotalPrice() {
    let total_price = 0;
    let all_inspection_prices = document.getElementsByName('inspection_price');
    // console.log(all_inspection_prices);
    for (let i = 0; i < all_inspection_prices.length; i++) {
        total_price += parseFloat(all_inspection_prices[i].innerText);
    }

    // total_price += parseFloat();
    $('#inspection_count').text(total_price.toFixed(2));

}

//region 提交函数
// 病历首页提交
function PostHisTorySheet(csrf_token) {
    if ($('#no').attr('placeholder') === undefined) {
        submitToastr('提交失败！', '您未选择病人', 'error')
        return;
    }

    let data = $('#history_sheet_form').serialize();
    console.log("病历首页form信息");
    console.log(data);
    $.ajax({
        type: "POST",
        url: URL,
        data: data,
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        },
        success: function (callback) {
            if (callback.status === -1) {
                submitAlert('提交失败', callback.message, 'error');
            } else {
                submitAlert("提交成功", callback.message, "success");
                init_style('#history_sheet_form');
            }
        },
        error: function (data) {
            alert("异常！");
            console.log(data);
        }
    });
}

// 药品提交(ajax post)
function PostMedicine(csrf_token) {
    if ($('#no').attr('placeholder') === undefined) {
        submitToastr('提交失败！', '您未选择病人', 'error')
        return;
    }
    let all_medicine = document.getElementsByName('medicine');
    let medical_advice = $('#medical_advice').val();
    let regis_id = $('#regis_id').val();
    let medicine_quantity = [];
    let medicine_info_id = []
    for (let i = 0; i < all_medicine.length; i++) {
        medicine_info_id.push(all_medicine[i].dataset['medicineNo']);
        medicine_quantity.push(all_medicine[i].dataset['medicineNum']);
    }

    let data = {
        'medicine_info_id[]': medicine_info_id, // 药品信息
        'medicine_quantity[]': medicine_quantity, // 药品信息
        'post_param': 'medicine', // 提交内容类型判断
        'medical_advice': medical_advice,
        'regis_id': regis_id
    }
    // console.log(data);
    $.ajax({
        url: URL,
        type: 'POST',
        data: data,
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        },
        success: function (callback) {
            if (callback.status === -1) {
                submitAlert("提交失败", callback.message, "error");
            } else {
                submitAlert("提交成功", callback.message, "success");
                init_style('#medical_advice_form')
            }
        },
        error: function (callback) {
            alert('提交失败');
            console.log(callback);
        }
    })
}

// 检查检验提交
function PostInspectionItem(csrf_token) {
    if ($('#no').attr('placeholder') === undefined) {
        submitToastr('提交失败！', '您未选择病人', 'error')
        return;
    }
    let data = $('#inspection_form').serialize();
    console.log(data);
    $.ajax({
        type: 'POST',
        url: URL,
        data: data,
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        },
        success: function (callback) {
            if (callback.status === -1) {
                submitAlert("提交失败", callback.message, "error");
                return;
            }
            submitAlert("提交成功", callback.message, "success");
            $('.swal2-confirm').attr('onblur', 'window.location.reload()');
            init_style('#inspection_form');
        },
        error: function (callback) {
            alert('提交失败');
        }
    })
}

// 诊断结果提交
function PostDiagnosisResults(csrf_token) {
    if ($('#no').attr('placeholder') === undefined) {
        submitToastr('提交失败！', '您未选择病人', 'error')
        return;
    }
    let data = $('#diagnosis_results_form').serialize();
    console.log(data);
    $.ajax({
        type: 'POST',
        url: URL,
        data: data,
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        },
        success: function (callback) {
            if (callback.status === -1) {
                submitAlert("提交失败", callback.message, "error");
                return;
            } else {
                submitAlert("提交成功", callback.message, "success");
                init_style('#diagnosis_results_form');
            }
        },
        error: function (callback) {
            alert('提交失败');
            console.log(callback);
        }
    })
}

// 确诊结果提交
function diagnosis_over() {
    let regis_id = $('#no').attr('placeholder');
    if (regis_id === undefined) {
        submitAlert('提交失败', '您未选择病人', 'error');
        return;
    }
    $.ajax({
        type: 'GET',
        url: URL,
        data: {
            get_param: 'diagnosis_over',
            regis_id: regis_id
        },
        success: function (callback) {
            if (callback.status === -1) {
                submitAlert('提交失败', callback.message, 'error');
                return;
            }
            submitAlert('提交成功', callback.message, 'success');
            $('.swal2-confirm').attr('onblur', 'window.location.reload()');
        },
        error: function () {
            alert('诊疗结束失败');
        }
    })
}

// 这里应该整一个document.ready，表示页面加载完毕后应该执行的操作，而不应该独立的放在这执行
/* window.setInterval(query_waiting_diagnosis_patients, 10000);
window.setInterval(QueryInDiagnosisPatient, 10000);*/
query_waiting_diagnosis_patients()
QueryInDiagnosisPatient()

