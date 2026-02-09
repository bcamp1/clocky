#!/usr/bin/env python3

import sys
import subprocess
import shlex
from datetime import datetime, date, timedelta


def run_ssh_command(remote_cmd):
    """Execute a command via SSH to chum."""
    cmd = ['ssh', '-t', '-o', 'LogLevel=ERROR', 'chum', remote_cmd]
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


def parse_time(time_str):
    """Parse a time string like '6:00pm', '9:00', '14:30' into HH:MM:SS format."""
    time_str = time_str.strip().lower()
    for fmt in ('%I:%M%p', '%I:%M %p', '%I%p', '%H:%M', '%H:%M:%S'):
        try:
            return datetime.strptime(time_str, fmt).strftime('%H:%M:%S')
        except ValueError:
            continue
    print(f"Could not parse time: {time_str}", file=sys.stderr)
    sys.exit(1)


def add_command():
    """
    Interactive command to add a completed time entry in the past.

    Prompts for tags, annotation, days ago, start time, and end time, then executes:
    1. timew track <start_datetime> - <end_datetime> <tags>
    2. timew annotate @1 "<annotation>"
    """
    tags_input = input("Enter tags (space-separated): ").strip()
    tags = tags_input.split() if tags_input else []

    annotation = input("Enter description: ").strip()

    days_ago = input("How many days ago? (0 for today): ").strip()

    start_time = input("Start time (e.g. 9:00, 6:00pm): ").strip()
    end_time = input("End time (e.g. 10:30, 9:00pm): ").strip()

    # Compute the actual date and build ISO datetimes
    days = int(days_ago) if days_ago else 0
    target_date = (date.today() - timedelta(days=days)).strftime('%Y%m%d')
    start_iso = f'{target_date}T{parse_time(start_time).replace(":", "")}'
    end_iso = f'{target_date}T{parse_time(end_time).replace(":", "")}'

    tags_str = ' '.join(shlex.quote(tag) for tag in tags)
    track_cmd = f'timew track {start_iso} - {end_iso} {tags_str}'
    result = run_ssh_command(track_cmd)

    if result.returncode != 0:
        print("Failed to add time entry", file=sys.stderr)
        sys.exit(result.returncode)

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

    Special commands:
        clocky begin - Interactive prompt to start a new time entry
        clocky add   - Interactive prompt to add a completed past entry

    For all commands except 'begin' and 'add', displays the daily report after.
    """
    # Check for special commands
    if len(sys.argv) == 2 and sys.argv[1] == 'begin':
        begin_command()
        sys.exit(0)

    if len(sys.argv) == 2 and sys.argv[1] == 'add':
        add_command()
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
