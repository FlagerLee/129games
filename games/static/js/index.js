jQuery(document).ready(function($) {
	console.log('hello, world!')
});

$('#originpic').change(function() {
	var formdata = new FormData();
	var file_name = $(this).val().split("\\").pop();
	var file_content = $(this)[0].files[0];
	formdata.append('name', file_name);
	formdata.append('content', file_content);
	$.ajax({
		url: "/index/",
		type: "POST",
		processData: false,
		contentType: false,
		data: formdata,
		success: function(data){
			console.log('ajax success!');
			content = JSON.parse(data);
			console.log(content['img_path']);
			console.log(content['new_img_path'])
			$('#img_origin').attr('src', content['img_path']);
			$('#img_new').attr('src', content['new_img_path']);
		}
	});
})

$('#cro').cropper({
	aspectRatio: 1,
	viewmode: 1,
	preview: '#preview',
	crop: function (e) {
		console.log(e);
	}
});