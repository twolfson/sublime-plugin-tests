# sublime-plugin-tests [![Build status](https://travis-ci.org/twolfson/sublime-plugin-tests.png?branch=master)](https://travis-ci.org/twolfson/sublime-plugin-tests)

Testing framework for Sublime Text plugins

This was built to create a platform to test plugins against multiple versions of Sublime Text.

![Screenshot of tests running](docs/tests.png)

## Getting Started
Install the module with: `pip install sublime_plugin_tests`

Then, write your tests:

```python
# Load in test framework
from sublime_plugin_tests import framework

# Define a TestCase
class TestLeftDelete(framework.TestCase):
    def test_left_delete_single(self):
        # Each test function *must* return Python with a `run` function
        # `run` will be run inside Sublime Text. Perform your assertions etc there.
        return """
# Use ScratchView utility provided by `sublime_plugin_tests`
from utils.scratch_view import ScratchView

def run():
    # Generate new scratch file
    scratch_view = ScratchView()
    try:
        # Update the content and selection `ab|c`
        scratch_view.set_content('abc')
        scratch_view.set_sel([(2, 2)])

        # Delete one character to the left `a|c
        scratch_view.run_command('left_delete')

        # Assert the current content
        assert scratch_view.get_content() == 'ac'
    finally:
        # No matter what happens, close the view
        scratch_view.destroy()
"""
```

```bash
$ # Run tests via nosetests
$ nosetests
.
----------------------------------------------------------------------
Ran 1 test in 0.076s

OK
```

## Documentation
### framework.TestCase
`framework.TestCase` extends [Python's unittest.TestCase][testcase]. Tests can be skipped and set up/torn down as you normally would. The key difference is the string you return **will not** be run in the same context and not have access to the assertions (yet...).

[testcase]: TODO: Link me

### utils.selection.split_selection
`utils.selection.split_selection` break up a string by selection markers into `content` and `selection`.

```python
split_selection(input)
"""
@param {String} input Python to parse selection indicators out of
@returns {Dictionary} ret_obj Container for selection and content
@return {List} ret_obj['selection'] List of tuples for start/end position of selections
@return {String} ret_obj['content'] Python with selection characters removed
"""
```

#### Example
Input:
```python
split_selection("""
def abc|():
    pas|s
""")
```

Output:
```python
{
  'content': """
def ab|():
    pa|s
""",
  'selection': [(7, 7), (18, 18)]
}
```

TODO: Document ScratchView

TODO: Build and release

## Architecture
Framework takes each test function, wraps it in a test harness, runs it, and asserts whether the harness saw an error or not.

The test harness generates a temporary Sublime Text plugin which runs your test in the context of Sublime. This harness is launched via a CLI invocation of Sublime Text.

The output and assertions of each test function are reported back to `nosetests` which prints to `stdout` and exits.

## Donating
Support this project and [others by twolfson][gittip] via [gittip][].

[![Support via Gittip][gittip-badge]][gittip]

[gittip-badge]: https://rawgithub.com/twolfson/gittip-badge/master/dist/gittip.png
[gittip]: https://www.gittip.com/twolfson/

## Contributing
In lieu of a formal styleguide, take care to maintain the existing coding style. Add unit tests for any new or changed functionality. Lint via [grunt](https://github.com/gruntjs/grunt) and test via `npm test`.

## Unlicense
As of Sep 05 2013, Todd Wolfson has released this repository and its contents to the public domain.

It has been released under the [UNLICENSE][].

[UNLICENSE]: UNLICENSE
