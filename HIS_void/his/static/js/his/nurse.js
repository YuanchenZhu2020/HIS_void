// 医嘱处理 Ajax 查询
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
            document.getElementById("JianYanMingCheng").setAttribute('placeholder', data.JYMC);
            document.getElementById("KaiJuShiJian").setAttribute('placeholder', data.KJSJ);
            document.getElementById("KaiJuYiShi").setAttribute('placeholder', data.KJYS);
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

// 住院患者 Ajax 查询
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
            alert('住院患者信息已更新');
            console.log(data);
            for (let i = 0; i < data.length; i++) {
                let patient = data[i];
                let td = '<td>' + patient.name + '</td>';
                let p_no = patient.p_no
                console.log(p_no)
                let tr = $("<tr onclick='ZYHZ(this.p_no)'></tr>");
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
// 待收患者 Ajax 查询
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
            alert('待收患者信息已更新');
            console.log(data);
            for (let i = 0; i < data.length; i++) {
                let patient = data[i];
                let td = '<td>' + patient.name + '</td>';
                let p_no = patient.p_no
                console.log(p_no)
                let tr = $("<tr onclick='ZYHZ(this.p_no)'></tr>");
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

QueryDSHZ()
QueryZYHZ()
