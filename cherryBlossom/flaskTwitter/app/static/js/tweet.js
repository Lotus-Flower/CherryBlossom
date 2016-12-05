$(document).ready(function(){
	$('#tweetBody').val("");
});

$('#tweetBody').keyup(function(event){
	if(event.keyCode == 13){
		$('#tweetBtn').trigger('click');
	}
});


$('#tweetBtn').click(function() {
	var body = $('#tweetBody').val();
	var name = $('#profileName').text();
	var username = $('#profileUser').text();
	var usernameParameter = String(username).substring(1);
	var gravatar = $('.testImg').attr('src');
	var dt = new Date();
	var time = dt.getHours() + ":" + dt.getMinutes() + ":" + dt.getSeconds();
	$.ajax({
		url: '/storeTweet',
		data: $('form').serialize(),
		type: 'POST',
		success: function(response) {
			console.log(response);
			var obj = jQuery.parseJSON(response)
			$('.firstWrapper').after('<div class="FTWrapper row" data-toggle="modal" data-target="#Modal' + obj.tweetID + '"><div class="row"><span class="col-md-1 testImgContainer"><img class="img-responsive testImg" src="' + gravatar +'"></span><span class="col-md-11"><span class="col-md-11"><a class="nickname" href="/profile/' + usernameParameter + '"><span>' + name + '</span></a><span class="timestamp"> - @' + username + ': ' + time + '</span></span><span class="col-md-11">' + obj.body +'</span><span class="col-md-11 heartRow"><span><button type="button" class="btn btn-clear"><span class="glyphicon glyphicon-heart-empty"></span></button></span><span id="commentButtonSpan"><button type="button" class="btn btn-clear"><span class="glyphicon glyphicon-comment"></span></button></span></span></span></div></div><!-- Modal --><div class="modal fade" id="Modal' + obj.tweetID + '" role="dialog"><div class="modal-dialog"><!-- Modal content--><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal">&times;</button><h4 class="col-md-10 modal-title"><span id="modalNickname">' + name + '</span><span class="timestamp" id="modalTimestamp"> - @' + username + ': ' + time + '</span></h4></div><div class="modal-body"><div class="row modalrow" id="bodyRow"><span class="col-md-2 testImgContainer"><img class="img-responsive testImg" src="' + gravatar + '"></span><span class="col-md-10"><h4 id="modalTweet">' + obj.body + '</h4></span></div></div><div class="modal-footer"></div></div></div></div>');
			$('#noPostsHere').remove();
		},
		error: function(error) {
    		console.log(error);
		}
	});
	$('#tweetBody').val("");
	$('#tweetBtn').blur();
	$('#tweetInfo').text(parseInt($('#tweetInfo').text())+1)
});

