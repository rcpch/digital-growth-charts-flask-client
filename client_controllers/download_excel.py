import json
import pandas as pd
from pathlib import Path
import pandas as pd

def save_as_excel(json_string: str):
    data_list = json.loads(json_string)
    data = []
    for counter, value in enumerate(data_list):
        birth_date = value['birth_data']['birth_date']
        measurement_date = value['measurement_dates']['observation_date']
        gestation_weeks = value['birth_data']['gestation_weeks']
        gestation_days = value['birth_data']['gestation_days']
        estimated_date_delivery = value['birth_data']['estimated_date_delivery']
        corrected_decimal_age = value['measurement_dates']['corrected_decimal_age']
        chronological_decimal_age = value['measurement_dates']['chronological_decimal_age']
        measurement_value = value['child_observation_value']['measurement_value']
        measurement_type = value['child_observation_value']['measurement_type']
        sds = value['measurement_calculated_values']['sds']
        centile = value['measurement_calculated_values']['centile']
  
        data_row = [birth_date, measurement_date, gestation_weeks, gestation_days, estimated_date_delivery, corrected_decimal_age, chronological_decimal_age, measurement_value, measurement_type, sds, centile]
        data.append(data_row)
    headings = ['birth_date', 'measurement_date', 'gestation_weeks', 'gestation_days', 'estimated_date_delivery', 'corrected_decimal_age', 'chronological_decimal_age', 'measurement_value', 'measurement_type', 'sds', 'centile']
    data_frame = pd.DataFrame(data, columns=headings)
    out_file_2 = Path.cwd().joinpath("static").joinpath('uploaded_data').joinpath("output.xlsx")
    excel_file = data_frame.to_excel(out_file_2)
    return excel_file