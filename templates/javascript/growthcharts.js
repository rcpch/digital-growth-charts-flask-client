var girl = 'rgba(217, 49, 155, 1.0)';
      var boy = 'rgba(0, 126, 198, 1.0)';
      var sex_color = ''
      var height_centiles = []
      var weight_centiles = []
      var bmi_centiles = []
      var ofc_centiles = []
      var max_ticks = 0;
      var measurements = ['height', 'weight', 'bmi', 'ofc'];

      var results = JSON.parse('{{chart_results|tojson|safe}}')
      
      if (results.sex == 'male') {
        sex_color = boy;
      }
      if (results.sex == 'female') {
        sex_color = girl;
      }
      
      // select which centile charts to show
      if(results.child_data.heights.length > 0){
        height_centiles = results.centile_data.height
      }
      if(results.child_data.weights.length > 0){
        weight_centiles = results.centile_data.weight
      }  
      if(results.child_data.bmis.length > 0){
        bmi_centiles = results.centile_data.bmi
      }
      if(results.child_data.ofcs.length > 0){
        ofc_centiles = results.centile_data.ofc
      }
      
    
      for (i=0; i<measurements.length; i++){

        var centile_data_set = [];
        
        // var pointfourth, second, ninth, twenty_fifth, fiftieth, seventy_fifth, ninety_first, ninety_eighth, ninety_ninth = [];
        measurement_label = ''
        axis_label=''

        if(measurements[i] == 'height'){
          // centile_data_set = results.centile_data.height_centiles;
          centile_data_set = height_centiles
          axis_label = "Length/Height (cm)";
          measurement_label = 'Length/Height';
          child_measurement = results.child_data.heights; // child measurements
          max_ticks = 200;
        }
        if(measurements[i] == 'weight') {
          // centile_data_set 
          centile_data_set = weight_centiles;
          axis_label = "Weight (kg)";
          measurement_label = 'Weight';
          child_measurement = results.child_data.weights // child measurements
          max_ticks = 180;
        }
        if(measurements[i] == 'bmi') {
          centile_data_set = bmi_centiles;
          axis_label = "BMI (kg/2)";
          measurement_label = 'Body Mass Index';
          child_measurement = results.child_data.bmis; // child measurements
          max_ticks = 65;
        }
        if(measurements[i] == 'ofc') {
          centile_data_set = ofc_centiles;
          axis_label = "Head Circumference (cm)";
          measurement_label = 'Head Circumference';
          child_measurement = results.child_data.ofcs; // child measurements
          max_ticks = 70;
        }

          var data = {
                // labels:results.data.sds,
                datasets:[ /// preterm to term UK90
                  {
                    label: '0.4th',  /// preterm to term UK90
                    data: centile_data_set[0].uk90_preterm_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    pointStyle: 'dash',
                    borderDash: [15, 5],
                    pointRadius: 0,
                    lineTension: 0,
                    cubicInterpolationMode: false
                  },
                  {
                    label: '2nd', /// preterm to term UK90
                    data: centile_data_set[1].uk90_preterm_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    spanGaps: false,
                    pointRadius: 0,
                    lineTension: 0
                  },
                  {
                    label: '9th',  /// preterm to term UK90
                    data: centile_data_set[2].uk90_preterm_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    pointStyle: 'dash',
                    borderDash: [15, 5],
                    pointRadius: 0,
                    lineTension: 0,
                    cubicInterpolationMode: false             
                  },
                  {
                    label: '25th', /// preterm to term UK90
                    data: centile_data_set[3].uk90_preterm_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    spanGaps: false,
                    pointRadius: 0,
                    lineTension: 0
                  },
                  {
                    label: '50th',  /// preterm to term UK90
                    data: centile_data_set[4].uk90_preterm_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    pointStyle: 'dash',
                    borderDash: [15, 5],
                    pointRadius: 0,
                    lineTension: 0,
                    cubicInterpolationMode: false             
                  },
                  {
                    label: '75th', /// preterm to term UK90
                    data: centile_data_set[5].uk90_preterm_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    spanGaps: false,
                    pointRadius: 0,
                    lineTension: 0
                  },
                  {
                    label: '91st',  /// preterm to term UK90
                    data: centile_data_set[6].uk90_preterm_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    pointStyle: 'dash',
                    borderDash: [15, 5],
                    pointRadius: 0,
                    lineTension: 0,
                    cubicInterpolationMode: false              
                  },
                  {
                    label: '98th', /// preterm to term UK90
                    data: centile_data_set[7].uk90_preterm_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    spanGaps: false,
                    pointRadius: 0,
                    lineTension: 0
                  },
                  {
                    label: '99.6th',  /// preterm to term UK90
                    data: centile_data_set[8].uk90_preterm_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    pointStyle: 'dash',
                    borderDash: [15, 5],
                    pointRadius: 0,
                    lineTension: 0,
                    cubicInterpolationMode: false
                  },
                  ///term WHO infant data
                  {
                    label: '0.4th',  /// WHO infant 
                    data: centile_data_set[0].who_infant_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    pointStyle: 'dash',
                    borderDash: [15, 5],
                    pointRadius: 0,
                    lineTension: 0,
                    cubicInterpolationMode: false
                  },
                  {
                    label: '2nd', /// WHO infant 
                    data: centile_data_set[1].who_infant_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    spanGaps: false,
                    pointRadius: 0,
                    lineTension: 0
                  },
                  {
                    label: '9th',  /// WHO infant 
                    data: centile_data_set[2].who_infant_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    pointStyle: 'dash',
                    borderDash: [15, 5],
                    pointRadius: 0,
                    lineTension: 0,
                    cubicInterpolationMode: false
                  },
                  {
                    label: '25th', /// WHO infant 
                    data: centile_data_set[3].who_infant_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    spanGaps: false,
                    pointRadius: 0,
                    lineTension: 0
                  },
                  {
                    label: '50th',  /// WHO infant 
                    data: centile_data_set[4].who_infant_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    pointStyle: 'dash',
                    borderDash: [15, 5],
                    pointRadius: 0,
                    lineTension: 0,
                    cubicInterpolationMode: false
                  },
                  {
                    label: '75th', /// WHO infant 
                    data: centile_data_set[5].who_infant_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    spanGaps: false,
                    pointRadius: 0,
                    lineTension: 0
                  },
                  {
                    label: '91st',  /// WHO infant 
                    data: centile_data_set[6].who_infant_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    pointStyle: 'dash',
                    borderDash: [15, 5],
                    pointRadius: 0,
                    lineTension: 0,
                    cubicInterpolationMode: false
                  },
                  {
                    label: '98th', /// WHO infant 
                    data: centile_data_set[7].who_infant_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    spanGaps: false,
                    pointRadius: 0,
                    lineTension: 0
                  },
                  {
                    label: '99.6th',  /// WHO infant 
                    data: centile_data_set[8].who_infant_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    pointStyle: 'dash',
                    borderDash: [15, 5],
                    pointRadius: 0,
                    lineTension: 0,
                    cubicInterpolationMode: false
                  },
                  //who child
                  {
                    label: '0.4th',  /// who standing data set
                    data: centile_data_set[0].who_child_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    pointStyle: 'dash',
                    borderDash: [15, 5],
                    pointRadius: 0,
                    lineTension: 0,
                    cubicInterpolationMode: false
                  },
                  {
                    label: '2nd', /// who standing data set
                    data: centile_data_set[1].who_child_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    spanGaps: false,
                    pointRadius: 0,
                    lineTension: 0
                  },
                  {
                    label: '9th',  /// who standing data set
                    data: centile_data_set[2].who_child_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    pointStyle: 'dash',
                    borderDash: [15, 5],
                    pointRadius: 0,
                    lineTension: 0,
                    cubicInterpolationMode: false
                  },
                  {
                    label: '25th', /// who standing data set
                    data: centile_data_set[3].who_child_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    spanGaps: false,
                    pointRadius: 0,
                    lineTension: 0
                  },
                  {
                    label: '50th',  /// who standing data set
                    data: centile_data_set[4].who_child_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    pointStyle: 'dash',
                    borderDash: [15, 5],
                    pointRadius: 0,
                    lineTension: 0,
                    cubicInterpolationMode: false
                  },
                  {
                    label: '75th', /// who standing data set
                    data: centile_data_set[5].who_child_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    spanGaps: false,
                    pointRadius: 0,
                    lineTension: 0
                  },
                  {
                    label: '91st',  /// who standing data set
                    data: centile_data_set[6].who_child_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    pointStyle: 'dash',
                    borderDash: [15, 5],
                    pointRadius: 0,
                    lineTension: 0,
                    cubicInterpolationMode: false
                  },
                  {
                    label: '98th', /// who standing data set
                    data: centile_data_set[7].who_child_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    spanGaps: false,
                    pointRadius: 0,
                    lineTension: 0
                  },
                  {
                    label: '99.6th',  /// who standing data set
                    data: centile_data_set[8].who_child_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    pointStyle: 'dash',
                    borderDash: [15, 5],
                    pointRadius: 0,
                    lineTension: 0,
                    cubicInterpolationMode: false
                  },
                  ////uk90 standing
                  {
                    label: '0.4th',  /// UK90 children
                    data: centile_data_set[0].uk90_child_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    pointStyle: 'dash',
                    borderDash: [15, 5],
                    pointRadius: 0,
                    lineTension: 0,
                    cubicInterpolationMode: false
                  },
                  {
                    label: '2nd', /// UK90 children
                    data: centile_data_set[1].uk90_child_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    spanGaps: false,
                    pointRadius: 0,
                    lineTension: 0
                  },
                  {
                    label: '9th',  /// UK90 children
                    data: centile_data_set[2].uk90_child_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    pointStyle: 'dash',
                    borderDash: [15, 5],
                    pointRadius: 0,
                    lineTension: 0,
                    cubicInterpolationMode: false
                  },
                  {
                    label: '25th', /// UK90 children
                    data: centile_data_set[3].uk90_child_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    spanGaps: false,
                    pointRadius: 0,
                    lineTension: 0
                  },
                  {
                    label: '50th',  /// UK90 children
                    data: centile_data_set[4].uk90_child_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    pointStyle: 'dash',
                    borderDash: [15, 5],
                    pointRadius: 0,
                    lineTension: 0,
                    cubicInterpolationMode: false
                  },
                  {
                    label: '75th', /// UK90 children
                    data: centile_data_set[5].uk90_child_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    spanGaps: false,
                    pointRadius: 0,
                    lineTension: 0
                  },
                  {
                    label: '91st',  /// UK90 children
                    data: centile_data_set[6].uk90_child_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    pointStyle: 'dash',
                    borderDash: [15, 5],
                    pointRadius: 0,
                    lineTension: 0,
                    cubicInterpolationMode: false
                  },
                  {
                    label: '98th', /// UK90 children
                    data: centile_data_set[7].uk90_child_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    spanGaps: false,
                    pointRadius: 0,
                    lineTension: 0
                  },
                  {
                    label: '99.6th',  /// UK90 children
                    data: centile_data_set[8].uk90_child_data,
                    fill: false,
                    showLine: true,
                    borderColor: sex_color,
                    borderWidth: 0.5,
                    pointStyle: 'dash',
                    borderDash: [15, 5],
                    pointRadius: 0,
                    lineTension: 0,
                    cubicInterpolationMode: false
                  },
                  ///patient data
                  {
                    label: 'Measurement',
                    data: child_measurement,
                    fill: false,
                    borderColor: 'rgba(0, 0, 0, 1.0)',
                    borderWidth: 1.0,
                    pointRadius: 1.0,
                    pointStyle: 'circle',
                  },

                ]
              }

              var options = {
                    title:{
                      display: true,
                      position: 'top',
                      text: measurement_label
                    },
                    legend: {
                      display: false
                    },
                    scales: {
                      xAxes: [{
                        scaleLabel: {
                          display: true,
                          labelString: 'Age (yrs)',
                          fontFamily: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
                          fontStyle: 'bold'
                        },
                        type: 'linear',
                        position: 'bottom',
                        ticks: {
                          min: -0.3,
                          max: 20,
                          stepSize: 0.5,
                          fixedStepSize: 0.5,
                          fontStyle: 'bold'
                        }
                      }],
                      yAxes: [{
                        scaleLabel: {
                          display: true,
                          labelString: axis_label,
                          fontStyle: 'bold'
                        },
                        ticks: {
                          min: 0,
                          max: max_ticks,
                          fontStyle: 'bold'
                        }
                      }]
                    },
                    plugins: {
                      zoom: {
                        // zoom: {
                        //   // Container for pan options
                        //   pan: {
                        //     // Boolean to enable panning
                        //     enabled: true,

                        //     // Panning directions. Remove the appropriate direction to disable
                        //     // Eg. 'y' would only allow panning in the y direction
                        //     // A function that is called as the user is panning and returns the
                        //     // available directions can also be used:
                        //     //   mode: function({ chart }) {
                        //     //     return 'xy';
                        //     //   },
                        //     mode: 'xy',

                        //     rangeMin: {
                        //       // Format of min pan range depends on scale type
                        //       x: null,
                        //       y: null
                        //     },
                        //     rangeMax: {
                        //       // Format of max pan range depends on scale type
                        //       x: null,
                        //       y: null
                        //     },

                        //     // On category scale, factor of pan velocity
                        //     speed: 20,

                        //     // Minimal pan distance required before actually applying pan
                        //     threshold: 10,

                        //     // Function called while the user is panning
                        //     onPan: function({chart}) { console.log(`I'm panning!!!`); },
                        //     // Function called once panning is completed
                        //     onPanComplete: function({chart}) { console.log(`I was panned!!!`); }
                        //   },

                          // Container for zoom options
                          zoom: {
                            // Boolean to enable zooming
                            enabled: true,

                            // Enable drag-to-zoom behavior
                            drag: true,

                            // Drag-to-zoom effect can be customized
                            // drag: {
                            // 	 borderColor: 'rgba(225,225,225,0.3)'
                            // 	 borderWidth: 5,
                            // 	 backgroundColor: 'rgb(225,225,225)',
                            // 	 animationDuration: 0
                            // },

                            // Zooming directions. Remove the appropriate direction to disable
                            // Eg. 'y' would only allow zooming in the y direction
                            // A function that is called as the user is zooming and returns the
                            // available directions can also be used:
                            //   mode: function({ chart }) {
                            //     return 'xy';
                            //   },
                            mode: 'xy',

                            // Speed of zoom via mouse wheel
                            // (percentage of zoom on a wheel event)
                            speed: 0.05,

                            // Minimal zoom distance required before actually applying zoom
                            threshold: 2,

                            // On category scale, minimal zoom level before actually applying zoom
                            sensitivity: 3,

                            // Function called while the user is zooming
                            onZoom: function({chart}) { console.log(`I'm zooming!!!`); },
                            // Function called once zooming is completed
                            onZoomComplete: function({chart}) { console.log(`I was zoomed!!!`); }
                          }
                        } //zoom
                      } //plugins
                    }//options
                  

                if (measurements[i] == 'height'){
                  var heightCtx = document.getElementById('heightChart').getContext('2d');
                  var heightChart = new Chart(heightCtx, {
                    type: 'scatter',
                    data: data,
                    options: options
                  });
                }
                if (measurements[i] == 'weight'){
                  var weightCtx = document.getElementById('weightChart').getContext('2d');
                  var weightChart = new Chart(weightCtx, {
                    type: 'scatter',
                    data: data,
                    options: options
                  });
                }
                if (measurements[i] == 'bmi'){
                  var bmiCtx = document.getElementById('bmiChart').getContext('2d');
                  var bmiChart = new Chart(bmiCtx, {
                    type: 'scatter',
                    data: data,
                    options: options
                  });
                }
                if (measurements[i] == 'ofc'){
                  var ofcCtx = document.getElementById('ofcChart').getContext('2d');
                  var ofcChart = new Chart(ofcCtx, {
                    type: 'scatter',
                    data: data,
                    options: options
                  });
                }
      }