---
name: Bug report
about: Create a report to help us improve
title: ''
labels: needs-triage
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**Steps to reproduce**
If you have a runnable example, please include it as a snippet or link to a repository/gist for larger code examples.

**Expected behavior**
A clear and concise description of what you expected to happen.

**Debug logs**
Full stack trace by adding 
```
import botocore.session
botocore.session.Session().set_debug_logger('')
```
to your code.
