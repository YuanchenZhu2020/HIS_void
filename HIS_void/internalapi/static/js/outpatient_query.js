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
function QueryBLSY(patient_id) {
    let URL = '/OutpatientAPI';
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            patient_id: patient_id,
            information: 'BLSY'
        },
        success: function (data) {
            document.getElementById("HZZS").setAttribute('placeholder', data.HZZS);
            document.getElementById("ZLQK").setAttribute('placeholder', data.ZLQK);
            document.getElementById("JWBS").setAttribute('placeholder', data.JWBS);
            document.getElementById("GMBS").setAttribute('placeholder', data.GMBS);
            document.getElementById("TGJC").setAttribute('placeholder', data.TGJC);
            document.getElementById("FBSJ").setAttribute('placeholder', data.FBSJ);
            document.getElementById("no").setAttribute('placeholder', data.no);
            document.getElementById("name").setAttribute('placeholder', data.name);
            document.getElementById("gender").setAttribute('placeholder', data.gender);
            document.getElementById("age").setAttribute('placeholder', data.age);
            document.getElementById("BLSY_a").click();
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        },
    })
}

// 查询待诊患者
function QueryDZHZ() {
    let URL = '/OutpatientAPI';
    console.log(URL);
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            d_no: '000000',
            information: 'DZHZ'
        },
        success: function (data) {
            console.log(data);
            for (let i = 0; i < data.length; i++) {
                let patient = data[i];
                let td = '<td>' + patient.name + '</td>';
                let td1 = '<td>' + patient.status + '</td>';
                let p_no = patient.p_no
                console.log(p_no)
                let tr = $("<tr onclick='QueryBLSY(this.p_no)'></tr>");
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
            information: 'ZZHZ'
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
            information: 'JCJY'
        },
        success: function (data) {
            console.log(data);
            document.getElementById("HZZS").setAttribute('placeholder', data.HZZS);
            document.getElementById("ZLQK").setAttribute('placeholder', data.ZLQK);
            document.getElementById("JWBS").setAttribute('placeholder', data.JWBS);
            document.getElementById("GMBS").setAttribute('placeholder', data.GMBS);
            document.getElementById("TGJC").setAttribute('placeholder', data.TGJC);
            document.getElementById("FBSJ").setAttribute('placeholder', data.FBSJ);
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

QueryZZHZ()
QueryDZHZ()

// 删除提示框，用于选定药品后或者输入框失去焦点后
function display_delete() {
    if (document.getElementById("dv")) {
        document.getElementById("box").removeChild(document.getElementById("dv"));
        $("#txt").attr("style", '');
    }
}

// 通过点击提示框中<li>元素将药品名添加到input中
function add_name(e) {
    console.log(e)
    document.getElementById('txt').value = e.innerText.trim();
    display_delete();
}

// 搜索框中查询药品
function QueryMedicine() {
    $.ajax({
        type: "get",
        url: "/OutpatientAPI",
        dataType: 'json',
        cache: true,
        data: {
            information: 'CFKJ'
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


// 删除药品
function deleteMedicine(e) {
    console.log(e);
    console.log(e.name);
    let tag = document.getElementById(e.name);
//删除
    tag.parentNode.removeChild(tag);
    totalPrice();

}

// 添加药品
function addMedicine(medicine_obj, num) {
    // 选中药品添加的表格body
    let medicine_body = $("#medicine_body");
    tr_html = '<tr id="medicine' + medicine_obj.no + '"><th scope="col">' + medicine_obj.name + '</th>' +
        '<th scope="col">' + num + '</th>' +
        '<th scope="col">' + medicine_obj.price + '</th>' +
        '<th name="total_price" scope="col">' + parseFloat(medicine_obj.price) * parseInt(num) + '</th>' +
        '<td><span>' +
        '<a name="medicine' + medicine_obj.no +
        '" href="javascript:void(0)" onclick="deleteMedicine(this)" data-toggle="tooltip" data-placement="top" title="Close">' +
        '<i class="fa fa-close color-danger"></i></a></span> </td></tr>';

    medicine_body.append(tr_html);
    totalPrice();
}

// 计算总价
function totalPrice() {
    if (document.getElementById("medicine_copy")) {
        document.getElementById("JEXZ").removeChild(document.getElementById("medicine_copy"));
        console.log("删除")
    }
    let total_prices = document.getElementsByName('total_price');
    let total = 0;
    for (let i = 0; i < total_prices.length; i++) {
        total += parseFloat(total_prices[i].innerText);
    }
    $("#medicine_count").text(total);
    copyMedicine();
}

// 添加药品按钮，收集药品名和药品数量
function collect_medicine() {
    $.ajax({
            type: "get",
            url: "/OutpatientAPI",
            dataType: 'json',
            cache: true,
            data: {
                information: 'CFKJ'
            },
            success: function (data) {
                let medicine_name = document.getElementById('txt').value;
                let num = document.getElementById('num').value;
                let medicine;
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


// 复制检查结果元素
function copyJCJG() {
    let ss = $('#inspect_content');
    let tt = ss.clone(false);
    $("#MZQZ_id").prepend(tt);
}

// 复制药品结果到患者账单处
function copyMedicine() {
    let ss = $('#medicine_hole');
    let tt = ss.clone(false);
    tt.attr('id', 'medicine_copy');
    if (document.getElementById("medicine_copy")) {
        document.getElementById("JEXZ").removeChild(document.getElementById("medicine_copy"));
        console.log("删除")
    }
    console.log(tt)
    $("#JEXZ").prepend(tt);
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

copyJCJG()
