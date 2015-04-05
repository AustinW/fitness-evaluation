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
	function changeView(event, data) {

		$('#rankings-table').fadeOut();
		$('#rankings-table-spinner').fadeIn();

		$('#graph').html('<i class="fa fa-spinner fa-5x fa-spin"></i>');

		var params = {};
		if (data.category)
			params.category = data.category

		getResults(data.worksheet, params, $('#rankings-table').find('tbody'));

		var url = '/week/' + data.worksheet + '/graph?' + $.param(params);

		$.get(url, function(response) {
			$('#graph').html('<a href="' + url + '" target="_blank">' + response + '</a>');
		});
	}

	// create function to retrieve the information
	function getResults(worksheetId, params, table) {

		var paramStr = $.param(params);
		
		$.getJSON('/week/' + worksheetId + '.json?' + paramStr).done(function(response) {

			table.empty();
			
			// Populate results table
			$.each(response, function showResults(index, data) {
				table.append('<tr><td>' + (index + 1) + '</td><td>' + data['athlete']['name'] + '</td><td>' + data['score'] + '</td></tr>');
			});

			$('#rankings-table').fadeIn();
			$('#rankings-table-spinner').fadeOut();
		}).fail(function(response) {
			showError(response.responseJSON.message);
		});
	}

	function showError(msg) {
		$('.error-display').find('.error-message').html(msg);
		$('.error-display').fadeIn();
	}

	urlSegments = window.location.pathname.split('/');
	console.log(urlSegments[urlSegments.length - 1]);

	// Initialize with overall results
	if ($('#graph').length) {
		changeView(null, {
			worksheet: urlSegments[urlSegments.length - 1]
		});
	}

	$('#category-selector').on('changed.fu.selectlist', changeView);
});