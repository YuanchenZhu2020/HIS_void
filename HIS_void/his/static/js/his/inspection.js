function JianYanXinXi(p_no) {
    let URL = '/QueryInspectingView';

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
            console.log(data);
            document.getElementById("JianYanMingCheng").setAttribute('placeholder', data.JYMC);
            document.getElementById("KaiJuShiJian").setAttribute('placeholder', data.KJSJ);
            document.getElementById("KaiJuYiShi").setAttribute('placeholder', data.KJYS);
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        },
    })
}


function jqueryInspectedPatient() {
    let URL = '/QueryInspectingView';
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
            alert('检中患者信息已更新');
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

jqueryInspectedPatient()
