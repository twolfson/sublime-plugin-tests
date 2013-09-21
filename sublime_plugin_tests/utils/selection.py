import re

def split_selection(input):
    """ Break up input string with selection delimiters into selection and content. """

    # Create a placeholder selection
    sel = []

    # Find all indications for selection
    while True:
        # Find the next matching selection
        # TODO: Robustify with multi-char selection and escaping
        # TODO: Take notes from CSV and template engines (e.g. ejs) to proper handle escaped delimiters
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
        'selection': sel,
        'content': input
    }
