Make a python executable `clocky` which calls `timew` with the correct arguments over ssh profile `chum`

`clocky <options>` -> `ssh chum 'timew <options>'`

and it will print the output to the client.

For all commands except `begin`, clocky displays the daily report (`timew report table :day`) after running the requested command.

## Special Commands

### `clocky begin`
Interactive command to start a new time entry:
1. Prompts for tags (space-separated)
2. Prompts for an annotation
3. Executes `timew start <tags>`
4. Executes `timew annotate @1 "<annotation>"`

