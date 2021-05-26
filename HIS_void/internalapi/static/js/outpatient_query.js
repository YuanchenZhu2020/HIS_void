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

// 查询待诊患者的所有需要的信息
function waiting_diagnosis_patient_info(regis_id) {
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            regis_id: regis_id,
            get_param: 'waiting_diagnosis_patient_info',
        },
        success: function (data) {
            // 设置最上面显示的患者信息
            $("#no").attr('placeholder', data.no);
            $("#name").attr('placeholder', data.name);
            $("#gender").attr('placeholder', data.gender);
            $("#age").attr('placeholder', data.age);
            // 给每一个需要提交的表格设置挂号编号
            $("input[name='regis_id']").each(function (i, value) {
                $(value).val(regis_id);
            })
            QueryHistorySheet(regis_id);
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        },
    })
}

// 查询诊中患者所有的需要的信息
function in_diagnosis_patient_info(regis_id) {
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            regis_id: regis_id,
            get_param: 'in_diagnosis_patient_info',
        },
        success: function (data) {
            // 设置最上面显示的患者信息
            $("#no").attr('placeholder', data.no);
            $("#name").attr('placeholder', data.name);
            $("#gender").attr('placeholder', data.gender);
            $("#age").attr('placeholder', data.age);
            // 给每一个需要提交的表格设置挂号编号
            $("input[name='regis_id']").each(function (i, value) {
                $(value).val(regis_id);
            })
            /* 其他需要的信息：
             已经选择的检验项目
             患者账单
            */
            QueryTestResults(regis_id);
            let inspection_items = [
                {
                    'inspect_type_name': '临床检查',
                    'inspect_name': '心肺听诊',
                    'inspect_price': 10.05
                }, {
                    'inspect_type_name': '临床检查',
                    'inspect_name': '肌电图检查',
                    'inspect_price': 130.85
                }, {
                    'inspect_type_name': '生物化学',
                    'inspect_name': '酸溶血试验',
                    'inspect_price': 80.22
                },
            ]
            let $inspection_cost_body = $('#inspection_cost_body');
            $inspection_cost_body.empty();
            for (let i = 0; i < inspection_items.length; i++) {
                let inspect_info = inspection_items[i];
                $inspection_cost_body.append(StringFormat(
                    '<tr style="color: #36c95f;"><td>{0}</td><td>{1}</td><td name="inspection_price">{2}</td></tr>',
                    inspect_info.inspect_type_name,
                    inspect_info.inspect_name,
                    inspect_info.inspect_price
                ))
            }
            inspectionTotalPrice();
            medicine_items = [
                {
                    'medicine_name': '维生素(AD滴剂(伊可新)(1岁以上)(红)',
                    'medicine_num': 2,
                    'medicine_price': 17.01,
                    'medicine_total': 34.02
                }, {
                    'medicine_name': '多维元素片(29)(善存)',
                    'medicine_num': 1,
                    'medicine_price': 30.24,
                    'medicine_total': 30.24
                }
            ]
            let $medicine_cost_body = $('#medicine_tbody');
            $medicine_cost_body.empty();
            for (let i = 0; i < medicine_items.length; i++) {
                let medicine_info = medicine_items[i];
                $medicine_cost_body.append(StringFormat(
                    '<tr style="color: #36c95f;"><td>{0}</td><td>{1}</td><td>{2}</td><td name="total_price">{3}</td><td></td></tr>',
                    medicine_info.medicine_name,
                    medicine_info.medicine_num,
                    medicine_info.medicine_price,
                    medicine_info.medicine_total
                ))
            }
            // 由于这里的计算价格需要先拷贝处方开具的药品信息，而一开始是没有开药的，因此药品会消失
            medicineTotalPrice();
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        },
    })
}

// 病历首页查询
function QueryHistorySheet(regis_id) {
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            regis_id: regis_id,
            get_param: 'BLSY'
        },
        success: function (data) {
            console.log("病历首页数据")
            console.log(data);
            $("#chief_complaint").val(data.chief_complaint);
            $("#past_illness").val(data.past_illness);
            $("#allegic_history").val(data.allegic_history);
            $("#illness_date").attr('placeholder', data.illness_date);
            $("#togo_history_sheet").click();
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        },
    })
}

// 查询待诊患者
function query_waiting_diagnosis_patients() {
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            get_param: 'waiting_diagnosis'
        },
        success: function (data) {
            console.log(data);
            for (let i = 0; i < data.length; i++) {
                let patient = data[i];
                let td = '<td>' + patient.name + '</td>';
                let td1 = '<td>' + patient.gender + '</td>';
                let id = patient.id
                let tr = $("<tr onclick='waiting_diagnosis_patient_info(" + id + ")'></tr>");
                tr.append(td);
                tr.append(td1);
                $("#DZHZ").append(tr);
            }
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        }
    });
}

// 查询诊中患者
function QueryInDiagnosisPatient() {
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            d_no: '000000',
            get_param: 'in_diagnosis'
        },
        success: function (data) {
            console.log(data);
            for (let i = 0; i < data.length; i++) {
                let patient = data[i];
                let td = '<td>' + patient.name + '</td>';
                let td1 = '<td>' + patient.status + '</td>';
                let tr = $(StringFormat("<tr onclick='in_diagnosis_patient_info({0})'></tr>", data.regis_id));
                tr.append(td);
                tr.append(td1);
                $("#ZZHZ").append(tr);
            }
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        }
    });
    self.location = '#jian_cha_jian_yan'
}

// 检查结果查询
function QueryTestResults(regis_id) {

    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            p_no: regis_id,
            get_param: 'test_results'
        },
        success: function (data) {
            alert("检查检验结果查询成功");
            console.log(data);
            let $inspection_text = $('#inspection_text')
            $inspection_text.empty();
            for (let key in data) {
                let $inspection_result_p = $(StringFormat(
                    '<p class="mb-0"><strong>{0}：</strong>{1}</p><hr class="mt-0"/>',
                    key,
                    data[key]
                ));
                $inspection_text.append($inspection_result_p);
            }
            copy_inspection_results();
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        },
    })
}

// 复制检查结果元素
function copy_inspection_results() {
    let inpspection_results_source = $('#inspection_text');
    let inpspction_results_copy = $(inpspection_results_source.clone()).children();
    let inspection_position = $("#inspection_text_copy");
    inspection_position.empty();
    inspection_position.append(inpspction_results_copy);
}


//region 处方开具所有函数
// 搜索框中查询药品
function QueryMedicine() {
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        cache: true,
        data: {
            get_param: 'CFKJ'
        },
        success: function (data) {
            if (data.length > 0) {
                let keyWords = [];
                // 获取所有的药品名
                for (let i = 0; i < data.length; i++) {
                    keyWords[i] = data[i]['name'];
                }
                //每次按下抬起时都要先清除一下div以免乜有数据时扔存在div边框
                display_delete();
                let txt = document.getElementById('txt');
                let tempArr = [];//定义临时数组用来存储用户与之相匹配的句子
                let text = txt.value;//获取用户所输入的文本框内容
                for (let i = 0; i < keyWords.length; i++) {
                    if (keyWords[i].indexOf(text) !== -1) {//将用户输入的文本框内容与数组进行比对，输入内容在数组中匹配到，并且开头的值存入临时数组中
                        tempArr.push(keyWords[i]);
                    }
                }
                // console.log(tempArr);
                let dvObj = document.createElement("div");//创建一个div用来放提示的语句
                dvObj.setAttribute('class', 'offset-2 basic-list-group col-md-4');
                document.getElementById("box").appendChild(dvObj);
                dvObj.id = "dv";
                if (txt.value.length === 0 || tempArr.length === 0) {//当文本框中乜有内容或者临时数组中没有元素是将div进行删除
                    display_delete();
                } else {
                    document.getElementById('txt').setAttribute("style", "border-radius: 0.7rem 0.7rem 0 0; border-bottom:none");
                    let ulObj = document.createElement("ul");
                    ulObj.setAttribute('class', 'list-group');
                    dvObj.append(ulObj);
                    for (let i = 0; i < tempArr.length; i++) {//创建临时数组长度个的p元素用来显示提示的语句
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

// 通过点击提示框中<li>元素将药品名添加到input中
function add_name(e) {
    console.log(e)
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
            type: "get",
            url: URL,
            dataType: 'json',
            cache: true,
            data: {
                get_param: 'CFKJ'
            },
            success: function (data) {
                let medicine_name = document.getElementById('txt').value;
                let num = document.getElementById('num').value;
                if (data.length > 0) {
                    // 获取所有的药品名
                    for (let i = 0; i < data.length; i++) {
                        if (data[i]["name"] === medicine_name) {
                            if ((/(^[1-9]\d*$)/.test(num))) {
                                addMedicine(data[i], num);
                                document.getElementById('txt').value = '';
                                document.getElementById('num').value = '';
                                return;
                            } else {
                                numError();
                                return;
                            }
                        }
                    }
                    medicineError();
                }
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                // 状态码
                alert(XMLHttpRequest.status);
            }
        }
    );
}

// 添加药品
function addMedicine(medicine_obj, medicine_num) {
    // 药品行
    let $medicine_tr = $('<tr></tr>');
    // 在药品行中添加药品id和药品数量medicine_num
    $medicine_tr.attr('data-medicine-no', medicine_obj.no);
    $medicine_tr.attr('data-medicine-num', medicine_num);
    $medicine_tr.attr('name', 'medicine');
    // 药品名列
    let $medicine_name_td = $('<td></td>');
    $medicine_name_td.text(medicine_obj.name);
    // 药品数量列
    let $medicine_num_td = $('<td></td>');
    $medicine_num_td.text(medicine_num);
    // 药品单价列
    let $medicine_price_td = $('<td></td>');
    $medicine_price_td.text(medicine_obj.price);
    // 药品总价列
    let $medicine_total_price = $('<td></td>');
    let total_price = parseFloat(medicine_obj.price) * medicine_num;
    total_price = parseFloat((total_price.toFixed(2)));
    $medicine_total_price.text(total_price);
    $medicine_total_price.attr('name', 'total_price');
    let $medicine_delete_td = $('<td></td>');
    $medicine_delete_td.append('<a onclick="deleteMedicine(this)" data-toggle="tooltip" data-placement="top" title="Close"><i class="fa fa-close color-danger"></i></a>');
    $medicine_tr.append($medicine_name_td, $medicine_num_td, $medicine_price_td, $medicine_total_price, $medicine_delete_td);
    $('#medicine_tbody').append($medicine_tr);
    medicineTotalPrice();
}

// 删除药品
function deleteMedicine(event) {
    console.log($(event).parent().parent().html());
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

// 药品数量错误（不是正整数）
function numError() {
    toastr.error("请输入正整数", "药品数量无效！", {
        positionClass: "toast-top-right",
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

// 药品名称错误
function medicineError() {
    toastr.error("请检查药品名是否正确", "药品不存在！", {
        positionClass: "toast-top-right",
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
        let $tr = $('<tr style="color: #36c95f"></tr>');
        let all_td = all_medicines[i].childNodes;
        for (let j = 0; j < all_td.length - 1; j++) {
            let $td = $('<td></td>');
            $td.text(all_td[j].innerText);
            $tr.append($td);
        }
        $('#medicine_copy_tbody').append($tr);
    }
}

//endregion

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

            //

            $('#inspection_cost_body').append($tr);
        }
    )
    inspectionTotalPrice();
}

// 计算检查检验总价
function inspectionTotalPrice() {
    let total_price = 0;
    let all_inspection_prices = document.getElementsByName('inspection_price');
    console.log(all_inspection_prices)
    for (let i = 0; i < all_inspection_prices.length; i++) {
        total_price += parseFloat(all_inspection_prices[i].innerText);
    }

    // total_price += parseFloat();
    $('#inspection_count').text(total_price.toFixed(2));

}

// 病历首页提交
function PostHisTorySheet(csrf_token) {
    let data = $('#history_sheet').serialize();
    console.log("病历首页form信息");
    console.log(data);
    $.ajax({
        type: "POST",
        url: URL,
        data: data,
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        },
        success: function (result) {
            alert("ajax提交成功，请使用submitAlert显示提示信息！");
            submitAlert("提交成功", "患者信息已更新", "success");
            console.log(result);
        },
        error: function (data) {
            alert("异常！");
            console.log(data);
        }
    });
}

// 药品提交(ajax post)
function PostMedicine(csrf_token) {
    let url = '/OutpatientAPI/';
    let all_medicine = document.getElementsByName('medicine');
    let medical_advice = $('#medical_advice').val();
    let regis_id = $('#regis_id').val();
    let medicine_data = [];
    for (let i = 0; i < all_medicine.length; i++) {
        console.log(all_medicine[i].dataset);
        medicine_data.push({
            'medicine_id': all_medicine[i].dataset['medicineNo'],
            'medicine_num': all_medicine[i].dataset['medicineNum']
        });
    }
    let data = {
        'medicine_data': medicine_data, // 药品信息
        'post_param': 'medicine', // 提交内容类型判断
        'medical_advice': medical_advice,
        'regis_id': regis_id
    }
    console.log(data);
    $.ajax({
        url: URL,
        type: 'POST',
        data: data, // 注意这里要将发送的数据转换成字符串
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        },
        success: function (callback) {
            // 清空医生选择的药品
            $('#medicine_tbody').empty();
            $('#medicine_copy_tbody').empty();
            $('#medicine_count').text(0.00);
            $('#medicine_copy_total_price').text(0.00);
            submitAlert('药品提交', '药品提交成功', 'success');
        },
        error: function (callback) {
            alert('提交失败');
            console.log(callback);
        }
    })
}

// 检查检验提交
function PostInspectionItem(csrf_token) {
    let data = $('#inspection_form').serialize();
    console.log(data);
    $.ajax({
        url: URL,
        type: 'POST',
        data: data, // 注意这里要将发送的数据转换成字符串
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        },
        success: function (callback) {
            alert(callback);
        },
        error: function (callback) {
            alert('提交失败');
            console.log(callback);
        }
    })
}

// 诊断结果提交
function PostDiagnosisResults(csrf_token) {
    let data = $('#diagnosis_results_form').serialize();
    console.log(data);
    $.ajax({
        url: URL,
        type: 'POST',
        data: data, // 注意这里要将发送的数据转换成字符串
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        },
        success: function (callback) {
            alert(callback);
        },
        error: function (callback) {
            alert('提交失败');
            console.log(callback);
        }
    })
}


// 这里应该整一个document.ready，表示页面加载完毕后应该执行的操作，而不应该独立的放在这执行
query_waiting_diagnosis_patients()
QueryInDiagnosisPatient()

