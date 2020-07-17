![RCPCH Logo](https://www.rcpch.ac.uk/themes/rcpch/images/logo-desktop.svg)

# Demo Python/Flask client for the RCPCH Digital Growth Charts API

This repo contains a Python/Flask application which demonstrates the capabilities of the RCPCH Digital Growth Charts API. The client passes all calculations to the API, no calculations are done in the client.

You *must* have the RCPCH Digital Growth Charts API running somewhere for this client to work.

## Python development environment setup and running the API locally

For details of our typical Python development setup, see the API repository https://github.com/rcpch/digital-growth-charts/blob/master/docs/dev-documentation/python-development.md where there are instructions for setting up the correct Python versions, installing dependencies, and then running the API locally for development and testing purposes.

### Running the Python/Flask Growth Charts client application

These instructions assume you are also running the API application on the same machine, which is why it reassigns the client's Flask port to 5001, on the presumption that the API is on 5000. If you are using an alternative setup then you can just run Flask on 5000.

* `git clone` this repository into a suitable location on your development machine  
`$ git clone https://github.com/rcpch/digital-growth-charts-flask-client.git`  
* `cd` into the directory  
`$ cd digital-growth-charts-flask-client`  
* install the Python dependencies  
`$ pip install -r requirements.txt`  
* Tell Flask you are in Development mode  
`$ export FLASK_ENV=development`
* Set up Flask so it knows what your app is called  
`$ export FLASK_APP=app.py`  
* Tell your client where the API is located (defaults to 5000 for now)
`$ export GROWTH_API_BASEURL=http://localhost:5000`  
* Run Flask on port 5001  
`$ flask run -h localhost -p 5001`  
* All of that in a single line command: `export FLASK_ENV=development;export FLASK_APP=app.py;export GROWTH_API_BASEURL=http://localhost:5000;flask run -h localhost -p 5001`

## Endpoints
- `/` This endpoint accepts a GET request and returns age, centile and SDS calculations of children's growth data. A typical response is shown below in [Arguments](#Arguments). Note that growth reference data **do not** exist to calculate SDS or centiles for:
1. Height/Length below 25 weeks gestation
2. BMI below 2 weeks of age (post 40 weeks)
3. OFC (occipitofrontal circumference) above 17y in girls and >18y in boys.
In these circumstances, `NoneType` is returned.

- `/results/table` : Reports anthropometric data entered via the webform with calculated values (ages/SDS and centile values with clinical guidance) as a table.

- `/results/chart` : Plots data entered via the webform, or uploaded in .xlsx format, as growth charts. Charts have capability to zoom in and out.

- `/chart_data` : a JSON dump of the centile chart data

- `/import` : accepts a POST request to upload an excel spreadsheet of mixed patient data (for example for research purposes), or serial growth data over time for individual patients. The upload format for each is different and prescribed. Mandatory column names are: 'birth_date', 'observation_date', 'gestation_weeks','gestation_days', 'sex', 'measurement_type', 'measurement_value'. These are case sensitive. measurement_type must be lower case and one of 'height', 'weight', 'ofc', 'bmi'. This must be anonymised as is in the public domain. Any columns other than those prescribed will be stripped and discarded. No data is retained on the server.

- `/uploaded_data/example` : this is a sample spreadsheet of fictional data for users to try

- `/uploaded_data/excel_spreadsheet` : redirected here once an excel spreadsheet of data has been uploaded.

- `/references` : currently is a hardcoded list (stored as JSON) of national and international growth references (not the datasets themselves), with literature references and authorship, date of publication. The intention is for this to be stored in a database and available opensource (with some governance) for users to update and use. In future it is intended to be a national standard for growth reference publication and provide guidance on growth reference development.

- `/instructions` : currently renders this readme.md. In future is intended to be a resource to help users access the API, as well as details of the API licence, rules of use and disclaimers.

## Open Source License

This work is Copyright ⓒ2020 The Royal College of Paediatrics and Child Health, and is released under the MIT Open Source License  

## Contributing
### How to contribute

* Fork the repository to your own GitHub account
* Set up your development environment (ideally using our instructions [here](python-development.md) for maximum compatibility with our own development environments)
* Ideally, you should have discussed with our team what you are proposing to change, because we can only accept pull requests where there is an accepted need for that new feature or fix.
* We can discuss with you how we would recommend to implement the new feature, for maximum potential 'mergeability' of your PR.
* Once the work is ready to show us, create a pull request on our repo, detailing what the change is and details about the fix or feature. PRs that affect the calculations or any other 'mission critical' part of the code will need suitable tests which we can run.
* We will endeavour to review and merge in a reasonable time frame, but will usually not merge straight into `master`, rather we will merge into an upcoming release branch.

### Coding style

* We are not Python experts but we would encourage use of Python best practices where possible.
* We are not going to get too pedantic over style though.
* Some helpful sources of information on Python style are:  
https://www.python.org/dev/peps/pep-0008  
https://google.github.io/styleguide/pyguide.html  


### Intellectual Property (IP)

* The copyright over the IP in this repository is owned by the Royal College of Paediatrics and Child Health, which releases it under an open source license.
* If you submit a contribution to the repository, you agree to transfer all IP rights over the contribution, both now and in the future, to the Royal College of Paediatrics and Child Health, in perpetuity.
* For larger contributions we may require a Contributor Covenant to support this agreement over transfer of title, however for small contributions it is probably sufficient that you should have read and understood this document, and that the act of submitting a PR is acceptance of these terms.
* All contributors will be acknowledged in the [Acknowledgements](acknowledgements.md) section.