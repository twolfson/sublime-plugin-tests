# Load in core dependencies
import re
import os
import shutil
import subprocess

# Load in 3rd party dependencies
from jinja2 import Template

# Set up constants
__dir__ = os.path.dirname(os.path.abspath(__file__))

# Define utility method
def split_sel(input):
    # Create a placeholder selection
    sel = []

    # Find all indications for selection
    while True:
        # Find the next matching selection
        # TODO: Robustify with multi-char selection and escaping
        match = re.search(r'\|', input)

        # If there was a match
        if match:
            # Save the selection
            start = match.start(0)
            sel.append((start, start))

            # Remove the match from the input
            input = input[:start] + input[match.end(0):]

        # Otherwise, break
        else:
            break

    # Return a selection and content
    return {
        'sel': sel,
        'content': input
    }

def main():
    # Load in single.input
    with open('example/left_delete/test_files/single.input.py') as f:
        input = f.read()

    # Break up target selection from content
    input_obj = split_sel(input)
    target_sel = input_obj['sel']
    content = input_obj['content']

    # Load in single.output
    with open('example/left_delete/test_files/single.output.py') as f:
        expected_output = f.read()

    # Break up expected selection from content
    expected_obj = split_sel(expected_output)
    expected_sel = expected_obj['sel']
    expected_content = expected_obj['content']

    # Template plugin
    plugin = None
    with open('plugin.template.py') as f:
        template = Template(f.read())
        plugin = template.render(target_sel=target_sel,
                                 content=content,
                                 expected_sel=expected_sel,
                                 expected_content=expected_content,
                                 output_file=__dir__ + '/output-0001.txt')

    # TODO: It would be nice to pull directory location from Sublime but it isn't critical
    # Determine the scratch plugin directory
    scratch_dir = os.path.expanduser('~/.config/sublime-text-2/Packages/tmp-plugin-tests')

    # If the scratch plugins directory does not exist, create it
    if not os.path.exists(scratch_dir):
        os.makedirs(scratch_dir)

    # If command.py doesn't exist, copy it
    orig_command_path = __dir__ + '/tmp/command.py'
    dest_command_path = scratch_dir + '/command.py'
    if not os.path.exists(scratch_dir + '/command.py'):
        shutil.copyfile(orig_command_path, dest_command_path)
    else:
    # Otherwise...
        # If there are updates for command.py
        expected_command = None
        with open(orig_command_path) as f:
            expected_command = f.read()
        actual_command = None
        with open(dest_command_path) as f:
            actual_command = f.read()
        if expected_command != actual_command:
            # Update the file
            shutil.copyfile(orig_command_path, dest_command_path)

            # and notify the user we must restart Sublime
            # TODO: We might want to make this even more loud
            print 'We had to update the test launcher plugin. You must close or restart Sublime to continue testing.'
            return

    # # Output plugin to directory
    with open(scratch_dir + '/plugin.py', 'w') as f:
        f.write(plugin)

    # Start a subprocess to run the plugin
    # TODO: We might want a development mode (runs commands inside local sublime window) and a testing mode (calls out to Vagrant box)
    # TODO: or at least 2 plugin hooks, one for CLI based testing and one for internal dev
    subprocess.call(['sublime_text', '--command', 'tmp_test'])

    # TODO: Read in the output

if __name__ == '__main__':
    main()
