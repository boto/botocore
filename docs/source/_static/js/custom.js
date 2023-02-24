/*
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
You may obtain a copy of the License at

	http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

// Checks if an html doc name matches a service class name.
function isValidServiceName(docName, serviceClassName) {
	const new_docName = docName.replaceAll('-', '').toLowerCase();
	return new_docName === serviceClassName;
}
// Checks if all elements of the split fragment are valid.
// Fragment items should only contain alphanumerics, hyphens, & underscores.
// A fragment should also only be redirected if it contain 3-5 items.
function isValidFragment(splitFragment) {
	const regex = /^[a-z0-9-_]+$/i;
	for (index in splitFragment) {
		if (!regex.test(splitFragment[index])) {
			return false;
		}
	}
	return splitFragment.length > 2 && splitFragment.length < 6;
}
// Reroutes previously existing links to the new path.
// Old: <root_url>/reference/services/s3.html#S3.Client.delete_bucket
// New: <root_url>/reference/services/s3/client/delete_bucket.html
// This must be done client side since the fragment (#S3.Client.delete_bucket) is never
// passed to the server.
(function () {
	const currentPath = window.location.pathname.split('/');
	const fragment = window.location.hash.substring(1);
	// Only redirect when viewing a top-level service page.
	if (fragment && currentPath[currentPath.length - 2] === 'services') {
		const serviceDocName = currentPath[currentPath.length - 1].replace('.html', '');
		const splitFragment = fragment.split('.');
		splitFragment[0] = splitFragment[0].toLowerCase();
		if (isValidFragment(splitFragment) && isValidServiceName(serviceDocName, splitFragment[0])) {
			// Replace class name with doc name
			splitFragment[0] = serviceDocName;
			splitFragment[1] = splitFragment[1].toLowerCase();
			// Exceptions have a longer sub-path (<service>/client/exceptions/<exception>.html)
			const isException = splitFragment[2] === 'exceptions';
			const sliceLocation = isException ? 4 : 3;
			var newPath = `${ splitFragment.slice(0, sliceLocation).join('/') }.html`;
			if (splitFragment.length > 3 && !isException || splitFragment.length > 4 && isException) {
				// Redirect with the fragment
				window.location.assign(`${ newPath }#${ fragment }`);
			} else {
				// Redirect without the fragment
				window.location.assign(newPath);
			}
		}
	}
}());
