$("#myformerror").hide();  //hide error box

function submitmodalform(submit_url){
//compile all data to be submitted
let formData = {};
//get all inputs, text area, selects
$.each($("#myform input, #myform textarea, #myform select"), function (key, value) {
    //formulate name:value pair
    formData[$(value).attr("name")] = $(value).val();
});
//overwirte values for an ajax file uploaders
//get only uploaders
$.each($("#myform input[control_type='file_uploader']"), function (key, value) {
    //formulate name:value pair
    formData[$(value).attr("uploader_for")] = $(value).val();
});
// console.log(formData);
//hide error box
$("#myformerror").hide();

$.ajax({
    type: "POST",
    url: submit_url,
    data: formData,
    dataType: "json",
    encode: true,
}).done(function (data) {
    if (data.error == true)
    {

        //remove all fld erros
        $('[obj_type="fld_errors"]').remove();

        //show all field errors
        //if we have errors
        if (data.form_errors)
        {
            $.each(data.form_errors, function (fld, msg) {
                //formulate name:value pair
                // console.log(fld, msg);
                //fidn and draw error message
                let er_msq = '<div obj_type="fld_errors" class="alert alert-danger  alert-dismissible fade show mt-2" role="alert">' + msg + '</div>';
                //place it
                $('label[for="'+ fld + '"]').append(er_msq);
            }); 
        }
    }
    else{
        //redirect
        window.location.href = submit_url;
    }
    // console.log(data);
});

}

function start_tempUpload(control_id){
    $('#form_for_'+control_id).submit(); // Submit the form
}