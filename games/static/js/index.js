jQuery(document).ready(function($) {
	var code = getRandomCode();
	setCookie(code);
	$('#cro').cropper({
		aspectRatio: 1,
		viewmode: 2,
		scalable: false,
		minCanvasWidth: 200, 
		crop: function (data) {
			console.log(data);
		}
	});
});

function getRandomCode() {
	//生成随机序列号
	return ((new Date()).getTime() * 1000 + Math.round(Math.random() * 1000)).toString();
}

function setCookie(code) {
	time = 1000000; //cookie过期时间
	var expires = "";
	var date = new Date();
	date.setTime(date.getTime() + time * 1000);
	expires = "; expires=" + date.toGMTString();
	document.cookie = "username=" + code + expires + "; path=/;";
}

function getCode() {
	//获取cookie中的code
	var cookie = document.cookie;
	cookie = cookie.split(';')[0];
	cookie = cookie.split('=')[1];
	return cookie;
}

$('#originpic').change(function() {
	var formdata = new FormData();
	var file_content = $(this)[0].files[0];
	var code = getCode();
	formdata.append('content', file_content);
	formdata.append('code', code);
	$.ajax({
		url: "/index/",
		type: "POST",
		processData: false,
		contentType: false,
		data: formdata,
		success: function(data){
			content = JSON.parse(data);
			$("#cro").cropper("replace", content['img_path']);
		}
	});
});

$('#commit').click(function() {
	var cas = $('#cro').cropper('getCroppedCanvas').toDataURL('image/png');
	var formdata = new FormData();
	var file_content = cas;
	var code = getCode();
	formdata.append('content', file_content);
	formdata.append('code', code);
	$.ajax({
		url: "/submit/",
		type: "POST",
		processData: false,
		contentType: false,
		data: formdata,
		success: function(data){
			content = JSON.parse(data);
			$('#img_new').attr('src', content['new_img_path']);
		}
	})
});

$('#download').click(function() {
	//下载处理好的图片
	var cookie = getCode();
	window.open("/download/" + String(cookie))
	var formdata = new FormData();
	formdata.append('code', cookie);
	$.ajax({
		url: "/download/" + String(cookie),
		type: "POST",
		processData: false,
		contentType: false,
	})
});

$(window).on('beforeunload', function() {
	var code = getCode();
	var formdata = new FormData();
	formdata.append('code', code);
	$.ajax({
		url: "/close/",
		type: "POST",
		processData: false,
		contentType: false,
		async: false,
		data: formdata,
	});
})