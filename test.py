import re
import os
# import subprocess

from jinja2 import Template

# Define utility method
def split_sel(input):
    # Create a placeholder selection
    # TODO: Consider moving to RegionSet over list
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
                                 expected_content=expected_content)

    # TODO: It would be nice to pull directory location from Sublime but it isn't critical
    scratch_dir = '~/.config/sublime-text-2/Packages/tmp-plugin-tests'

    # TODO: If the scratch plugins directory already exists, scrap it
    if os.path.exists(scratch_dir):
        pass

    # Generate scratch plugins directory
    os.mkdir(scratch_dir)

    # TODO: Output plugin to directory
    # TODO: Start a subprocess to run the plugin
    # TODO: Direct the output to a local file
    # subprocess.call(['sublime_text', '--command', 'left_delete'])

    # TODO: Read in the output

if __name__ == '__main__':
    main()
