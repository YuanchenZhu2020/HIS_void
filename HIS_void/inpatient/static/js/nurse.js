// 医嘱处理查询
function QueryYZCL(p_no) {
    let URL = '/NurseAPI';
    console.log(URL);
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            p_no: p_no,
            information: 'YZCL'
        },
        success: function (data) {
            console.log(data);
            document.getElementById("YZCL_a").click();
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        },
    })
}

// 住院患者查询
function QueryZYHZ() {
    let URL = '/NurseAPI';
    console.log(URL);
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            d_no: '000000',
            information: 'ZYHZ'
        },
        success: function (data) {
            console.log(data);
            for (let i = 0; i < data.length; i++) {
                let patient = data[i];
                let td = '<td>' + patient.name + '</td>';
                let p_no = patient.p_no
                console.log(p_no)
                let tr = $("<tr onclick='QueryYZCL(this.p_no)'></tr>");
                tr.append(td);
                $("#ZYHZ").append(tr);
            }
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        }
    });
}

// 待收患者查询
function QueryDSHZ() {
    let URL = '/NurseAPI';
    console.log(URL);
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            d_no: '000000',
            information: 'DSHZ'
        },
        success: function (data) {
            console.log(data);
            for (let i = 0; i < data.length; i++) {
                let patient = data[i];
                let td = '<td>' + patient.name + '</td>';
                let p_no = patient.p_no
                console.log(p_no)
                let tr = $("<tr onclick='QueryRYDJ(this.p_no)'></tr>");
                tr.append(td);
                $("#DSHZ").append(tr);
            }
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        }
    });
}

// 入院登记查询
function QueryRYDJ(p_no) {
    let URL = '/NurseAPI';

    console.log(URL);
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            p_no: p_no,
            information: 'RYDJ'
        },
        success: function (data) {
            console.log(data);
            document.getElementById("no").setAttribute('placeholder', data.no);
            document.getElementById("name").setAttribute('placeholder', data.name);
            document.getElementById("gender").setAttribute('placeholder', data.gender);
            document.getElementById("age").setAttribute('placeholder', data.age);
            document.getElementById("RYDJ_a").click();
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        },
    })
}

QueryDSHZ()
QueryZYHZ()

// 床位查询
function QueryCWXZ() {
    let CW = $("input[name='CW']:checked").val();
    console.log(document.getElementById('BQCW'));
    if (CW !== undefined) {
        document.getElementById('BQCW').value = CW;
    } else {
        document.getElementById('BQCW').value = '';
    }
}

// 床位信息
function QueryCWXX() {
    let URL = '/NurseAPI';
    console.log(URL);
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            d_no: '000000',
            information: 'CWXX'
        },
        success: function (data) {
            alert("查询成功");
            $("#BQ_head").empty();
            // 生成病区分页按钮
            for (let i in data) {
                BQ_html = '';
                BQ_html += '<li class="nav-item"> ';
                BQ_html += '<a href="#' + data[i].BQ + '"';
                BQ_html += ' class="nav-link ';
                if (i == 0) {
                    BQ_html += 'active ';
                }
                BQ_html += '" ' + 'data-toggle="tab" aria-expanded="false">病区' + data[i].BQ;
                BQ_html += '</a></li>'
                $("#BQ_head").append(BQ_html);
            }
            $("#BQ_content").empty();
            // 生成病区分页页面
            for (let i in data) {
                let content_html = '';
                content_html += '<div id="' + data[i].BQ + '"';
                content_html += 'class="tab-pane fade ';
                if (i == 0) {
                    content_html += 'show active'
                }
                content_html += '">';
                content_html += '<div class="card-body"><div class="form-group mb-0">';
                for (let CW in data[i].CW) {
                    content_html += '<label class="radio-inline mr-3">';
                    content_html += '<input type="radio" value="';
                    content_html += data[i].BQ + CW + '" name="CW">';
                    content_html += data[i].BQ + CW + '</label>'
                }
                content_html += "</div></div></div>"
                $("#BQ_content").append(content_html);
            }
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        }
    });
}
