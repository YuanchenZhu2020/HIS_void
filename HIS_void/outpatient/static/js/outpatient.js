// 病历首页查询
function QueryBLSY(p_no) {
    let URL = '/OutpatientAPI';
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            p_no: p_no,
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

/*
$(document).ready(function () {
    $("#txtSearch").keyup(function () {
        if ($("#txtSearch").val() == "") {
            $("#search-result").hide();
        } else {
            $.ajax({
                type: "get",
                url: "/QueryMZYSView",
                dataType: 'json',
                cache: true,
                data: {
                    information: 'CFKJ'
                },
                success: function (data) {
                    console.log(data);
                    var lists = "<ul class='list-group list-group-flush' style='list-style:none;text-align:left;'>";
                    if (data.length > 0) {
                        for (i = 0; i < data.length; i++) {
                            lists += "<li style='padding: 0px 5px' class='list-group-item' onclick='liClick(this)'>" + data[i].name + "</li>";//遍历出每一条返回的数据
                        }
                        lists += "</ul>";
                        $("#search-result").html(lists).show();//将搜索到的结果展示出来
                    }
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    // 状态码
                    alert(XMLHttpRequest.status);
                }
            })
        }
    });
    $('#txtSearch').keydown(function () {
        $("#search-result").hide();
        $('#search-result').empty();

    })
    $('#search').blur(function () {
        $('#search-result').empty();
    })
});

function liClick(data) {
    $("#search-result").hide();
    $("#txtSearch").val($(data).text());
}
*/

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
    let total_prices = document.getElementsByName('total_price');
    console.log(total_prices);
    let total = 0;
    for (let i = 0; i < total_prices.length; i++) {
        console.log(i);
        total += parseFloat(total_prices[i].innerText);
        console.log(total_prices[i]);
    }
    $("#medicine_count").text(total);
}
