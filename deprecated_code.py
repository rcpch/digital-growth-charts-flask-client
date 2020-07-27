"""
# This endpoint is to upload an excel spreadsheet of a child or children's growth data. Data persisted transiently
# while it is imported as a dataframe into PANDAS and then deleted. The code for this currently is in a client side controller.
# TODO #4 Move the converation from EXCEL to PANDAS functions from client_controller to the api.
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
                
                # Loop through static/upload folder
                # Avoid the example sheet
                # Save there temporarily, import the data then delete
                
                file_path = path.join(static_directory, file_name)
                try:
                    # import the data from excel and validate, delete the file once imported (True flag)
                    child_data = import_excel_data.import_excel_sheet(file_path, True)
                    # extract the dataframe - rejected if not in the correct format. Date convert to ISO8601 here.
                    data_frame = child_data["data"]
                    unique_child = child_data["unique_child"] #API returns if these data are from one child

                    
                except ValueError as e:
                    
                    
                    #Error handler - uploaded sheet is incompatible: missing essential data
                    
                    print(e)
                    flash(f"{e}")
                    data=None
                    render_template("uploaded_data.html", data=data, unique_child=False, dynamic_calculations=None)

                except LookupError as l:
                    
                    
                    #Error handler - uploaded sheet is incompatible: headings are missing or too many or misspelled
                    

                    data=None
                    print(l)
                    flash(f"{l}")
                    data=None
                    render_template("uploaded_data.html", data=data, unique_child=False, dynamic_calculations=None)
                
                else:
                    
                    # Data is correct format
                    # Load as JSON and report to table
                    # If the imported data is all same patient (on basis of unique birth_date),
                    # offer the opportunity to chart it, calculate velocity and acceleration of most recent parameters
                    
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

    elif id=="download":
        download_excel.save_as_excel(json.dumps(requested_data))
        temp_directory = Path.cwd().joinpath("static").joinpath("uploaded_data")
        file_path = temp_directory.joinpath("output.xlsx")
        return send_from_directory(directory=temp_directory, filename="output.xlsx", as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        @after_this_request
        def remove_file(filepath):
            remove(file_path)
            return redirect(url_for('home'))
"""