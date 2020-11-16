![RCPCH Logo](https://www.rcpch.ac.uk/themes/rcpch/images/logo-desktop.svg)

# DEPRECATED Demo Python/Flask client for the RCPCH Digital Growth Charts API

This repo contains a **DEPRECATED** Python/Flask application which demonstrates the capabilities of the RCPCH Digital Growth Charts API. It was produced as part of developing the RCPCH Digital Growth Charts API server, which is at a separate repository https://github.com/rcpch/digital-growth-charts-server.

It has been retained purely for demonstration purposes. AT this point the Flask client still works against our API, but we don't guarantee that future API cnahges will not break it. Our currently-developed demo client is built in React and is here https://github.com/rcpch/digital-growth-charts-react-client

If there are people who find this Flask client useful and wish us to continue maintenance of it, or indeed wish to contribute to the project by maintaining it for us, then please get in touch.

The client passes all calculations to the API, no calculations are done in the client. Therefore you _must_ have the RCPCH Digital Growth Charts API running somewhere for this client to work.

## Python development environment setup and running the API locally

For details of our typical Python development setup, see the API repository https://github.com/rcpch/digital-growth-charts/blob/master/docs/dev-documentation/python-development.md where there are instructions for setting up the correct Python versions, installing dependencies, and then running the API locally for development and testing purposes.

### Running the Python/Flask Growth Charts client application

These instructions assume you are also running the API application on the same machine, which is why it reassigns the client's Flask port to 5001, on the presumption that the API is on 5000. If you are using an alternative setup then you can just run Flask on 5000.

- Clone this repository into a suitable location on your development machine  
  `$ git clone https://github.com/rcpch/digital-growth-charts-flask-client.git`
- Move into the directory  
  `$ cd digital-growth-charts-flask-client`
- Install the Python dependencies  
  `$ pip install -r requirements.txt`
- Run the development script  
  ` $ s/start-flask-client`  
  If you need to vary any of the parameters passed to Flask, you can either modify the startup script or simply pass the commands to the shell manually.
  Scripts are located in the `s/` folder in the application root.
- Using the development script, by default the Flask client will run at http://localhost:5001, and expects an API server at http://localhost:5000
- Visit http://localhost:5001 in a web browser to see and use the client, which is largely self-explanatory.

## Open Source License

This work is Copyright ⓒ 2020 The Royal College of Paediatrics and Child Health, and is released under the MIT Open Source License

## Contributing

### How to contribute

- Fork the repository to your own GitHub account
- Set up your development environment (ideally using our instructions [here](python-development.md) for maximum compatibility with our own development environments)
- Ideally, you should have discussed with our team what you are proposing to change, because we can only accept pull requests where there is an accepted need for that new feature or fix.
- We can discuss with you how we would recommend to implement the new feature, for maximum potential 'mergeability' of your PR.
- Once the work is ready to show us, create a pull request on our repo, detailing what the change is and details about the fix or feature. PRs that affect the calculations or any other 'mission critical' part of the code will need suitable tests which we can run.
- We will endeavour to review and merge in a reasonable time frame, but will usually not merge straight into `master`, rather we will merge into an upcoming release branch.

### Coding style

- We are not Python experts but we would encourage use of Python best practices where possible.
- We are not going to get too pedantic over style though.
- Most of the team are using the PyLint formatter in VSCode
- Some helpful sources of information on Python style are:  
  https://www.python.org/dev/peps/pep-0008  
  https://google.github.io/styleguide/pyguide.html

### Technical acknowledgements

The following is a list of some of the resources, tools and frameworks used to build the Flask Demo Client

- [Flask](https://flask.palletsprojects.com/en/1.1.x/quickstart/) - microframework for Python web projects
- [FlaskForms](https://github.com/wtforms/wtforms/) - forms and validation.
- [Jinja2](https://pypi.org/project/Jinja2/) templating engine.
- [Werkzeug](https://palletsprojects.com/p/werkzeug/) - WSGI web application library
- [DropzoneJS](https://www.dropzonejs.com/) - an open source javascript library for drag'n'drop file uploads.
- Chris Griffith, Code Calamity - An implementation of his published method on chunking large files on upload.
- [Semantic UI](https://semantic-ui.com/) - CSS framework
- [ChartJS](https://www.chartjs.org/) - Javascript charting package

### Intellectual Property (IP)

- The copyright over the IP in this repository is owned by the Royal College of Paediatrics and Child Health, which releases it under an open source license.
- If you submit a contribution to the repository, you agree to transfer all IP rights over the contribution, both now and in the future, to the Royal College of Paediatrics and Child Health, in perpetuity.
- For larger contributions we may require a Contributor Covenant to support this agreement over transfer of title, however for small contributions it is probably sufficient that you should have read and understood this document, and that the act of submitting a PR is acceptance of these terms.
- All contributors will be acknowledged in the [Acknowledgements](acknowledgements.md) section.
