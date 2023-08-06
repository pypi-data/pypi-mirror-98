# SNaP OneDrive Report Aggregator
Utility for ModelTB.org team. Aggregates SNaP reports to a single file.

## Prerequisites
1. Gain access to the appropriate OneDrive folders.
2. Install [OneDrive](https://www.microsoft.com/en-us/microsoft-365/onedrive/download)
3. Install [Python](https://www.python.org/downloads/)

## Installation
1. Ensure that all prerequisites are complete.
2. Open [Terminal (Mac)](https://www.howtogeek.com/682770/how-to-open-the-terminal-on-a-mac/) / [Command Prompt (Windows)](https://www.howtogeek.com/235101/10-ways-to-open-the-command-prompt-in-windows-10/)
3. Enter command: `python -m pip install pipx`
4. Enter command: `python -m pipx ensurepath`
5. Restart Terminal / Command Prompt
6. Enter command: `pipx install snap-tam`
7. If prompted, you may need to re-enter the command `python -m pipx ensurepath` and restart the Terminal / Command Prompt again. Finally, in the case that the command `snap-tam` is still unrecognized after following these installation steps, restart your computer and try running again.

## Running
1. Open Terminal / Command Prompt
2. Enter command: `snap-tam`

## Configuration
When running for the first time, you will be asked to enter the path to your OneDrive installation. What you enter will be stored in the config file. If you have trouble getting the path to the folder, here are some instructions that you can use, depending on your OS: [Mac](https://www.switchingtomac.com/tutorials/osx/5-ways-to-reveal-the-path-of-a-file-on-macos/) || [Windows](https://www.laptopmag.com/articles/show-full-folder-path-file-explorer)

You can also edit the config file in order to update any changed or incorrectly entered information. Additional options for further customization are also available.

Config file w/ default values:
```json
{
  "onedrive_dir_path": "",
  "input_dir_regexp": [
    "SNAP_TAM_[0-9]{3}",
    "SNAP_TAM_Interviewer"
  ],
  "worksheet_name": "Data Entry Log",
  "duration_colnames": [
    "Duration",
    "Total Interaction Duration"
  ],
  "output_dirname": "SNAP_TAM_Aggregated",
  "print_progress": false
}
```

## Troubleshooting
- If python commands don't work, try replacing `python` with `python3`, e.g. `python -m pip install pipx` --> `python3 -m pip install pipx`.
- If installation succeeds, but the program doesn't work, an immediate upgrade may solve the problem. To upgrade, execute from the command line: `pipx upgrade snap-tam`
