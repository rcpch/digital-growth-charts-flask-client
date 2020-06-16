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

## Open Source License

This work is Copyright (c)2020 The Royal College of Paediatrics and Child Health, and is released under the MIT Open Source License  

## Contributing