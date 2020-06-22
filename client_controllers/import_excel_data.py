import pandas as pd
from os import path, listdir, remove

def import_excel_sheet(file_path: str, can_delete: bool):

    unique_child = "false" ## this string flags if uploaded data belong to a single child (common birth_date) or multiple children (different birth_date)
    
    data_frame = pd.read_excel(file_path)
    
    ## delete the file if not dummy_data.xlsx
    if can_delete:
        remove(file_path)

    ## check all columns present
    expected_column_names = ['birth_date', 'observation_date', 'gestation_weeks','gestation_days', 'sex', 'measurement_type', 'measurement_value']
    # essential_column_names = ['birth_date', 'sex', 'measurement_type', 'measurement_value']
    columns = data_frame.columns.ravel().tolist()
    for column in columns:
        ## flag if column_names are missing or extra
        if column not in expected_column_names: 
            raise LookupError('Please include only the headings: birth_date, observation_date, gestation_days, sex, measurement_type, measurement_value')
    if len(columns) != len(expected_column_names):
        raise LookupError('Please include ALL the headings (even if columns left blank): birth_date, observation_date, gestation_days, sex, measurement_type, measurement_value')

    ## check no missing data in essential columns
    elif(pd.isnull(data_frame['birth_date']).values.any() or pd.isnull(data_frame['observation_date']).values.any() or pd.isnull(data_frame['sex']).values.any() or pd.isnull(data_frame['measurement_type']).values.any() or pd.isnull(data_frame['measurement_value']).values.any()):
        remove(file_path)
        raise ValueError('birth_date, sex, measurement_type and measurement_value are all essential data fields and cannot be blank.')
    else:

        ## the dataframe is in the correct format
        ## format the dataframe
        data_frame['birth_date']=data_frame['birth_date'].astype('datetime64[ns]')
        data_frame['observation_date']=data_frame['observation_date'].astype('datetime64[ns]')
        data_frame['measurement_type']=data_frame['measurement_type'].astype(str)
        data_frame['measurement_type']=data_frame.apply(lambda  row: row['measurement_type'].lower(), axis=1) ## ensure sex and measurement_type are lowercase
        data_frame['sex']=data_frame['sex'].astype(str)
        data_frame['sex']=data_frame.apply(lambda  row: row['sex'].lower(), axis=1) ## ensure sex and measurement_type are lowercase
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

    """
    ########################################################################
    The dataframe has been validated so the measurements and dates can be processed.
    This should all be done server side
    #######################################################################

    ## check columns data-type correct
    
    # data_frame['decimal_age'] = data_frame['decimal_age'].fillna(0).astype(float)
    
    # data_frame['estimated_date_delivery']= data_frame['estimated_date_delivery'].astype('datetime64[ns]')
    
    
    ## add the calculated columns (SDS and Centile, corrected and chronological decimal age)
    data_frame['corrected_decimal_age']=data_frame.apply(lambda row: rcpchgrowth.corrected_decimal_age(row['birth_date'], row['observation_date'], row['gestation_weeks'], row['gestation_days']), axis=1)
    data_frame['chronological_decimal_age']=data_frame.apply(lambda row: rcpchgrowth.chronological_decimal_age(row['birth_date'], row['observation_date']), axis=1)
    data_frame['estimated_date_delivery']=data_frame.apply(lambda row: rcpchgrowth.estimated_date_delivery(row['birth_date'], row['gestation_weeks'], row['gestation_days']), axis=1)
    data_frame['sds']=data_frame.apply(lambda row: sds_if_parameters(row['corrected_decimal_age'], row['measurement_type'], row['measurement_value'], row['sex']), axis=1)
    data_frame['centile']=data_frame.apply(lambda row: rcpchgrowth.centile(row['sds']), axis=1)
    data_frame['height'] = data_frame.apply(lambda row: value_for_measurement('height', row['measurement_type'], row['measurement_value']), axis=1)
    data_frame['weight'] = data_frame.apply(lambda row: value_for_measurement('weight', row['measurement_type'], row['measurement_value']), axis=1)
    # same_date_data_frame = data_frame[data_frame.duplicated(['birth_date', 'observation_date'], keep=False)]
    height = 0.0
    weight = 0.0
    weight_date = ''
    height_date = '' 
    weight_birth_date = ''
    height_birth_date = ''

    extra_rows = []
    for index, row in same_date_data_frame.iterrows():
        if pd.notnull(row['height']):
            height = row['height']
            height_date = row['observation_date']
            height_birth_date = row['birth_date']
        if pd.notnull(row['weight']):
            weight = row['weight']
            weight_date = row['observation_date']
            weight_birth_date = row['birth_date']
        if height > 0.0 and weight > 0.0 and height_date == weight_date and height_birth_date == weight_birth_date:
            bmi = rcpchgrowth.bmi_from_height_weight(height, weight)
            if row['corrected_decimal_age'] > 0.038329911: 
                bmi_sds = rcpchgrowth.sds(row['corrected_decimal_age'], 'bmi', bmi, row['sex'])
                bmi_centile = rcpchgrowth.centile(bmi_sds)
            else:
                bmi_sds = None
                bmi_centile = None
            new_row = {'birth_date': height_birth_date, 'observation_date': height_date, 'gestation_weeks': row['gestation_weeks'], 'gestation_days': row['gestation_days'], 'estimated_date_delivery': row['estimated_date_delivery'], 'chronological_decimal_age': row['chronological_decimal_age'], 'corrected_decimal_age': row['corrected_decimal_age'], 'sex': row['sex'], 'measurement_type': 'bmi', 'measurement_value': bmi, 'sds': bmi_sds, 'centile': bmi_centile, 'height': None, 'weight': None}
            extra_rows.append(new_row)

    if len(extra_rows) > 0:
        data_frame = data_frame.append(extra_rows, ignore_index=True)
        data_frame = data_frame.drop_duplicates(ignore_index=True)
        

    if data_frame['birth_date'].nunique() > 1:
        print('these are not all data from the same patient. They cannot be charted.') #do not chart these values
        unique = False

    return {
        'data': data_frame.to_json(orient='records', date_format='epoch'),
        'unique': unique
    }
    """