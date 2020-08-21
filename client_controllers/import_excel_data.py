import pandas as pd
from os import path, listdir, remove

## DEPRECATED - NOW THE FILE IS SENT TO THE API FOR THIS TO HAPPEN
def import_excel_sheet(file_path: str):

    unique_child = "false" ## this string flags if uploaded data belong to a single child (common birth_date) or multiple children (different birth_date)
    
    data_frame = pd.read_excel(file_path)
    
    ## delete the file
    remove(file_path)
    
    ## check all columns present
    expected_column_names = ['birth_date', 'observation_date', 'gestation_weeks','gestation_days', 'sex', 'measurement_method', 'measurement_value']
    # essential_column_names = ['birth_date', 'sex', 'measurement_method', 'measurement_value']
    columns = data_frame.columns.ravel().tolist()
    for column in columns:
        ## flag if column_names are missing or extra
        if column not in expected_column_names: 
            raise LookupError('Please include only the headings: birth_date, observation_date, gestation_days, sex, measurement_method, measurement_value')
    if len(columns) != len(expected_column_names):
        raise LookupError('Please include ALL the headings (even if columns left blank): birth_date, observation_date, gestation_days, sex, measurement_method, measurement_value')

    ## check no missing data in essential columns
    elif(pd.isnull(data_frame['birth_date']).values.any() or pd.isnull(data_frame['observation_date']).values.any() or pd.isnull(data_frame['sex']).values.any() or pd.isnull(data_frame['measurement_method']).values.any() or pd.isnull(data_frame['measurement_value']).values.any()):
        remove(file_path)
        raise ValueError('birth_date, sex, measurement_method and measurement_value are all essential data fields and cannot be blank.')
    else:

        ## the dataframe is in the correct format
        ## format the dataframe
        data_frame['birth_date']=data_frame['birth_date'].astype('datetime64[ns]')
        data_frame['observation_date']=data_frame['observation_date'].astype('datetime64[ns]')
        data_frame['measurement_method']=data_frame['measurement_method'].astype(str)
        data_frame['measurement_method']=data_frame.apply(lambda  row: row['measurement_method'].lower(), axis=1) ## ensure sex and measurement_method are lowercase
        data_frame['sex']=data_frame['sex'].astype(str)
        data_frame['sex']=data_frame.apply(lambda  row: row['sex'].lower(), axis=1) ## ensure sex and measurement_method are lowercase
        ## fill the gaps
        data_frame['gestation_days'] = data_frame['gestation_days'].fillna(0).astype(int) 
        data_frame['gestation_weeks'] = data_frame['gestation_weeks'].fillna(0).astype(int)

        ## convert dates to iso8601
        data_frame['birth_date'] = pd.to_datetime(data_frame['birth_date']).dt.strftime('%Y-%m-%dT%H:%M:%S.%f')
        data_frame['observation_date'] = pd.to_datetime(data_frame['observation_date']).dt.strftime('%Y-%m-%dT%H:%M:%S.%f')

        ## Now compare the dates of birth - if they are all the same, patient is unique, serial_data is true

        if data_frame['birth_date'].nunique() > 1:
            print('these are not all data from the same patient. They cannot be charted.') #do not chart these values
            unique_child = "false"
        else:
            unique_child = "true"

        return {
            'data': data_frame.to_json(orient='records', date_format='epoch'),
            'unique_child': unique_child
        }