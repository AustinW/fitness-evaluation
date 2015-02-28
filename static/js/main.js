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

requirejs.config({
  paths: {
    'bootstrap': '//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min',
    'fuelux':    '//www.fuelcdn.com/fuelux/3.5.0/js/fuelux.min',
    'jquery':    '//code.jquery.com/jquery-2.1.3.min',
    'moment':    '//cdnjs.cloudflare.com/ajax/libs/moment.js/2.9.0/locales.min'
  },
  // Bootstrap is a "browser globals" script :-(
  shim: { 'bootstrap': { deps: ['jquery'] } }
});
// Require all.js or include individual files as needed
require(['jquery', 'bootstrap', 'fuelux'], function($) {
	function changeView(event, data) {

		$('#rankings-table').fadeOut();
		$('#rankings-table-spinner').fadeIn();

		$('#graph').html('<i class="fa fa-spinner fa-5x fa-spin"></i>');

		var params = {};
		if (data.category)
			params.category = data.category

		getResults(data.worksheet, params, $('#rankings-table').find('tbody'));

		$.get('/worksheet/' + data.worksheet + '/graph?' + $.param(params), function(response) {
			$('#graph').html(response);
		});
	}

	// create function to retrieve the information
	function getResults(worksheetId, params, table) {

		var paramStr = $.param(params);
		
		$.getJSON('/worksheet/' + worksheetId + '.json?' + paramStr, function(response) {

			table.empty();
			
			// Populate results table
			$.each(response, function showResults(index, data) {
				table.append('<tr><td>' + (index + 1) + '</td><td>' + data['athlete']['name'] + '</td><td>' + data['score'] + '</td></tr>');
			});

			$('#rankings-table').fadeIn();
			$('#rankings-table-spinner').fadeOut();
		});
	}

	urlSegments = window.location.pathname.split('/');
	console.log(urlSegments[urlSegments.length - 1]);

	// Initialize with overall results
	changeView(null, {
		worksheet: urlSegments[urlSegments.length - 1]
	});	

	$('#category-selector').on('changed.fu.selectlist', changeView);
});