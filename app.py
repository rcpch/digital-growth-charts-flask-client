
from datetime import datetime
from os import path, listdir, remove, environ
from measurement_request import MeasurementForm, FictionalChildForm
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, make_response, jsonify, session, abort, after_this_request
from flask_cors import CORS
from flask import Response
import markdown
import requests
import json
from client_controllers import chunk_file, import_excel_data, download_excel
from werkzeug.utils import secure_filename
from pathlib import Path
from flask_dropzone import Dropzone


# client side controller to manipulate excel sheet
"""
we have two options here: either upload the spreadsheet, store it temporarily client side in order to create the dataframe and 
manipulate fields client side here, or send the dataframe to the server. The second option is preferable
"""


app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = "UK_WHO" #not very secret - this will need complicating and adding to config
CORS(app)
Dropzone(app)

assets_folder = path.join(app.root_path, 'static')
uploaded_data_folder = path.join(assets_folder, 'uploaded_data')

from app import app

"""
SETUP THE API
TODO: consider use of "configparser" for this
API_BASEURL defaults to "localhost:5000" unless explicitly set
"""

OKBLUE = "\033[94m"
OKGREEN = "\033[92m"
WARNING = "\033[93m"
FAIL = "\033[91m"
ENDC = "\033[0m"

API_BASEURL=environ.get("GROWTH_API_BASEURL") or "http://localhost:5000"
print(f"{OKGREEN} * Growth Charts API_BASEURL is {API_BASEURL}{ENDC}")


"""
FLASK CLIENT ROUTES
"""

# FICTIONAL CHILD
@app.route("/fictionalchild", methods=["POST"])
def fictional_child():
    payload = {
        # "key" : "value"
    }
    data = requests.get(
        f"{API_BASEURL}/api/v1/json/fictionalchild",
        data = payload
    )
    
    return render_template("fictional_data.html", data=data)


# CALCULATIONS FORM
@app.route("/", methods=["GET", "POST"])
def home():
    form = MeasurementForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            payload = {
                "birth_date": form.birth_date.data,
                "observation_date": form.obs_date.data,
                "height_in_cm": float(form.height.data),
                "weight_in_kg": float(form.weight.data),
                "head_circ_in_cm": float(form.ofc.data),
                "sex": str(form.sex.data),
                "gestation_weeks": int(form.gestation_weeks.data),
                "gestation_days": int(form.gestation_days.data)
            }

            # collect user form entries and perform date and SDS/Centile calculations
            response = requests.post(
                f"{API_BASEURL}/api/v1/json/calculations",
                data=payload
            )
            print(response.json()) # to debug 500 error in client
            
            # serialize results before passing to test_results table
            table_results = response.json()

            ## results are on a single child and can be charted. Request chart data from api
            payload = {
                "results": json.dumps(table_results),
                "unique_child": "true"
            }

            # collect user form entries and perform date and SDS/Centile calculations
            try:
                chart_data = requests.post(
                    f"{API_BASEURL}/api/v1/json/chart_data",
                    data=payload
                )
            except ValueError as error:
                chart_data = None
                print(error)

            return render_template("test_results.html", table_result=table_results, chart_results=chart_data.json(), unique_child="true")

        # form not validated. Need flash warning here
        return render_template("measurement_form.html", form = form)
    else:
        ## delete files if still present
        # temp_directory = Path.cwd().joinpath("static").joinpath("uploaded_data")
        for filename in listdir(uploaded_data_folder):
            if filename:
                remove(path.join(uploaded_data_folder, filename))
        return render_template("measurement_form.html", form = form)


# GROWTH REFERENCES LIST
@app.route("/references", methods=["GET"])
def client_references():
    response = requests.get(f"{API_BASEURL}/api/v1/json/references") 
    return render_template("references.html", data=response.json() )


@app.route("/instructions", methods=["GET"])
def instructions():
    html = requests.get(f"{API_BASEURL}/api/v1/json/instructions")
    return render_template("instructions.html", fill=html.json())


# IMPORT EXCEL FILE
@app.route("/import", methods=["GET", "POST"])
def import_growth_data():
    form = FictionalChildForm()
    if request.method == "POST":
        ## can only receive .xls, .xlsx, or .csv files TODO need to chunk files
        file = request.files["file"]
        # static_directory = path.join(path.abspath(path.dirname(__file__)), "static/uploaded_data")
        # file.save(path.join(static_directory, file.filename))
        file.save(path.join(uploaded_data_folder, file.filename))
        return make_response("ok")
    else:
        return render_template("import.html", form=form)

@app.route("/uploaded_data/<id>", methods=["GET"])
def uploaded_data(id):
    global table_data
    if id=='sheet':
        # get file from store
        # static_directory = path.join(path.abspath(path.dirname(__file__)), "static/uploaded_data")
        global static_file
        global static_file_name
        for file_name in listdir(uploaded_data_folder):
            file_path = path.join(uploaded_data_folder, file_name)
            static_file = file_path
            static_file_name = file_name
        files = {'excel_file': (static_file_name, open(static_file, 'rb'))}
        try:
            response=requests.post(f"{API_BASEURL}/api/v1/json/spreadsheet", 
                files=files
            )
            remove(static_file)
        except:
            remove(static_file)
            return make_response("Error occurred", 500)
        if response.json()['valid']:
            table_data = response.json()['data']
            unique_child = response.json()['unique_child']
        else:
            error = response.json()['error']
            #pass this message to template

        if unique_child:
            ## the measurements are from a unique child - get the chart data
            try:
                payload = {
                            "results": json.dumps(table_data),
                            "unique_child": "true"
                        }
                chart_response = requests.post(f"{API_BASEURL}/api/v1/json/chart_data", data=payload )
                chart_data=chart_response.json()
            except:
                #error
                chart_data = None
        else: 
            chart_data = None
        
        unique_child_string = 'false'
        if unique_child:
            unique_child_string = 'true'
        return render_template("uploaded_data.html", table_data=table_data, chart_results=chart_data, unique_child=unique_child_string)

    elif id=="download":
        ## saves table_data json to excel format in static folder then deletes after download
        download_excel.save_as_excel(json.dumps(table_data))
        # temp_directory = Path.cwd().joinpath("static").joinpath("uploaded_data")
        file_path = path.join(uploaded_data_folder, "output.xlsx")
        return send_from_directory(directory=uploaded_data_folder, filename="output.xlsx", as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        @after_this_request
        def remove_file(filepath):
            remove(file_path)
            return redirect(url_for('home'))

if __name__ == "__main__":
    app.run()