jQuery(document).ready(function($) {
	console.log('hello, world!')
});

$('#originpic').change(function() {
	var formdata = new FormData();
	console.log(typeof($('#originpic').val()));
	console.log($('#originpic').val());
	var file = $(this)[0].files;
	console.log(RegExp.test(file[0].name.toLowerCase()));
	/*
	$.ajax({
		url: "/index/",
		datatype: "json",


	})
	*/
})