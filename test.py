import re
import subprocess

# Define utility method
def split_sel(cls, input):
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
            # sel.append(Region(start, start))
            # TODO: Must cast all tuples to Regions
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
    with open(__dir__ + '/example/left_delete/test_files/single.input.py') as f:
        input = f.read()

    # Break up target selection from content
    input_obj = split_sel(input)
    target_sel = input_obj['sel']
    content = input_obj['content']

    # Load in single.output
    with open(__dir__ + '/example/left_delete/test_files/single.output.py') as f:
        expected_output = f.read()

    # Break up expected selection from content
    expected_obj = split_sel(expected_output)
    expected_sel = expected_obj['sel']
    expected_content = expected_obj['content']

    # subprocess.call(['sublime_text', '--command', 'left_delete'])

if __name__ == '__main__':
    main()
