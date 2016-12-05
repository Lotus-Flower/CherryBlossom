$(function(){
	$.ajax({
		url: '/searchResults',
		type: 'GET',
		success: function(response){
			console.log(response);
			response = jQuery.parseJSON(response)
			$('#searchBar').autocomplete({source:response});
			$('#searchBar').autocomplete("option", "appendTo", ".navbar");
		},
		error: function(error){
			console.log(error);
		}
	});
});