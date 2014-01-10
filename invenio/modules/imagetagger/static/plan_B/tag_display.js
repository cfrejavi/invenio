$(document).ready(function(){
	$('.photoTag').photoTag({
		requesTagstUrl: "{{ url_for('imagetagger.static.plan_B', filename='photo-tags.php') }}",
		deleteTagsUrl: "{{ url_for('imagetagger.static.plan_B', filename='delete.php') }}",
		addTagUrl: "{{ url_for('imagetagger.static.plan_B', filename='add-tag.php') }}",
		parametersForNewTag: {
			name: {
				parameterKey: 'name',
				isAutocomplete: true,
				autocompleteUrl: "{{ url_for('imagetagger.static.plan_B', filename='names.php') }}",
				label: 'Name'
			}
		}
	});
});