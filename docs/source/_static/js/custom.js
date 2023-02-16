// Reroutes previously existing links to the new path.
// Old: <root_url>/reference/services/s3.html#S3.Client.delete_bucket
// New: <root_url>/reference/services/s3/client/delete_bucket.html
// This must be done client side since the fragment (#S3.Client.delete_bucket) is never
// passed to the server.
(function () {
	const windowLocation = window.location;
	const currentPath = windowLocation.pathname.split('/');
	const fragment = windowLocation.hash.substring(1);
	// Only redirect when viewing a top-level service page.
	if (fragment && currentPath[currentPath.length - 2] === 'services') {
		const splitFragment = fragment.split('.');
		splitFragment[0] = splitFragment[0].toLowerCase();
		if (splitFragment.length > 2) {
			splitFragment[1] = splitFragment[1].toLowerCase();
            // Exceptions have a longer sub-path (<service>/client/exceptions/<exception>.html)
			const isException = splitFragment[2] === 'exceptions' ? true : false;
			const sliceLocation = isException ? 4 : 3;
			var newPath = `${ splitFragment.slice(0, sliceLocation).join('/') }.html`;
			if (splitFragment.length > 3 && !isException || splitFragment.length > 4 && isException) {
                // Redirect with the fragment
				windowLocation.replace(`${ newPath }#${ fragment }`);
			} else {
                // Redirect without the fragment
				windowLocation.replace(newPath);
			}
		}
	}
}());
