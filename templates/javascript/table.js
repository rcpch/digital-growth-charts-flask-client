///Javascript code for the table
$('.tabular.menu .item').tab();
$('#gestational_age_delivery_explain').popup({
    on: 'click',
    setFluidWidth: true,
    variation: 'wide green',
    html: '<p><b>Info: </b>This is the child\'s gestation at birth; it is the number of weeks since the last menstrual period.</p>'
});
$('#corrected_decimal_age_explain').popup({
    on: 'click',
    setFluidWidth: true,
    variation: 'wide green',
    html: '<p><b>Info: </b>This calculates the child\'s age from their expected due date, not their date of birth. This allows clinicians to compare them with other term babies the same age. It is considered 0 at term (37-42 weeks)</p>'
});
$('#chronological_decimal_age_explain').popup({
    on: 'click',
    setFluidWidth: true,
    variation: 'wide green',
    html: '<p><b>Info: </b>This reports the child\'s age from birth in years, expressed as a decimal.</p>'
});
$('#chronological_calendar_age_explain').popup({
    on: 'click',
    setFluidWidth: true,
    variation: 'wide green',
    html: '<p><b>Info: </b>This is the child\'s age from birth in years, months, weeks and days.</p>'
});
$('#corrected_calendar_age_explain').popup({
    on: 'click',
    setFluidWidth: true,
    variation: 'wide green',
    html: '<p><b>Info: </b>This is the child\'s age from their due date in years, months, weeks and days.</p>'
});
$('#estimated_date_delivery_explain').popup({
    on: 'click',
    setFluidWidth: true,
    variation: 'wide green',
    html: '<p><b>Info: </b>This is the child\'s due date.</p>'
});
$('#corrected_gestational_age_explain').popup({
    on: 'click',
    setFluidWidth: true,
    variation: 'wide green',
    html: '<p><b>Info: </b>For babies born preterm, this is their gestational age since birth up until 42 weeks.</p>'
});
$('#corrected_decimal_age').popup({
    on: 'click',
    setFluidWidth: true,
    variation: 'wide green',
    html: "<p><b>Clinician: </b>{{table_result[0].measurement_dates.clinician_decimal_age_comment}}</p><p><b>Parent/Carer:</b> {{table_result[0].measurement_dates.lay_decimal_age_comment}}</p>"
});
$('#height_centile').popup({
    on: 'click',
    setFluidWidth: true,
    variation: 'wide green',
    html: '<p><b>Clinician: </b>{% for measurement in table_result %}{% if measurement.measurement_calculated_values.clinician_height_comment and measurement.child_observation_value.clinician_height_comment is not none %}{{measurement.measurement_calculated_values.clinician_height_comment}}</p><p><b>Parent/Carer:</b> {{measurement.measurement_calculated_values.lay_height_comment}}{%endif%}{%endfor%}</p>'
});
$('#weight_centile').popup({
    on: 'click',
    setFluidWidth: true,
    variation: 'wide green',
    html: '<p><b>Clinician: </b>{% for measurement in table_result %}{% if measurement.measurement_calculated_values.clinician_weight_comment and measurement.child_observation_value.clinician_weight_comment is not none %}{{measurement.measurement_calculated_values.clinician_weight_comment}}</p><p><b>Parent/Carer:</b> {{measurement.measurement_calculated_values.lay_weight_comment}}{%endif%}{%endfor%}</p>'
});
$('#bmi_centile').popup({
    on: 'click',
    setFluidWidth: true,
    variation: 'wide green',
    html: '<p><b>Clinician: </b>{% for measurement in table_result %}{% if measurement.measurement_calculated_values.clinician_bmi_comment and measurement.child_observation_value.clinician_bmi_comment is not none %}{{measurement.measurement_calculated_values.clinician_bmi_comment}}</p><p><b>Parent/Carer:</b> {{measurement.measurement_calculated_values.lay_bmi_comment}}{%endif%}{%endfor%}</p>'
});
$('#ofc_centile').popup({
    on: 'click',
    setFluidWidth: true,
    variation: 'wide green',
    html: '<p><b>Clinician: </b>{% for measurement in table_result %}{% if measurement.measurement_calculated_values.clinician_ofc_comment and measurement.child_observation_value.clinician_ofc_comment is not none %}{{measurement.measurement_calculated_values.clinician_ofc_comment}}</p><p><b>Parent/Carer:</b> {{measurement.measurement_calculated_values.lay_ofc_comment}}{%endif%}{%endfor%}</p>'
});

function returnComment(array, measurement, clinician) {
    for(record in array) {
        console.log(record.measurement_calculated_values.clinician_bmi_comment);
        
    }
}