"""SNaP OneDrive Report Aggregator

# Running
1. Replace onedrive_dir_path with your path
2. Run Python script

# Troubleshooting problems
1. "Permission denied"
Solution: Make sure the OneDrive program is running on your computer.

"""
import json
import os
import pandas as pd
import re

from datetime import datetime
from openpyxl import load_workbook
from typing import List, Dict


# Constants
SCRIPT_PATH = os.path.realpath(__file__)
PKG_DIR = os.path.dirname(SCRIPT_PATH)
CONFIG_PATH = os.path.join(PKG_DIR, 'config.json')
VALID_EXTENSIONS = ['.xls', '.xlsx', '.xlsm']


def run(
    onedrive_dir_path: str = None,
    input_dir_regexp: str = None,
    worksheet_name: str = None,
    duration_colnames: str = None,
    output_dirname_regexp: str = None,
    print_progress: bool = None
):
    """Run"""
    args: Dict = locals()
    config: Dict = None

    with open(CONFIG_PATH, 'r') as config_file:
        config = json.load(config_file)
        for arg_key, arg_val in args.items():
            if arg_key in config.keys() and arg_val:
                config[arg_key] = arg_val
    with open(CONFIG_PATH, 'w') as config_file:
        json_string = json.dumps(
            config,
            default=lambda o: o.__dict__,  # pretty prints
            indent=2)
        config_file.write(json_string)

    onedrive_dir_path: str = config['onedrive_dir_path']
    input_dir_regexp: str = config['input_dir_regexp']
    worksheet_name: str = config['worksheet_name']
    duration_colnames: str = config['duration_colnames']
    output_dirname_regexp: str = config['output_dirname_regexp']
    print_progress: bool = config['print_progress']

    if not onedrive_dir_path:
        onedrive_dir_path: str = input('Enter path to OneDrive folder: ')
        config['onedrive_dir_path']: str = onedrive_dir_path
        with open(CONFIG_PATH, 'w') as config_file:
            json_string = json.dumps(
                config,
                default=lambda o: o.__dict__,  # pretty prints
                indent=2)
            config_file.write(json_string)

    print('Running...')

    # Find snap dirs
    # TODO: If 0 records, or if snap_interviewer not found, or no matches to
    # ...the regexp pattern with 3 numbers at end. show a message.
    # ...Currently, the error just shows if nothing found at all.
    snap_dirs: List[str] = []
    for root, dirs, files in os.walk(onedrive_dir_path):
        for name in dirs:
            for regexp in input_dir_regexp:
                if re.match(regexp, name):
                    path = os.path.join(root, name)
                    snap_dirs.append(path)
                    break

    err = 'No folders found matching either of the following folder ' \
          'patterns: ' + str(input_dir_regexp)
    if not snap_dirs:
        raise RuntimeError(err)

    # Find output dir
    output_path: str = None
    for root, dirs, files in os.walk(onedrive_dir_path):
        for name in dirs:
            if re.match(output_dirname_regexp, name):
                path = os.path.join(root, name)
                output_path = path
                break
    if not output_path:
        # Hopefully in this case they didn't acutally put a regexp:
        output_dirname = output_dirname_regexp

        output_path = os.path.join(onedrive_dir_path, output_dirname)
        os.mkdir(output_path)

    snap_files: List[str] = []
    for folder in snap_dirs:
        candidates = [
            y for y in os.listdir(folder)
            if any([y.endswith(ext) for ext in VALID_EXTENSIONS])]
        for candidate in candidates:
            path = os.path.join(folder, candidate)
            snap_files.append(path)

    # Enable permission to read (may not be necessary)
    workbooks = {}
    for file in snap_files:
        os.chmod(file, 0o777)
        wb = load_workbook(filename=file, read_only=True)
        workbooks[file] = wb

    worksheets = {}
    for file, wb in workbooks.items():
        ws = wb[worksheet_name]
        worksheets[file] = ws

    headers: List[str] = None
    duration_col_indices = []
    data: List[List] = []
    n_worksheets = len(worksheets)
    ws_num = 0
    for _, ws in worksheets.items():
        row_num = 0
        ws_num += 1
        if print_progress:
            print(
                'Processing file ' + str(ws_num) + ' of ' + str(n_worksheets))

        for row in ws:
            row_num += 1
            if not any(cell.value for cell in row):
                break
            row_vals = [cell.value for cell in row]
            n_cols = len(row_vals)
            if row_num == 1:
                if ws_num > 1:
                    continue
                headers = row_vals
                # identify 'duration' cols for empty test
                for i in range(n_cols):
                    if headers[i] in duration_colnames:
                        duration_col_indices.append(i)
                continue
            # check if row is 'effectively' empty
            is_empty_row = False
            if not row_vals[0]:
                for i in range(n_cols):
                    if i in duration_col_indices and \
                            row_vals[i] not in [None, 0]:
                        is_empty_row = True
                        break
                    if row_vals[i]:
                        is_empty_row = True
                        break
            if is_empty_row:
                break
            data.append(row_vals)

    df = pd.DataFrame(data, columns=headers)
    filename = (str(datetime.now()) + '.csv').replace(':', '-')
    outpath = os.path.join(output_path, filename)
    df.to_csv(outpath, index=False)
    print(f'Created: {outpath}')


if __name__ == '__main__':
    run()
