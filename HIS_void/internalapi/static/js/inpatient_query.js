// 字符串格式化函数
function StringFormat() {
    if (arguments.length === 0)
        return null;
    var str = arguments[0];
    for (var i = 1; i < arguments.length; i++) {
        var re = new RegExp('\\{' + (i - 1) + '\\}', 'gm');
        str = str.replace(re, arguments[i]);
    }
    return str;
}

const URL = '/InpatientAPI/';

// 清除已有的信息
function clear_all_info() {
    $('#history_sheet').empty();
    $('#patient_base_info_form').find('input').each(function (i, tag) {
        $(tag).val('');
    })
    $('#all_history_sheet').empty();
    $('#all_history_inspect').empty();

}

// 清除患者td选中样式
function clear_patient_card_style() {
    $('[name="patient_card"]').each(function (i, tag) {
        $(tag).find('tr').each(function (j, tr) {
            $(tr).removeAttr('style');
        })
    })
}

// 查询住院患者
function queryInhospitalPatient() {
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            'get_param': 'inpatient',
            'area_id': $('#area').data('areaId'),
            'dept_id': $('#dept').data('deptId')
        },
        success: function (data) {
            console.log(data);
            let $inhospital_tbody = $('#inhospital_tbody');
            for (let i = 0; i < data.length; i++) {
                let patient_info = data[i];
                $inhospital_tbody.append(StringFormat(
                    '<tr onclick="{0}"><td>{1}</td><td>{2}</td><td>{3}</td></tr>',
                    StringFormat('queryPatientBaseInfo({0}, this)', patient_info.regis_id),
                    patient_info.patient_name,
                    patient_info.bed_id,
                    patient_info.care_level
                ))
            }
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        }
    });
}

// 查询近期出院患者
function queryRecentlyDischarged() {
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            'get_param': 'recently_discharged',
            'area_id': $('#area').data('areaId'),
            'dept_id': $('#dept').data('deptId')
        },
        success: function (data) {
            console.log(data);
            let $inhospital_tbody = $('#recently_discharged_tbody');
            for (let i = 0; i < data.length; i++) {
                let patient_info = data[i];
                $inhospital_tbody.append(StringFormat(
                    '<tr onclick="{0}"><td>{1}</td><td>{2}</td><td>{3}</td></tr>',
                    StringFormat('queryPatientBaseInfo({0}, this)', patient_info.regis_id),
                    patient_info.patient_name,
                    patient_info.bed_id,
                    patient_info.care_level
                ))
            }
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        }
    });

}

// 查询病人基础信息
function queryPatientBaseInfo(regis_id, event) {
    $.ajax({
        url: URL,
        dataType: 'json',
        data: {'get_param': 'patient_info', 'regis_id': regis_id},
        success: function (data) {
            if ($(event).attr("style")) {
                $(event).removeAttr('style');
                clear_all_info();
                return;
            }
            clear_patient_card_style();
            $(event).attr('style', 'background-color: #d7dae3');
            $('#patient_base_info_form').find('input').each(function (i, tag) {
                console.log(tag);
                $(tag).val(data[i]);
            })
            $('input[name="regis_id"]').each(function (i, tag) {
                $(tag).val($('#regis_id').val());
            })
            queryMedicalAdvice(regis_id);
            queryHistorySheet(regis_id);
            queryHistoryInspection(regis_id);
        }
    })
}

// 查询近期出院患者
queryRecentlyDischarged()

// 查询住院患者
queryInhospitalPatient()

// 医嘱记录查询
function queryMedicalAdvice(regis_id) {
    $.ajax({
        url: URL,
        dataType: 'json',
        data: {'get_param': 'medical_advice', 'regis_id': regis_id},
        success: function (data) {
            data.sort(function (a, b) {
                return b.issue_time - a.issue_time;
            })
            console.log(data);
            let all_history_sheet = $('#all_history_sheet');
            all_history_sheet.empty();
            for (let i = 0; i < data.length; i++) {
                let medicine_info_list = data[i].medicine_info;
                let medical_advice = data[i].medical_advice;
                let issue_time = data[i].issue_time;
                let accordion = '<div class="accordion__item">' +
                    '<div class="accordion__header pb-1 pt-1 collapsed" data-toggle="collapse" data-target="#bordered_no-gutter_' + issue_time + '">' +
                    '<span class="accordion__header--text">' + issue_time + '</span>' +
                    '<span class="accordion__header--indicator style_two"></span>' +
                    '</div>' +
                    '<div id="bordered_no-gutter_' + issue_time + '" class="collapse accordion__body" data-parent="#all_history_sheet">' +
                    '<div class="accordion__body--text row">';
                accordion += '<p class="col-12 pt-0 pb-0 mt-0 mb-0">药品详情</p>'
                for (let j = 0; j < medicine_info_list.length; j++) {
                    accordion += StringFormat(
                        '<p class="text-left offset-1 col-5 pt-1 pb-0 mt-0 mb-0">药品名: {0}</p>' +
                        '<p class="text-center col-6 pt-1 pb-0 mt-0 mb-0">（数量：{1}）</p>',
                        medicine_info_list[j][0],
                        medicine_info_list[j][1]
                    )
                }
                accordion += StringFormat('<p class="col-12 pt-0 pb-0 mt-0 mb-0">医嘱详情</p><p class="offset-1">{0}</p>', medical_advice);
                accordion += '</div></div></div>';
                console.log(accordion)
                all_history_sheet.append($(accordion));
            }
        }
    })
}

// 病历记录查询
function queryHistorySheet(regis_id) {
    $.ajax({
        url: URL,
        dataType: 'json',
        data: {'get_param': 'history_sheet', 'regis_id': regis_id},
        success: function (data) {
            console.log(data);
            $history_sheet = $('#history_sheet');
            $history_sheet.empty();
            $history_sheet.append(StringFormat(
                '<p class="col-12 mb-0">患者主诉：{0}</p><hr class="mt-1"/>' +
                '<p class="col-12 mb-0">发病时间：{1}</p><hr class="mt-1"/>' +
                '<p class="col-12 mb-0">过敏病史：{2}</p><hr class="mt-1"/>' +
                '<p class="col-12 mb-0">既往病史：{3}</p><hr class="mt-1"/>' +
                '<p class="col-12 mb-0">门诊预诊：{4}</p><hr class="mt-1"/>' +
                '<p class="col-12 mb-0">家属电话：{5}</p><hr class="mt-1"/>' +
                '<p class="col-12 mb-0">住院日期：{6}</p><hr class="mt-1"/>',
                data.chief_complaint || '无',
                data.illness_date || '无',
                data.past_illness || '无',
                data.allegic_history || '无',
                data.diagnosis_results || '无',
                data.kin_phone || '无',
                data.reg_date
            ))
        }
    })
}

// 查询历史检查检验记录
function queryHistoryInspection(regis_id) {
    $.ajax({
        url: URL,
        type: 'GET',
        data: {'get_param': 'history_inspect', 'regis_id': regis_id},
        success: function (data) {
            console.log(data)
            let all_history_inspect = $('#all_history_inspect');
            all_history_inspect.empty();
            for (let i = 0; i < data.length; i++) {
                all_history_inspect.append(StringFormat(
                    '<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>',
                    data[i]['issue_time'],
                    data[i]['inspect_name'],
                    data[i]['test_result'],
                ))
            }
        }
    })
}

//region select2插件实现药品选择
$(".ajax-search-medicine").select2({
    ajax: {
        url: URL,
        dataType: 'JSON',
        delay: 250,
        data: function (params) {
            return {
                get_param: 'search_medicines',
                medicine_text: params.term, // search term
                page: params.page || 1
            };
        },
        processResults: function (data, params) {
            params.page = params.page || 1;

            return {
                results: data.items,
                pagination: {
                    more: (params.page * 10) < data.total_count
                }
            };
        },
        cache: true
    },
    placeholder: '输入药品名以搜索',
    escapeMarkup: function (markup) {
        return markup;
    }, // let our custom formatter work
    minimumInputLength: 1,
    templateResult: formatMedicineInfo,
    templateSelection: formatMedicineSelection
});

function formatMedicineInfo(repo) {
    if (repo.loading) {
        return repo.text;
    }

    let markup = StringFormat(
        "<div class='select2-result-repository clearfix'><div class='select2-result-repository__meta'>" +
        "<div class='select2-result-repository__title'>{0}</div>",
        repo.medicine_name
    );
    return markup;
}

function formatMedicineSelection(repo) {
    return repo.medicine_name || repo.text;
}

//endregion

// 点击添加按钮将药品添加到表格中
function add_medicine() {
    let medicine_id = $("select[name='medicine_id']").val();
    let medicine_quantity = $("input[name='medicine_quantity']").val();
    let medicine_name = $("span[class=select2-selection__rendered]").text();
    $.ajax({
        url: URL,
        dataType: 'JSON',
        data: {
            get_param: 'medicine_details',
            medicine_id: medicine_id
        },
        success: function (data) {
            $('#medicine_tbody').append(StringFormat(
                '<tr name="medicine_info" data-medicine-id="{5}" data-medicine-quantity="{6}">' +
                '<td>{0}</td><td>{1}</td><td>{2}</td><td name="medicine_cost">{3}</td><td>{4}</td></tr>',
                medicine_name,
                medicine_quantity,
                data.retail_price,
                parseInt((data.retail_price * medicine_quantity).toFixed(2)),
                '<a onclick="deleteMedicine(this)" data-toggle="tooltip" data-placement="top" title="Close"><i class="fa fa-close color-danger"></i></a>',
                medicine_id,
                medicine_quantity
            ))
            updateMedicineCost();
        }
    });
}

// 删除表格中药品
function deleteMedicine(event) {
    $(event).parent().parent().remove();
    updateMedicineCost()
}

// 更新药品总价
function updateMedicineCost() {
    let total = 0;
    $("td[name='medicine_cost']").each(function (i, tag) {
        total += parseInt($(tag).text());
    })
    $('#medicine_count').text(total);
}

// 提交药品及医嘱
function postMedicalAdvice(csrf_token) {
    let data = {
        'medicine_id': [], // 药品ID
        'medicine_quantity': [], // 药品数量
        'medical_advice': '', // 医嘱
        'regis_id': $('#regis_id').val(),
        'post_param': 'medical_advice' // 参数
    }
    $('tr[name="medicine_info"]').each(function (i, tag) {
        data.medicine_id.push($(tag).data('medicineId'));
        data.medicine_quantity.push($(tag).data('medicineQuantity'));
    })
    data.medical_advice = $('#medical_advice').val();
    $.ajax({
        url: URL,
        type: 'POST',
        data: data,
        dataType: 'JSON',
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        },
        success: function (callback) {
            if (callback.status === 0) {
                submitAlert("提交成功", callback.message, "success");

            } else {
                submitAlert("提交失败", callback.message, "error");

            }
        }
    })
}


// 检查检验提交
function PostInspectionItem(csrf_token) {
    if ($('#regis_id').val() === undefined) {
        submitToastr('提交失败！', '您未选择病人', 'error')
        return;
    }
    let data = $('#inspection_form').serialize();
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
                return;
            }
            submitAlert("提交成功", callback.message, "success");
            $('.swal2-confirm').attr('onblur', 'window.location.reload()');
        },
        error: function (callback) {
            alert('提交失败');
            console.log(callback);
        }
    })
}
