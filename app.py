from os import path, listdir, remove, environ
from datetime import datetime
from pathlib import Path
from measurement_request import MeasurementForm
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, make_response, jsonify, session
import markdown
import requests
import json


app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'UK_WHO' #not very secret - this will need complicating and adding to config

from app import app

"""
SETUP THE API
TODO: consider use of 'configparser' for this
API_BASEURL defaults to 'localhost:5000' unless explicitly set
"""

OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

API_BASEURL=environ.get('GROWTH_API_BASEURL') or 'http://localhost:5000'
print(f'{OKGREEN} * Growth Charts API_BASEURL is {API_BASEURL}{ENDC}')


"""
FLASK CLIENT ROUTES
"""

# CALCULATIONS FORM
@app.route("/", methods=['GET', 'POST'])
def home():
    form = MeasurementForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            payload = {
                'birth_date': form.birth_date.data,
                'observation_date': form.obs_date.data,
                'height_in_metres': float(form.height.data),
                'weight_in_kg': float(form.weight.data),
                'occipitofrontal_circ_in_cm': float(form.ofc.data),
                'sex': str(form.sex.data),
                'gestation_weeks': int(form.gestation_weeks.data),
                'gestation_days': int(form.gestation_days.data)
            }
            # collect user form entries and perform date and SDS/Centile calculations
            response = requests.get(
                f'{API_BASEURL}/api/v1/json/calculations',
                params=payload
            )

            print(response.json())

            # store the results in a session for access by tables and charts later
            session['results'] = response.json()

            # flag to differentiate between individual plot and serial data plot
            session['serial_data'] = False

            return redirect(url_for('results', id='table'))

        # form not validated. Need flash warning here
        return render_template('measurement_form.html', form = form)
    else:
        # controllers.temp_test_functions.tim_tests_preterm()
        return render_template('measurement_form.html', form = form)


# GROWTH REFERENCES LIST
@app.route("/references", methods=['GET'])
def client_references():
    response = requests.get(f'{API_BASEURL}/api/v1/json/references') 
    return render_template('references.html', data=response.json() )


# RESULTS
@app.route("/results/<id>", methods=['GET', 'POST'])
def results(id):
    results = session.get('results')
    if id == 'table':
        return render_template('test_results.html', result = results)
    if id == 'chart':
        return render_template('chart.html')


# CHART
@app.route("/chart", methods=['GET'])
def chart():
    return render_template('chart.html')


@app.route("/instructions", methods=['GET'])
def instructions():
    html = requests.get(f'{API_BASEURL}/api/v1/json/instructions') 
    return render_template('instructions.html', fill=html)


# IMPORT EXCEL FILE
@app.route("/import", methods=['GET', 'POST'])
def import_growth_data():
    if request.method == 'POST':
        ## can only receive .xls, .xlsx, or .csv files
        ## thanks to Chris Griffith, Code Calamity for this code - upload files, chunk if large
        file = request.files['file']
        static_directory = path.join(path.abspath(path.dirname(__file__)), "static/uploaded_data")
        file_to_save = path.join(static_directory, secure_filename(file.filename))
        current_chunk = int(request.form['dzchunkindex'])

        # If the file already exists it's ok if we are appending to it,
        # but not if it's new file that would overwrite the existing one
        if path.exists(file_to_save) and current_chunk == 0:
            # 400 and 500s will tell dropzone that an error occurred and show an error
            return make_response(('File already exists', 400))

        try:
            with open(file_to_save, 'ab') as f:
                f.seek(int(request.form['dzchunkbyteoffset']))
                f.write(file.stream.read())
        except OSError:
            # log.exception will include the traceback so we can see what's wrong 
            print('Could not write to file')
            return make_response(("Not sure why,"
                                " but we couldn't write the file to disk", 500))

        total_chunks = int(request.form['dztotalchunkcount'])

        if current_chunk + 1 == total_chunks:
            # This was the last chunk, the file should be complete and the size we expect
            if path.getsize(file_to_save) != int(request.form['dztotalfilesize']):
                assert(f"File {file.filename} was completed, "
                        f"but has a size mismatch."
                        f"Was {os.path.getsize(save_path)} but we"
                        f" expected {request.form['dztotalfilesize']} ")
                return make_response(('Size mismatch', 500))
            else:
                print(f'File {file.filename} has been uploaded successfully')
                # return make_response('Upload Successful', 200)
                return make_response('success', 200)
        else:
            print(f'Chunk {current_chunk + 1} of {total_chunks} '
                    f'for file {file.filename} complete')

        return make_response("Chunk upload successful", 200)
            
    else:
        return render_template('import.html')


# UPLOAD EXCEL FILE?
# TODO: Definitely needs to be deprecated in favour of a PR model of submitting reference data
@app.route("/uploaded_data/<id>", methods=['GET', 'POST'])
def uploaded_data(id):
    global requested_data
    if request.method == 'GET':
        static_directory = path.join(path.abspath(path.dirname(__file__)), "static/uploaded_data/")
        if id == 'example':
            ## Have requested to view the sample data
            file_path = path.join(static_directory, 'dummy_data.xlsx')
            loaded_data = controllers.import_excel_sheet(file_path, False) #false flag prevents deleting file once data imported
            data = json.loads(loaded_data['data'])
            """
            converts ISO8601 to UK readable dates
            """
            for i in data:
                if(i['birth_date']):
                    i['birth_date'] =  datetime.strftime(datetime.fromtimestamp(i['birth_date']/1000), '%d/%m/%Y')
                if(i['observation_date']):    
                    i['observation_date'] =  datetime.strftime(datetime.fromtimestamp(i['observation_date']/1000), '%d/%m/%Y')
                if(i['estimated_date_delivery']): 
                    i['estimated_date_delivery'] =  datetime.strftime(datetime.fromtimestamp(i['estimated_date_delivery']/1000), '%d/%m/%Y')
            # store the formatted data in a global variable
            requested_data = data
            ## this data is not from a unique patient - cannot graph or produce velocities
            return render_template('uploaded_data.html', data=data, unique=loaded_data['unique'], dynamic_calculations=None)
        if id == 'excel_sheet':
            for file_name in listdir(static_directory):
                if file_name != 'dummy_data.xlsx':
                    """
                    Loop through static/upload folder
                    Avoid the example sheet
                    Save there temporarily, import the data then delete
                    """
                    file_path = path.join(static_directory, file_name)
                    try:
                        # import the data from excel and validate, delete the file once imported (True flag)
                        child_data = controllers.import_excel_sheet(file_path, True)
                        # extract the dataframe
                        data_frame = child_data['data']
                    
                    except ValueError as e:
                        
                        """
                        Error handler - uploaded sheet is incompatible: missing essential data
                        """
                        print(e)
                        flash(f"{e}")
                        data=None
                        render_template('uploaded_data.html', data=data, unique=False, dynamic_calculations=None)

                    except LookupError as l:
                        
                        """
                        Error handler - uploaded sheet is incompatible: headings are missing or too many or misspelled
                        """

                        data=None
                        print(l)
                        flash(f"{l}")
                        data=None
                        render_template('uploaded_data.html', data=data, unique=False, dynamic_calculations=None)
                    
                    else:
                        """
                        Data is correct format
                        Load as JSON and report to table
                        If the imported data is all same patient (on basis of unique birth_date),
                        offer the opportunity to chart it, calculate velocity and acceleration of most recent parameters
                        """

                        #convert dataframe to JSON
                        data = json.loads(data_frame)

                        """
                        creates UK date strings from ISO8601
                        """
                        for i in data:
                            if(i['birth_date']):
                                i['birth_date'] =  datetime.strftime(datetime.fromtimestamp(i['birth_date']/1000), '%d/%m/%Y')
                            if(i['observation_date']):
                                i['observation_date'] =  datetime.strftime(datetime.fromtimestamp(i['observation_date']/1000), '%d/%m/%Y')
                            if(i['estimated_date_delivery']): 
                                i['estimated_date_delivery'] =  datetime.strftime(datetime.fromtimestamp(i['estimated_date_delivery']/1000), '%d/%m/%Y')
                        
                        # store the JSON in global variable for conversion back to excel format for download if requested
                        requested_data = data

                        # data is unique patient, calculate velocity
                        # data come from a table and need converting to Measurement class
                        formatted_child_data = controllers.prepare_data_as_array_of_measurement_objects(requested_data)
                        dynamic_calculations = controllers.calculate_velocity_acceleration(formatted_child_data)
                        
                        # if unique data(single child, not multiple children) store in session for access by chart if requested
                        session['results'] = requested_data
                        session['serial_data'] = True
                
            return render_template('uploaded_data.html', data=data, unique=child_data['unique'], dynamic_calculations = dynamic_calculations) #unique is a flag to indicate if unique child or multiple children
        
        if id=='get_excel': ##broken needs fix - file deleted so can't download
            excel_file = controllers.download_excel(requested_data)
            temp_directory = Path.cwd().joinpath("static").joinpath('uploaded_data').joinpath('temp')
            return send_from_directory(temp_directory, filename='output.xlsx', as_attachment=True)



if __name__ == '__main__':
    app.run()
