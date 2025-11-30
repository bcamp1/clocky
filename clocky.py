#!/usr/bin/env python3

import sys
import subprocess
import shlex

def main():
    """
    Forward all arguments to the remote 'clock' command via SSH.

    Usage: clocky <options>
    This executes: ssh chum 'clock <options>'
    """
    # All arguments after 'clocky' are passed to 'clock'
    clock_args = sys.argv[1:]

    # Construct the remote command with properly quoted arguments
    remote_cmd = 'clock ' + ' '.join(shlex.quote(arg) for arg in clock_args)

    # Construct the SSH command
    cmd = ['ssh', 'chum', remote_cmd]

    # Execute and forward output
    try:
        result = subprocess.run(cmd)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error executing clocky: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
