
from datetime import datetime
from os import path, listdir, remove, environ
from measurement_request import MeasurementForm, FictionalChildForm
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, make_response, jsonify, session
from flask_cors import CORS
import markdown
import requests
import json
from client_controllers import chunk_file, import_excel_data, download_excel
from werkzeug.utils import secure_filename
from pathlib import Path

# client side controller to manipulate excel sheet
"""
we have two options here: either upload the spreadsheet, store it temporarily client side in order to create the dataframe and 
manipulate fields client side here, or send the dataframe to the server. The second option is preferable
"""


app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = "UK_WHO" #not very secret - this will need complicating and adding to config
CORS(app)

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
        params = payload
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
            response = requests.get(
                f"{API_BASEURL}/api/v1/json/calculations",
                params=payload
            )
            
            # serialize results before passing to test_results table
            table_results = response.json()

            ## results are on a single child and can be charted. Request chart data from api
            payload = {
                "results": json.dumps(table_results),
                "unique_child": "true"
            }

            try:
                chart_data = requests.get(f"{API_BASEURL}/api/v1/json/chart_data", params=payload).json()
            except ValueError as error:
                chart_data = None
                print(error)
                
            return render_template("test_results.html", table_result=table_results, chart_results=chart_data, unique_child="true")

        # form not validated. Need flash warning here
        return render_template("measurement_form.html", form = form)
    else:
        return render_template("measurement_form.html", form = form)


# GROWTH REFERENCES LIST
@app.route("/references", methods=["GET"])
def client_references():
    response = requests.get(f"{API_BASEURL}/api/v1/json/references") 
    return render_template("references.html", data=response.json() )


# RESULTS
# @app.route("/results/<id>/<unique_child>/<data>", methods=["GET"])
# def results(id, unique_child, data):

#     # deserialize table json data before pass to test_results template
#     # table_results=json.loads(data)

#     #send results to chart api if unique child
#     if unique_child=="true":
#         payload = {
#             "results": json.dumps(table_results),
#             "unique_child": unique_child
#         }
#         chart_data = requests.get(f"{API_BASEURL}/api/v1/json/chart_data", params=payload )

#     if id == "table":
#         return render_template("test_results.html", table_result=table_results, chart_results=chart_data.json(), unique_child=unique_child)
#     if id == "chart":
#         return render_template("chart.html", data=results, unique_child=unique_child)


# CHART
# @app.route("/chart/<unique_child>/<data>", methods=["GET"])
# def chart(unique_child, data):

#     results = eval(data) # deserialised from string when passed from template
#     payload = {
#         "results": json.dumps(results),
#         "unique_child": unique_child
#     }
#     data = requests.get(f"{API_BASEURL}/api/v1/json/chart_data", params=payload )
#     return render_template("chart.html", data=data.json())


@app.route("/instructions", methods=["GET"])
def instructions():
    html = requests.get(f"{API_BASEURL}/api/v1/json/instructions")
    return render_template("instructions.html", fill=html.json())


# IMPORT EXCEL FILE
@app.route("/import", methods=["GET", "POST"])
def import_growth_data():
    form = FictionalChildForm()
    if request.method == "POST":
        ## can only receive .xls, .xlsx, or .csv files
        file = request.files["file"]
        static_directory = path.join(path.abspath(path.dirname(__file__)), "static/uploaded_data")
        file_to_save = path.join(static_directory, secure_filename(file.filename))
        controller_response = chunk_file.chunk_file(file, file_to_save)
        return make_response(controller_response["response"], controller_response["response_code"])
    else:
        return render_template("import.html", form=form)


# UPLOAD EXCEL FILE?
# TODO: Definitely needs to be deprecated in favour of a PR model of submitting reference data
@app.route("/uploaded_data/<id>", methods=["GET", "POST"])
## excel now uploaded. Needs validating
def uploaded_data(id):
    global requested_data
    global unique_child
    if id=="sheet":
        # get file from static directory and check if meets criteria and then set flag unique_child
        static_directory = path.join(path.abspath(path.dirname(__file__)), "static/uploaded_data")
        for file_name in listdir(static_directory):
            if file_name != "dummy_data.xlsx":
                """
                Loop through static/upload folder
                Avoid the example sheet
                Save there temporarily, import the data then delete
                """
                file_path = path.join(static_directory, file_name)
                try:
                    # import the data from excel and validate, delete the file once imported (True flag)
                    child_data = import_excel_data.import_excel_sheet(file_path, True)
                    # extract the dataframe - rejected if not in the correct format. Date convert to ISO8601 here.
                    data_frame = child_data["data"]
                    unique_child = child_data["unique_child"] #API returns if these data are from one child
                    
                    
                except ValueError as e:
                    
                    """
                    Error handler - uploaded sheet is incompatible: missing essential data
                    """
                    print(e)
                    flash(f"{e}")
                    data=None
                    render_template("uploaded_data.html", data=data, unique_child=False, dynamic_calculations=None)

                except LookupError as l:
                    
                    """
                    Error handler - uploaded sheet is incompatible: headings are missing or too many or misspelled
                    """

                    data=None
                    print(l)
                    flash(f"{l}")
                    data=None
                    render_template("uploaded_data.html", data=data, unique_child=False, dynamic_calculations=None)
                
                else:
                    """
                    Data is correct format
                    Load as JSON and report to table
                    If the imported data is all same patient (on basis of unique birth_date),
                    offer the opportunity to chart it, calculate velocity and acceleration of most recent parameters
                    """
                    #serialise dataframe as JSON
                    data = json.loads(data_frame)
                    
                    #pass data to the api for calculation
                    payload = {
                        "uploaded_data": json.dumps(data)
                    }

                    # calculate the uploaded data sds and centiles.
                    data = requests.get(f"{API_BASEURL}/api/v1/json/serial_data_calculations", params=payload)
                    
                    # store the response as JSON in global variable for conversion back to excel format for download if requested
                    requested_data=data.json()
                    
                    # TODO - create endpoint to calculate velocity +/- correlated weight centiles
                    # dynamic_calculations = controllers.calculate_velocity_acceleration(formatted_child_data)

                    # if unique_child (ie data only from one child and not multiple children), these data can be plotted
                    # make a second call to the api for the growth chart data
                    if unique_child=="true":
                        payload = {
                            "results": json.dumps(requested_data),
                            "unique_child": unique_child
                        }
                        chart_data = requests.get(f"{API_BASEURL}/api/v1/json/chart_data", params=payload )
                    else: 
                        chart_data = None
                    
                    return render_template("uploaded_data.html", table_data=requested_data, chart_results=chart_data.json(), unique_child=unique_child)
            else:
                #TODO this is the example sheet - download and return the data
                return render_template("uploaded_data.html", data=requested_data, chart_data=None, unique_child=unique_child)
                            
            # return render_template("uploaded_data.html", data=data, unique_child=unique_child, dynamic_calculations = dynamic_calculations)
            # if id=="get_excel": 
            #     
    elif id=="download":
        ## broken needs fix - file deleted so can"t download
        download_excel.save_as_excel(requested_data)
        temp_directory = Path.cwd().joinpath("static").joinpath("uploaded_data")
        send_from_directory(directory=temp_directory, filename="output.xlsx", as_attachment=True)
        file_path = temp_directory.joinpath("output.xlsx")
        # remove(file_path)
        return render_template("uploaded_data.html", data=requested_data, unique_child=unique_child)

if __name__ == "__main__":
    app.run()
