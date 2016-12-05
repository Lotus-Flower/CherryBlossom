$(document).ready(function(){
	$('.comment-form-control').val("");
});


$('.comment-form-control').keyup(function(event){
	if(event.keyCode == 13){
		var commentID = $(this).closest('form').attr('id');
		var arrayCommentID = commentID.split('-');
		var tweetIndex = parseInt(arrayCommentID[2]);

		var body = $(this).val();
		var name = $('#profileName').text();
		var username = $('#profileUser').text();
		var usernameParameter = String(username).substring(1);
		var gravatar = $('.testImg').attr('src');
		var dt = new Date();
		var time = dt.getHours() + ":" + dt.getMinutes() + ":" + dt.getSeconds();

		var infoJSON = {index : tweetIndex, body : body};
		$.ajax({
			url: '/storeComment',
			data: JSON.stringify(infoJSON),
			dataType: 'json',
			contentType: 'application/json; charset=utf-8',
			type: 'POST',
			success: function(response) {
				console.log(response);
				$('#placeholderRow' + tweetIndex).before('<div class="row commentRow"><span class="col-md-1 testImgContainer"><img class="img-responsive testImg" src="' + gravatar + '"></span><span class="col-md-11"><a class="nickname" href="/profile/' + usernameParameter + '"><span>' + name + '</span></a><span class="timestamp"> - @' + usernameParameter + ': ' + time + '</span></span><span class="col-md-11"><p id="modalTweet">' + body + '</p></span></div>');
			},
			error: function(error) {
				console.log(error);
			}
		});
		$('.comment-form-control').val("");
		$('.comment-form-control').blur();
	}
});

