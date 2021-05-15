// 医生信息
function QueryGH(date, KS_id) {
    let URL = '/PatientViewAPI';
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            information: 'GH',
            KS_id: KS_id,
            date: date,
        },
        success: function (data) {
            alert('弹出对话框.');
            for (let i = 0; i < data.length; i++) {
                let ghinfo = data[i];
                let td0 = '<td>' + ghinfo.doctor_name + '</td>';
                let td1 = '<td>' + ghinfo.AM + '</td>';
                let td2 = '<td>' + ghinfo.PM + '</td>';
                // let p_no = patient.p_no
                // console.log(p_no)
                let tr1 = $("<tr></tr>"); // onclick='QueryBLSY(this.p_no)
                tr1.append(td0);
                tr1.append(td1);
                tr1.append(td2);
                console.log(tr1);
                $("#GH").append(tr1);
                // console.log(tr);
                // console.log($("#GH"));
                // $("#GH").append(tr);
                // console.log($("#GH"));

            }
        },
        error: function (err) {
            alert("请求服务器失败！");
        }
    });
}