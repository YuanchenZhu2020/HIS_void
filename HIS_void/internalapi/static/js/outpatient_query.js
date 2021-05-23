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

// 病历首页查询
function QueryHistorySheet(regis_id) {
    let URL = '/OutpatientAPI';
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
            $("#chief_complaint").text(data.chief_complaint);
            $("#past_illness").text(data.past_illness);
            $("#allegic_history").text(data.allegic_history);
            $("#illness_date").text(data.illness_date);
            $("#no").attr('placeholder', data.no);
            $("#name").attr('placeholder', data.name);
            $("#gender").attr('placeholder', data.gender);
            $("#age").attr('placeholder', data.age);
            $('input[name=regis_id]').each(function (index, value) {
                $(value).val(regis_id);
                console.log(value);
            })
            $("#BLSY_a").click();
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        },
    })
}

// 查询待诊患者
function query_waiting_diagnosis_patients() {
    let URL = '/OutpatientAPI';
    console.log(URL);
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
                let regis_id = patient.regis_id
                let tr = $("<tr onclick='QueryHistorySheet(" + regis_id + ")'></tr>");
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
function QueryZZHZ() {
    let URL = '/OutpatientAPI';
    console.log(URL);
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            d_no: '000000',
            get_param: 'ZZHZ'
        },
        success: function (data) {
            console.log(data);
            for (let i = 0; i < data.length; i++) {
                let patient = data[i];
                let td = '<td>' + patient.name + '</td>';
                let td1 = '<td>' + patient.status + '</td>';
                let p_no = patient.p_no
                console.log(p_no)
                let tr = $("<tr onclick='QueryJCJY(this.p_no)'></tr>");
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
function QueryJCJY(p_no) {
    let URL = '/OutpatientAPI';

    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            p_no: p_no,
            get_param: 'JCJY'
        },
        success: function (data) {
            console.log(data);
            document.getElementById("chief_complaint").setAttribute('placeholder', data.chief_complaint);
            document.getElementById("ZLQK").setAttribute('placeholder', data.ZLQK);
            document.getElementById("past_illness").setAttribute('placeholder', data.past_illness);
            document.getElementById("allegic_history").setAttribute('placeholder', data.allegic_history);
            document.getElementById("TGJC").setAttribute('placeholder', data.TGJC);
            document.getElementById("illness_date").setAttribute('placeholder', data.illness_date);
            document.getElementById("no").setAttribute('placeholder', data.no);
            document.getElementById("name").setAttribute('placeholder', data.name);
            document.getElementById("gender").setAttribute('placeholder', data.gender);
            document.getElementById("age").setAttribute('placeholder', data.age);
            document.getElementById("JCJY_a").click();
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        },
    })
}

// 复制检查结果元素
function copyJCJG() {
    let ss = $('#inspect_content');
    let tt = ss.clone(false);
    $("#MZQZ_id").prepend(tt);
}


/*
* 处方开具页面函数
*/


// 搜索框中查询药品
function QueryMedicine() {
    $.ajax({
        type: "get",
        url: "/OutpatientAPI",
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
            url: "/OutpatientAPI",
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
    $medicine_total_price.text(parseFloat(medicine_obj.price) * medicine_num);
    $medicine_total_price.attr('name', 'total_price');
    let $medicine_delete_td = $('<td></td>');
    $medicine_delete_td.append('<a onclick="deleteMedicine(this)" data-toggle="tooltip" data-placement="top" title="Close"><i class="fa fa-close color-danger"></i></a>');
    $medicine_tr.append($medicine_name_td, $medicine_num_td, $medicine_price_td, $medicine_total_price, $medicine_delete_td);
    $('#medicine_tbody').append($medicine_tr);
    totalPrice();
}

// 删除药品
function deleteMedicine(event) {
    console.log($(event).parent().parent().html());
    $(event).parent().parent().remove();
    totalPrice();

}

// 计算总价
function totalPrice() {
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
    let inspection_type = $($event).attr('name');
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
function inspectionTotalPrice(csrf_token) {
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
function PostHisTorySheet() {
    let data = $('#history_sheet').serializeArray();
    console.log("病历首页form信息");
    $.ajax(
        {
            //几个参数需要注意一下
            type: "POST",//方法类型
            dataType: "json",//预期服务器返回的数据类型
            url: "/outpatientAPI",//url
            data: data,
            success: function (result) {
                alert("ajax提交成功，请使用submitAlert显示提示信息！");
                // submitAlert("提交成功", );
            },
            error: function (data) {
                alert("异常！");
                console.log(data);
            }
        });
}

// 药品提交(ajax post)
function post_medicine(csrf_token, url) {  //由于
    let all_medicine = document.getElementsByName('medicine');
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
        'post_param': 'medicine' // 提交内容类型判断
    }
    console.log(data);
    $.ajax({
        url: url,
        type: 'POST',
        dataType: 'text',
        data: JSON.stringify(data), // 注意这里要将发送的数据转换成字符串
        processData: false,// tell jQuery not to process the data
        contentType: false,// tell jQuery not to set contentType
        beforeSend: function (xhr, setting) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        },
        success: function (callback) {
            // 清空医生选择的药品
            $('#medicine_tbody').empty();
            $('#medicine_copy_tbody').empty();
            $('#medicine_count').text(0.00);
            $('#medicine_copy_total_price').text(0.00);
            submitAlert();
        }, // end success
        error: function (callback) {
            alert('提交失败');
            console.log(callback);
        }
    })
}

// 检查检验提交
function post_inspection(csrf_token, url) {  //由于
    let all_medicine = document.getElementsByName('medicine');
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
        'post_param': 'medicine' // 提交内容类型判断
    }
    console.log(data);
    $.ajax({
        url: url,
        type: 'POST',
        dataType: 'text',
        data: JSON.stringify(data), // 注意这里要将发送的数据转换成字符串
        processData: false,// tell jQuery not to process the data
        contentType: false,// tell jQuery not to set contentType
        beforeSend: function (xhr, setting) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        },
        success: function (callback) {
            // 清空医生选择的药品
            $('#medicine_tbody').empty();
            $('#medicine_copy_tbody').empty();
            $('#medicine_count').text(0.00);
            $('#medicine_copy_total_price').text(0.00);
            submitAlert();
        }, // end success
        error: function (callback) {
            alert('提交失败');
            console.log(callback);
        }
    })
}


// 这里应该整一个document.ready，表示页面加载完毕后应该执行的操作，而不应该独立的放在这执行
query_waiting_diagnosis_patients()
copyJCJG()
QueryZZHZ()

