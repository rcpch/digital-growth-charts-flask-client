import json
import pandas as pd
from pathlib import Path
import pandas as pd

def save_as_excel(json_string: str):
    json_file = json.dumps(json_string)
    data_frame = pd.read_json(json_file, orient='split')
    print(data_frame.to_string())
    out_file_2 = Path.cwd().joinpath("static").joinpath('uploaded_data').joinpath("output.xlsx")
    excel_file = pd.read_json(json_file).to_excel(out_file_2)
    return excel_file