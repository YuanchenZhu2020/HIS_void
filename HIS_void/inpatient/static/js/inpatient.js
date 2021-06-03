(function($) {
	// 表单函数
 	var table = $('#example4').DataTable();

	// 画图函数
	var dzSparkLine = function(){

		let draw = Chart.controllers.line.__super__.draw; //draw shadow
		var lineChart3 = function(){

			if(jQuery('#lineChart_3').length > 0 ){
			const lineChart_3 = document.getElementById("lineChart_3").getContext('2d');

			const lineChart_3gradientStroke1 = lineChart_3.createLinearGradient(500, 0, 100, 0);
			lineChart_3gradientStroke1.addColorStop(0, "rgba(54, 201, 95, 1)");
			lineChart_3gradientStroke1.addColorStop(1, "rgba(54, 201, 95, 0.5)");

			const lineChart_3gradientStroke2 = lineChart_3.createLinearGradient(500, 0, 100, 0);
			lineChart_3gradientStroke2.addColorStop(0, "rgba(54, 157, 201, 1)");
			lineChart_3gradientStroke2.addColorStop(1, "rgba(54, 157, 201, 1)");

			Chart.controllers.line = Chart.controllers.line.extend({
				draw: function () {
					draw.apply(this, arguments);
					let nk = this.chart.chart.ctx;
					let _stroke = nk.stroke;
					nk.stroke = function () {
						nk.save();
						nk.shadowColor = 'rgba(0, 0, 0, 0)';
						nk.shadowBlur = 10;
						nk.shadowOffsetX = 0;
						nk.shadowOffsetY = 10;
						_stroke.apply(this, arguments)
						nk.restore();
					}
				}
			});
			lineChart_3.height = 100;

			// 以上都是相关的配置，在这里修改数据
			new Chart(lineChart_3, {
				type: 'line',
				data: {
					defaultFontFamily: 'Poppins',
					labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
					datasets: [
						{
							label: "收缩压",
							data: [25, 20, 60, 41, 66, 45, 80],
							borderColor: lineChart_3gradientStroke1,
							borderWidth: "2",
							backgroundColor: 'transparent',
							pointBackgroundColor: 'rgba(54, 201, 95, 0.5)'
						}, {
							label: "舒张压",
							data: [5, 20, 15, 41, 35, 65, 80],
							borderColor: lineChart_3gradientStroke2,
							borderWidth: "2",
							backgroundColor: 'transparent',
							pointBackgroundColor: 'rgba(254, 176, 25, 1)'
						}
					]
				},
				options: {
					legend: false,
					scales: {
						yAxes: [{
							ticks: {
								beginAtZero: true,
								max: 100,
								min: 0,
								stepSize: 20,
								padding: 10
							}
						}],
						xAxes: [{
							ticks: {
								padding: 5
							}
						}]
					}
				}
			});
			}
		}
		var areaChart1 = function(){
		//basic area chart
			if(jQuery('#areaChart_1').length > 0 ){
			const areaChart_1 = document.getElementById("areaChart_1").getContext('2d');

			areaChart_1.height = 100;

			new Chart(areaChart_1, {
				type: 'line',
				data: {
					defaultFontFamily: '体温',
					labels: ["week-1", "week-2", "week-3", "week-4", "week-5", "week-6", "week-7"],
					datasets: [
						{
							label: "My First dataset",
							data: [35.5, 36, 36.7, 37, 36, 35.6, 36.5],
							borderColor: 'rgba(0, 0, 1128, .3)',
							borderWidth: "1",
							backgroundColor: 'rgba(54, 201, 95, .5)',
							pointBackgroundColor: 'rgba(0, 0, 1128, .3)'
						}
					]
				},
				options: {
					legend: false,
					scales: {
						yAxes: [{
							ticks: {
								beginAtZero: true,
								max: 40,
								min: 35,
								stepSize: 0.5,
								padding: 10
							}
						}],
						xAxes: [{
							ticks: {
								padding: 5
							}
						}]
					}
				}
			});
		}
			}
		return {
			init:function(){

			},

			load:function(){
				lineChart3();
				areaChart1();
			},

			resize:function(){
				lineChart3();
				areaChart1();
			}
		}

	}();

	jQuery(document).ready(function(){
	});

	jQuery(window).on('load',function(){
		dzSparkLine.load();
		table.load();
	});

	jQuery(window).on('resize',function(){
		dzSparkLine.resize();
		table.resize();
	});

})(jQuery);