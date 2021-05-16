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

// 医嘱处理查询
function QueryMedicalAdviceProcess(patient_id) {
    let URL = '/NurseAPI';
    console.log(URL);
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            patient_id: patient_id,
            information: 'MEDICAL_ADVICE_QUERY'
        },
        success: function (data) {
            console.log(data);/** */
            document.getElementById("MedicalAdviceProcess").click();
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);/** */
        },
    })
}

// 住院患者查询
function QueryInpatients() {
    let URL = '/NurseAPI';
    console.log(URL);
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            information: 'INPATIENTS_QUERY'
        },
        success: function (data) {
            console.log(data);/** */
            for (let i = 0; i < data.length; i++) {
                let patient = data[i];
                let td = StringFormat('<td>{0}</td>', patient.name);
                let pid = patient.pid
                console.log(pid)/** */
                let tr = $("<tr onclick='QueryMedicalAdviceProcess(this.pid)'></tr>");
                tr.append(td);
                $("#Inpatients").append(tr);
            }
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);/** */
        }
    });
}

// 待收患者查询
function QueryWaitingPatients() {
    let URL = '/NurseAPI';
    console.log(URL);
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            d_no: '000000',
            information: 'WAITING_QUERY'
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
                $("#WaitingPatients").append(tr);
            }
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        }
    });
}

// 患者入院登记基础信息查询
function QueryRegisterPatient(p_no) {
    let URL = '/NurseAPI';

    console.log(URL);/** */
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            patient_id: patient_id,
            information: 'REGISTER_QUERY'
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

QueryInpatients()
QueryWaitingPatients()

// 床位选择
function BedSelect() {
    let BED = $("input[name='CW']:checked").val();
    console.log(document.getElementById('AreaBed')); /**/
    if (BED !== undefined) {
        document.getElementById('AreaBed').value = BED;
    } else {
        document.getElementById('AreaBed').value = '';
    }
}

// 可用床位查询
function QueryBed() {
    let URL = '/NurseAPI';
    $.ajax({
        type: "get",
        url: URL,
        dataType: 'json',
        data: {
            information: 'BED_QUERY'
        },
        success: function (data) {
            $("#areas").empty();
            // 生成病区分页按钮
            for (let i in data) {
                let format_str = '<li class="nav-item"><a href="#{0}" class="nav-link {1}" data-toggle="tab" aria-expanded="false">病区{0}</a></li>'
                is_active = ''
                if (i == 0) {
                    is_active += 'active ';
                }
                let areas = StringFormat(format_str, data[i].AREA, is_active)
                $("#areas").append(areas)
            }
            $("#beds").empty();
            // 生成病区分页页面
            for (let i in data) {
                // 床位 labels
                let labels_html = ''
                let format_str_inside = '<label class="radio-inline mr-3"><input type="radio" value="{0}{1}" name="BED">{0}{1}</label>'
                for (let bed in data[i].BED) {
                    labels_html += StringFormat(format_str_inside, data[i].AREA, bed)
                }
                // 床位 html
                let format_str = '<div id="{0}" class="tab-pane fade {1}"><div class="card-body"><div class="form-group mb-0">{2}</div></div></div>'
                is_active = ''
                if (i == 0) {
                    is_active += 'show active'
                }
                let beds = StringFormat(format_str, data[i].AREA, is_active, labels_html)
                $("#beds").append(beds);
            }
        },
        error: function (err) {
            alert("请求服务器失败！");
            console.log(err);
        }
    });
}
