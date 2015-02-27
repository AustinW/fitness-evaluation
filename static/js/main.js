function slug(str) {
	str = str.replace(/^\s+|\s+$/g, ''); // trim
	str = str.toLowerCase();

	// remove accents, swap ñ for n, etc
	var from = "ãàáäâẽèéëêìíïîõòóöôùúüûñç·/_,:;";
	var to   = "aaaaaeeeeeiiiiooooouuuunc------";
	for (var i=0, l=from.length ; i<l ; i++) {
		str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
	}

	str = str.replace(/[^a-z0-9 -]/g, '') // remove invalid chars
		.replace(/\s+/g, '-') // collapse whitespace and replace by -
		.replace(/-+/g, '-'); // collapse dashes

	return str;
}

$(function() {

	

	// create function to retrieve the information
	function getResults(params, table) {

		var worksheetId = null;

		if ('worksheetId' in params) {
			worksheetId = params.worksheetId;
			delete params.worksheetId;
		}

		var paramStr = $.param(params);
		
		$.getJSON('/worksheet/' + worksheetId + '.json?' + paramStr, function(response) {
			$.each(response, function showResults(index, data) {
				table.append('<tr><td>' + (index + 1) + '</td><td>' + data['athlete']['name'] + '</td><td>' + data['score'] + '</td></tr>');
			});
		});
	}

	

	$('#category-selector').on('changed.fu.selectlist', function(event, data) {

		var params = {
			worksheetId: data.worksheet,
			category:    data.category
		};
		
		getResults(params, $('#rankings-table').find('tbody'));
	});

	$('a.worksheet-category').click(function(e) {
		
	});
});