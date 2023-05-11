# Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
from sphinx.locale import admonitionlabels
from sphinx.writers.html5 import HTML5Translator as SphinxHTML5Translator


class BotoHTML5Translator(SphinxHTML5Translator):
    """Extension of Sphinx's ``HTML5Translator`` for Botocore documentation."""

    STRONG_TO_H3_HEADINGS = [
        "Example",
        "Examples",
        "Exceptions",
        "Request Syntax",
        "Response Structure",
        "Response Syntax",
        "Structure",
        "Syntax",
    ]

    def visit_admonition(self, node, name=""):
        """Uses the h3 tag for admonition titles instead of the p tag."""
        self.body.append(
            self.starttag(node, "div", CLASS=("admonition " + name))
        )
        if name:
            title = (
                f"<h3 class='admonition-title'> {admonitionlabels[name]}</h3>"
            )
            self.body.append(title)

    def visit_strong(self, node):
        """Visit a strong HTML element.

        Opens the h3 tag for a specific set of words/phrases and opens the
        strong tag for all others.
        """
        if len(node) > 0 and node[0] in self.STRONG_TO_H3_HEADINGS:
            self.body.append(self.starttag(node, "h3", ""))
        else:
            self.body.append(self.starttag(node, "strong", ""))

    def depart_strong(self, node):
        """Depart a strong HTML element.

        Closes the h3 tag for a specific set of words/phrases and closes the
        strong tag for all others.
        """
        if node[0] in self.STRONG_TO_H3_HEADINGS:
            self.body.append("</h3>")
        else:
            self.body.append("</strong>")
