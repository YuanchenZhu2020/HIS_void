// 病历首页 Ajax 查询
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
            console.log(data);
            // document.getElementById("HZZS").setAttribute('placeholder', data.HZZS);
            document.getElementById("HZZS").value = data.HZZS;
            document.getElementById("ZLQK").setAttribute('placeholder', data.ZLQK);
            document.getElementById("JWBS").setAttribute('placeholder', data.JWBS);
            document.getElementById("GMBS").setAttribute('placeholder', data.GMBS);
            document.getElementById("TGJC").setAttribute('placeholder', data.TGJC);
            document.getElementById("FBSJ").setAttribute('placeholder', data.FBSJ);
            document.getElementById("no").setAttribute('placeholder', data.no);
            document.getElementById("name").setAttribute('placeholder', data.name);
            document.getElementById("gender").setAttribute('placeholder', data.gender);
            document.getElementById("age").setAttribute('placeholder', data.age);
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        },
    })
}

// 查询待诊患者
function QueryZZHZ() {
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
            alert('弹出对话框.');
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
function QueryDZHZ() {
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
            alert('弹出对话框.');
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
function QueryJCJG(p_no) {
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
