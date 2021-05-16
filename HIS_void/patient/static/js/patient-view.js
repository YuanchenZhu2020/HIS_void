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
                console.log(data);
                let ghinfo = data[i];
                let td = '<td>' + ghinfo.doctor_name + '</td>';
                let td1 = '<td>' + btn_registration(ghinfo.AM, KS_id, date, 1, ghinfo)  + '</td>';
                let td2 = '<td>' + btn_registration(ghinfo.PM, KS_id, date, 2, ghinfo) + '</td>'
                let tr = $("<tr></tr>");
                tr.append(td);
                tr.append(td1);
                tr.append(td2);
                $("#" + KS_id + '_' + date).append(tr);
            }
        }
        ,
        error: function (err) {
            alert("请求服务器失败！");
        }
    });
}


function btn_registration(remain, KS_id, date, time, ghinfo) {
    let btn = '<button onclick="get_regis_info('+KS_id + ','+ date+',' +1 + ',' +  ghinfo + ')" type="button" class="btn btn-outline-success tp-btn-light" data-toggle="modal" data-target="#GHask">'
    btn += remain;
    btn += '</button>';
    console.log(btn)
    return btn;
}

/*
function get_regis_info(KS_id, date, time, ghinfo) {
    console.log(KS_id);
    console.log(date);
    console.log(time);
    console.log(ghinfo);
    let id_to_name = ["内科", "呼吸科", "小儿科", "牙科", "精神科", "外科"]
    let AMs_PM = ["上午", "下午"]
    $("#modal-body").empty();
    note = "您挂的号是："+date + AM_PM[time - 1] + id_to_name[KS_id + 1] + "的" + ghinfo.name
    console.log(note)
    $("#modal-body").append()
}*/
