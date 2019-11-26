jQuery(document).ready(function($) {
	console.log('hello, world!')
});

$('#originpic').change(function() {
	var formdata = new FormData();
	/*
	console.log(typeof($('#originpic').val()));
	console.log($('#originpic').val());
	var file = $(this)[0].files;
	console.log(RegExp.test(file[0].name.toLowerCase()));
	*/
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
		}
	});
})