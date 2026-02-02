#!/usr/bin/env python3

import sys
import subprocess
import shlex


def run_ssh_command(remote_cmd):
    """Execute a command via SSH to chum."""
    cmd = ['ssh', '-t', 'chum', remote_cmd]
    return subprocess.run(cmd)


def begin_command():
    """
    Interactive command to start a new time entry with tags and annotation.

    Prompts for tags and annotation, then executes:
    1. timew start <tags>
    2. timew annotate @1 "<annotation>"
    """
    # Prompt for tags
    tags_input = input("Enter tags (space-separated): ").strip()
    tags = tags_input.split() if tags_input else []

    # Prompt for annotation
    annotation = input("Enter annotation: ").strip()

    # Start the time entry with tags
    start_cmd = 'timew start ' + ' '.join(shlex.quote(tag) for tag in tags)
    result = run_ssh_command(start_cmd)

    if result.returncode != 0:
        print("Failed to start time entry", file=sys.stderr)
        sys.exit(result.returncode)

    # Add annotation if provided
    if annotation:
        annotate_cmd = f'timew annotate @1 {shlex.quote(annotation)}'
        result = run_ssh_command(annotate_cmd)

        if result.returncode != 0:
            print("Failed to add annotation", file=sys.stderr)
            sys.exit(result.returncode)


def main():
    """
    Forward all arguments to the remote 'timew' command via SSH.

    Usage: clocky <options>
    This executes: ssh chum 'timew <options>'

    Special command:
        clocky begin - Interactive prompt for tags and annotation

    For all commands except 'begin', displays the daily report first.
    """
    # Check for special 'begin' command
    if len(sys.argv) == 2 and sys.argv[1] == 'begin':
        begin_command()
        sys.exit(0)

    # All arguments after 'clocky' are passed to 'timew'
    timew_args = sys.argv[1:]

    # Construct the remote command with properly quoted arguments
    remote_cmd = 'timew ' + ' '.join(shlex.quote(arg) for arg in timew_args)

    # Execute and forward output
    try:
        result = run_ssh_command(remote_cmd)

        # Show daily report after the command
        print()  # Add blank line separator
        run_ssh_command('timew report table :day')

        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error executing clocky: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
