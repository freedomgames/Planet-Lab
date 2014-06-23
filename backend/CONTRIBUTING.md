Contributing
============
First of all, thanks for contributing!
If you could follow a few short guidelines in your contributions,
that would be super.

Pull Requests
-------------
* Fork https://github.com/freedomgames/Planet-Lab
and send pull requests against the master branch.
* Try to keep them short -- aim for a focused pull requests of around
300 lines or shorter.
A few short, focused pull requests are preferable to one big pull request.

Code Style
----------
* [PEP8](http://legacy.python.org/dev/peps/pep-0008/) all the way.
* Put a docstring on everything and be liberal with comments --
remember that this is a project with a shifting group of contributors
who would love to be able to quickly get up to speed thanks to your
excellent documentation.
* avoid 'from import' statements.  Do
```python
import foo.bar as bar
```
rather than
```python
from foo import bar
```

Code Quality
------------
* Your changes must include unit tests.
Please don't lower our (quite high!) unit test coverage.
* Keep the [API docs](API_DOCS.md) up-to-date with your changes.
* [Pylint](http://www.pylint.org) is your friend!
Use the provided pylintrc and update it if you see false positives.
