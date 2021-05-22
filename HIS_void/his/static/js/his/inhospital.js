// function QueryBLSY(p_no) {
//     let URL = '/InhospitalAPI';
//
//     $.ajax({
//         type: "get",
//         url: URL,
//         dataType: 'json',
//         data: {
//             p_no: p_no,
//             information: 'BLSY'
//         },
//         success: function (data) {
//             // console.log(data);
//             // document.getElementById("HZZS").setAttribute('placeholder', data.HZZS);
//             // document.getElementById("ZLQK").setAttribute('placeholder', data.ZLQK);
//             // document.getElementById("JWBS").setAttribute('placeholder', data.JWBS);
//             // document.getElementById("GMBS").setAttribute('placeholder', data.GMBS);
//             // document.getElementById("TGJC").setAttribute('placeholder', data.TGJC);
//             // document.getElementById("FBSJ").setAttribute('placeholder', data.FBSJ);
//             // document.getElementById("no").setAttribute('placeholder', data.no);
//             // document.getElementById("name").setAttribute('placeholder', data.name);
//             // document.getElementById("gender").setAttribute('placeholder', data.gender);
//             // document.getElementById("age").setAttribute('placeholder', data.age);
//         },
//         error: function (err) {
//             alert("请求服务器失败！");
//             console.log(err);
//         },
//     })
// }s
//
// // 查询诊中患者
// // function QueryZZHZ() {
// //     let URL = '/InhospitalAPI';
// //     console.log(URL);
// //     $.ajax({
// //         type: "get",
// //         url: URL,
// //         dataType: 'json',
// //         data: {
// //             d_no: '000000',
// //             information: 'ZZHZ'
// //         },
// //         success: function (data) {
// //             alert('诊中患者.');
// //             console.log(data);
// //             for (let i = 0; i < data.length; i++) {
// //                 let patient = data[i];
// //                 let td = '<td>' + patient.name + '</td>';
// //                 let td1 = '<td>' + patient.bed + '</td>';
// //                 let p_no = patient.p_no
// //                 console.log(p_no)
// //                 let tr = $("<tr onclick='alert(123)'></tr>");  //QueryBLSY(this.p_no)
// //                 tr.append(td);
// //                 tr.append(td1);
// //                 $("#ZZHZ").append(tr);
// //             }
// //         },
// //         error: function (err) {
// //             alert("请求服务器失败！");
// //             console.log(err);
// //         }
// //     });
// // }
//
// // 查询出院患者
// function QueryCYHZ() {
//     let URL = '/InhospitalAPI';
//     console.log(URL);
//     $.ajax({
//         type: "get",
//         url: URL,
//         dataType: 'json',
//         data: {
//             d_no: '000000',
//             information: 'CYHZ'
//         },
//
//         success: function (data) {
//             console.log(URL);
//             alert('出院患者.');
//             console.log(data);
//             // for (let i = 0; i < data.length; i++) {
//             //     let patient = data[i];
//             //     let td = '<td>' + patient.name + '</td>';
//             //     let td1 = '<td>' + patient.status + '</td>';
//             //     let p_no = patient.p_no
//             //     console.log(p_no)
//             //     let tr = $("<tr onclick='alert(333)''></tr>");
//             //     tr.append(td);
//             //     tr.append(td1);
//             //     $("#CYHZ").append(tr);
//             // }
//         },
//         error: function (err) {
//             console.log(URL);
//             alert("请求服务器失败！");
//             console.log(err);
//         }
//     });
//     // self.location = '#jian_cha_jian_yan'  //这个又是什么吖
// }
//
// // QueryZZHZ()
// // QueryCYHZ()