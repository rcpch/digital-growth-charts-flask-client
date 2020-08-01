import json
import pandas as pd
from os import path
import pandas as pd
from datetime import datetime, date

def save_as_excel(python_dict, upload_root: str):
    data_list = python_dict         #json.loads(json_string)
    data = []
    for counter, value in enumerate(data_list):
        birth_date = datetime.strptime(value['birth_data']['birth_date'],"%a, %d %b %Y %H:%M:%S %Z").date()
        measurement_date = datetime.strptime(value['measurement_dates']['observation_date'],"%a, %d %b %Y %H:%M:%S %Z").date()
        gestation_weeks = value['birth_data']['gestation_weeks']
        gestation_days = value['birth_data']['gestation_days']
        if value['birth_data']['estimated_date_delivery']:
            estimated_date_delivery = datetime.strptime(value['birth_data']['estimated_date_delivery'],"%a, %d %b %Y %H:%M:%S %Z").date()
        else:
            estimated_date_delivery = None
        corrected_decimal_age = value['measurement_dates']['corrected_decimal_age']
        chronological_decimal_age = value['measurement_dates']['chronological_decimal_age']
        measurement_value = value['child_observation_value']['measurement_value']
        measurement_method = value['child_observation_value']['measurement_method']
        sds = value['measurement_calculated_values']['sds']
        centile = value['measurement_calculated_values']['centile']
  
        data_row = [birth_date, measurement_date, gestation_weeks, gestation_days, estimated_date_delivery, corrected_decimal_age, chronological_decimal_age, measurement_value, measurement_method, sds, centile]
        data.append(data_row)
    headings = ['birth_date', 'measurement_date', 'gestation_weeks', 'gestation_days', 'estimated_date_delivery', 'corrected_decimal_age', 'chronological_decimal_age', 'measurement_value', 'measurement_method', 'sds', 'centile']
    data_frame = pd.DataFrame(data, columns=headings)
    data_frame.index+=1
    out_file_2 = path.join(upload_root, "output.xlsx")
    excel_file = data_frame.to_excel(out_file_2)
    return excel_file