// 检验信息 Ajax 查询
function JianYanXinXi(p_no) {
    let URL = '/InspectionAPI';

    console.log(URL);
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            p_no: p_no,
            information: 'InspectingInformation'
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

// 待检患者 Ajax 查询
function jqueryInspectingPatient() {
    let URL = '/InspectionAPI';
    console.log(URL);
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            d_no: '000000',
            information: 'InspectingPatient'
        },
        success: function (data) {
            console.log(data);
            for (let i = 0; i < data.length; i++) {
                let patient = data[i];
                let td = '<td>' + patient.name + '</td>';
                let p_no = patient.p_no
                console.log(p_no)
                let tr = $("<tr onclick='JianYanXinXi(this.p_no)'></tr>");
                tr.append(td);
                $("#inspectingPatient").append(tr);
            }
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        }
    });
}

jqueryInspectingPatient()
