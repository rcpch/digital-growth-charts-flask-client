from client_controllers import save_as_csv
from datetime import datetime
from flask import Flask, Response, render_template, request, flash, redirect, url_for, send_from_directory, make_response, jsonify, abort, send_file, session
from flask_cors import CORS
from flask_dropzone import Dropzone
from measurement_request import MeasurementForm, FictionalChildForm
from os import path, listdir, remove, environ, urandom
from pathlib import Path
from werkzeug.utils import secure_filename

import markdown
import requests
import json


#######################
##### FLASK SETUP #####
app = Flask(__name__, static_folder="static")
CORS(app)
Dropzone(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Declare shell colour variables for logging output
OKBLUE = "\033[94m"
OKGREEN = "\033[92m"
WARNING = "\033[93m"
FAIL = "\033[91m"
ENDC = "\033[0m"

# Load the secret key from the ENV if it has been set
if "FLASK_SECRET_KEY" in environ:
    app.secret_key = environ["FLASK_SECRET_KEY"]
    print(f"{OKGREEN} * FLASK_SECRET_KEY was loaded from the environment{ENDC}")
# Otherwise create a new one. (NB: We don't need session persistence between reboots of the app)
else:
    app.secret_key = urandom(16)
    print(f"{OKGREEN} * A new SECRET_KEY for Flask was automatically generated{ENDC}")

# Declare paths for temporary uploads folder
assets_folder = path.join(app.root_path, 'static')
uploaded_data_folder = path.join(assets_folder, 'uploaded_data')

from app import app

##### END FLASK SETUP #####
###########################


#####################
##### API SETUP #####
# TODO: consider use of "configparser" for this
# API_BASEURL defaults to "localhost:5000" unless explicitly set

API_BASEURL = environ.get(
    "GROWTH_API_BASEURL") or "http://localhost:5000/"
print(f"{OKGREEN} * Growth Charts API_BASEURL is {API_BASEURL}{ENDC}")

##### END API SETUP #####
#########################


# FICTIONAL CHILD
@app.route("/fictionalchild", methods=["POST"])
def fictional_child():
    payload = {
        # "key" : "value"
    }
    data = requests.get(
        f"{API_BASEURL}/utilities/create_fictional_child_measurements",
        data=payload
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
                f"{API_BASEURL}/uk-who/calculations",
                data=payload
            )
            print(response.json())  # to debug 500 error in client

            # serialize results before passing to test_results table
            table_results = response.json()

            # results are on a single child and can be charted. Request chart data from api
            payload = {
                "results": json.dumps(table_results),
                "unique_child": "true"
            }

            # collect user form entries and perform date and SDS/Centile calculations
            try:
                chart_data = requests.post(
                    f"{API_BASEURL}/uk-who/chart-data",
                    data=payload
                )
            except ValueError as error:
                chart_data = None
                print(error)

            return render_template("test_results.html", table_result=table_results, chart_results=chart_data.json(), unique_child="true")

        # form not validated. Need flash warning here
        return render_template("measurement_form.html", form=form)
    else:
        # delete files if still present
        # temp_directory = Path.cwd().joinpath("static").joinpath("uploaded_data")
        clear_upload_folder()
        return render_template("measurement_form.html", form=form)


# GROWTH REFERENCES LIST
@app.route("/references", methods=["GET"])
def client_references():
    response = requests.get(f"{API_BASEURL}/utilities/references")
    return render_template("references.html", data=response.json())


@app.route("/instructions", methods=["GET"])
def instructions():
    html = requests.get(f"{API_BASEURL}/utilities/instructions")
    return render_template("instructions.html", fill=html.json())


# IMPORT EXCEL FILE
@app.route("/import", methods=["GET", "POST"])
def import_growth_data():
    form = FictionalChildForm()
    # empty out file system
    clear_upload_folder()
    if request.method == "POST":

        # can only receive .csv files TODO need to chunk files
        file = request.files["file"]
        file.filename = "output.csv"
        file = {'csv_file': file}

        # send file to API
        try:
            response = requests.post(f"{API_BASEURL}/uk-who/spreadsheet",
                                     files=file
                                     )
        except:
            return make_response("Error occurred", 500)
        # save response as json in filesystem + csv.

        # need to pass on unique_child flag to uploaded_date
        if response.json()['valid']:
            # save the excel file in uploaded_data folder
            save_as_csv.save_as_csv(
                response.json()['data'], uploaded_data_folder)
            # save the data as json in data.txt in uploaded_data folder
            new_json_data_file = path.join(uploaded_data_folder, 'data.txt')
            with open(new_json_data_file, 'w') as outfile:
                json.dump(response.json()['data'], outfile)

            unique_child = response.json()['unique_child']
            # store unique_child in a session
            session['unique_child'] = unique_child
        else:
            error = response.json()['error']
            return make_response(error)

        return make_response(json.dumps({'success': True}), 200, {'ContentType': 'application/json'})
    else:
        return render_template("import.html", form=form)


@app.route("/uploaded_data", methods=["GET"])
def uploaded_data():
    # retrieve the json file from the filesystem
    file_path = path.join(uploaded_data_folder, "data.txt")
    with open(file_path, "r") as json_file:
        table_data = json.loads(json_file.read())

    unique_child = session.get('unique_child')

    if unique_child:
        # the measurements are from a unique child - get the chart data
        try:
            payload = {
                "results": json.dumps(table_data),
                "unique_child": "true"
            }
            chart_response = requests.post(
                f"{API_BASEURL}/uk-who/chart-data", data=payload)
            chart_data = chart_response.json()
        except:
            # error
            chart_data = None
    else:
        chart_data = None

    unique_child_string = 'false'
    if unique_child:
        unique_child_string = 'true'
    return render_template("uploaded_data.html", table_data=table_data, chart_results=chart_data, unique_child=unique_child_string)


@app.route("/download")
def download():
    # saves table_data to excel format in static folder then deletes after download
    try:
        response = send_from_directory(
            directory=uploaded_data_folder, filename="output.csv", as_attachment=True, mimetype='text/csv')
        return response
    except:
        print("error")
    finally:
        clear_upload_folder()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(410)
def gone(e):
    return render_template('410.html'), 410


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


def clear_upload_folder():
    for file in listdir(uploaded_data_folder):
        filepath = path.join(uploaded_data_folder, file)
        if path.exists(filepath):
            remove(filepath)


if __name__ == "__main__":
    app.run()
