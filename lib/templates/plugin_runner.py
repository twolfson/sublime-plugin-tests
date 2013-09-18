import sys
import traceback

class Test():
    def run(self):
        # Placeholder for success and error info
        success = True
        err = None

        # Attempt to perform actions and catch *any* exception
        try:
            import plugin
            plugin.run()
        except Exception:
        # If an error occurs, record it
            success = False
            exc_type, exc_value, exc_traceback = sys.exc_info()
            err = ''.join(traceback.format_exception(exc_type,
                                                     exc_value,
                                                     exc_traceback))
        finally:
        # Always...
            # Write out success/failure and any meta data
            output = 'SUCCESS' if success else 'FAILURE'
            if err:
                output += '\n%s' % err
            with open('{{output_file}}', 'w') as f:
                f.write(output)
