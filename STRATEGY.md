## Proof of Concept
1. Write sublime command to open scratch file (tbd whether it exists/not) with input and cursors at selected point
2. Perform action as configured (e.g. `left_delete`)
3. Assert content + cursor position matches output

## Polish
4. Repeat on remaining files
5. Collect feedback and return results

## Notes
- Move break out of content and selection to pre-command action (e.g. compile step)
    - Ideally, content/selection would be variable at this step to allow for different delimiters etc without bloating code (e.g. strategy pattern)
    - Additionally, it would allow for selection as an action (and even content) to be an opt-in action. The default would be a noop command (not even opening a view).
- Take notes from CSV and template engines (e.g. ejs) to proper handle escaped delimiters