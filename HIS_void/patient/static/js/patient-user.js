// 检验信息 Ajax 查询
function Details(quezhen_no) {
    console.log(quezhen_no);
    let URL = '/PatientUserAPI';

    console.log(URL);

    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            p_no: quezhen_no,
            information: 'QZXQ'
        },
        success: function (data) {
            alert("查询成功")
            // 控制台输出 data 信息
            console.log(data);
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        },
    })
}
