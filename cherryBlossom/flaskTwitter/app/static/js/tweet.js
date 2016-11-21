$(document).ready(function(){
	$('#tweetBody').val("");
});

$('#tweetBtn').click(function() {
	alert("got here");
	var body = $('#tweetBody').val();
	var name = $('#profileName').text();
	var username = $('#profileUser').text();
	var gravatar = $('.testImg').attr('src');
	var dt = new Date();
	var time = dt.getHours() + ":" + dt.getMinutes() + ":" + dt.getSeconds();
	$.ajax({
		url: '/storeTweet',
		data: $('form').serialize(),
		type: 'POST',
		success: function(response) {
    		console.log(response);
    		$('#firstWrapper').after('<div class="FTWrapper row"><div class="row"><span class="col-md-1 testImgContainer"><img class="img-responsive testImg" src="' + gravatar + '"></span><span class="col-md-10 testSpan"><span class="nickname">' + name + '</span><span class="timestamp"> - ' + username + ': ' + time + '</span></span><span class="col-md-10 testSpan">' + response + '</span></div></div>');
		},
		error: function(error) {
    		console.log(error);
		}
	});
	$('#tweetBody').val("");
	$('#tweetBtn').blur();
});

