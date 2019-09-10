function ValidateFileUpload(input, user_id, user_type) {
  var fuData = document.getElementById('avatar');
  var FileUploadPath = fuData.value;
  var Extension = FileUploadPath.substring(
    FileUploadPath.lastIndexOf('.') + 1).toLowerCase();
  if (Extension == "gif" || Extension == "png" || Extension == "bmp"
    || Extension == "jpeg" || Extension == "jpg") {
    if (fuData.files[0].size > 3e+6) {
      alert("File size must be less than or equal to 3 MB.");
      fuData.value = '';
      fuData.src = '';
    } else {
      if (fuData.files && fuData.files[0]) {
        $(".loaderdiv").show()
        var reader = new FileReader();
        reader.onload = function (e) {
          $.ajax({
            url: '/user-image',
            type: "POST",
            dataType: 'json',
            data: {
              uuid: user_id,
              avatar: e.target.result,
              user_type: user_type,
              csrfmiddlewaretoken: '{{ csrf_token }}',
            },
            success: function (success) {
              $('#signup-image').attr('src', e.target.result)
                .height(220);
              $('#signup-image-header').attr('src', e.target.result);
              $(".loaderdiv").hide()
            }
          });
        }
        reader.readAsDataURL(fuData.files[0]);
      }
    }
  }
  else {
    fuData.value = '';
    alert("Photo only allows file types of GIF, PNG, JPG, JPEG and BMP. ");

  }
}

function validateresumeupload() {
  var fuData = document.getElementById('resume');
  var FileUploadPath = fuData.value;
  var Extension = FileUploadPath.substring(
    FileUploadPath.lastIndexOf('.') + 1).toLowerCase();

  file = document.getElementById('resume').value
  if (Extension == "pdf") {
    if (fuData.files[0].size > 3e+6) {
      alert("File size must be less than or equal to 3 MB.");
      fuData.value = '';
      fuData.src = '';
    } else {
      document.getElementById("resume").innerHTML = file;
      $("#proposal").val(fuData.files[0].name)
      $("#fileuploadmessage").text(fuData.files[0].name)
    }
  }
  else {
    fuData.value = '';
    alert("It only allows file types of pdf.");
  }

}


validateform = function () {
  var flag = 0;
  if (validateoldpass())
    flag++;
  if (validatepass())
    flag++;
  if (confirmPassword())
    flag++;
  if (flag == 3)
    return true;
  else
    return false;
}


validateResetform = function () {
  var flag = 0;

  if (validatepass())
    flag++;
  if (confirmPassword())
    flag++;
  if (flag == 2)
    return true;
  else
    return false;
}

changepasswordform = function () {
  var flag = 0;
  if (validateoldpass()) {
    flag++;
  }
  if (validatepass()) {
    flag++;
  }
  if (confirmPassword()) {
    flag++;
  }
  if (flag == 3) {
    return true;
  } else {
    return false;
  }
}

validatelogin = function () {
  var flag = 0;

  if (validatepass())
    flag++;
  if (validateemail())
    flag++;

  if (flag == 2)
    return true;
  else
    return false;
}

validatestep1form = function () {
  var flag = 0;
  if (validatecompanyname())
    flag++;
  if (validatefirstname())
    flag++;
  if (validatelastname())
    flag++;
  if (validatepass())
    flag++;
  if (confirmPassword())
    flag++;
  if (flag == 5)
    return true;
  else
    return false;
}


validateoldpass = function () {
  var password = $('#old_password').val();
  if (password.length == "") {
    $('#oldpassword_error').html("Password field should not be empty");
    $('#oldpassword_error').css("color", "red");
    $('#oldpassword_error').show();
    return false;
  }
  else {
    $('#oldpassword_error').hide();
    return true;
  }
}

validatepass = function () {
  var password = $('#new_password').val();
  var confirmpassword = $('#confirm_password:visible').val();
  var regex = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,16}$/;

  if (password.length == "") {
    $('#newpassword_error').html("Password field should not be empty");
    $('#newpassword_error').css("color", "red");
    $('#newpassword_error').show();
    return false;
  } else if (password.length < 8) {
    $('#newpassword_error').html("Password length too short.");
    $('#newpassword_error').css("color", "red");
    $('#newpassword_error').show();
    return false;
  } else if (!regex.test(password)) {
    $('#newpassword_error').html("Password must contain 1 number, 1 uppercase value and 1 lowercase value.");
    $('#newpassword_error').css("color", "red");
    $('#newpassword_error').show();
    return false;
  } else if (confirmpassword && password != confirmpassword) {
    $('#confirmpassword_error').html("Password does not match.");
    $('#confirmpassword_error').css("color", "red");
    $('#confirmpassword_error').show();
    return false;
  } else {
    if (confirmpassword && password == confirmpassword) {
      $('#confirmpassword_error').hide();
    }
    $('#newpassword_error').hide();
    return true;
  }
}


confirmPassword = function () {
  var password = $('#new_password:visible').val();
  var confirmpassword = $('#confirm_password:visible').val();

  if (confirmpassword.length == "") {
    $('#confirmpassword_error').html("Confirm password field should not be empty");
    $('#confirmpassword_error').css("color", "red");
    $('#confirmpassword_error').show();
    return false;
  } else if (password && password != confirmpassword) {
    $('#confirmpassword_error').html("Password does not match.");
    $('#confirmpassword_error').css("color", "red");
    $('#confirmpassword_error').show();
    return false;
  } else {
    $('#confirmpassword_error').hide();
    return true;
  }
}


validateemail = function () {
  var EmailId = $('#email').val();
  var regex = /^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;

  if (EmailId.length == "") {
    $('#email_error').html("Please input a email id.");
    $('#email_error').css("color", "red");
    $('#email_error').show();
    return false;
  } else if (EmailId.indexOf("@", 0) < 0) {
    $('#email_error').html("Please input valid email id format.");
    $('#email_error').css("color", "red");
    $('#email_error').show();
    return false;
  }
  else if (!regex.test(EmailId)) {
    $('#email_error').html("Please input valid email id format.");
    $('#email_error').css("color", "red");
    $('#email_error').show();
    return false;
  } else {
    $('#email_error').hide();
    return true;
  }
}


validatefirstname = function () {

  var name = $('#first_name').val();
  var regex = /^([a-zA-Z ])+$/;

  if (name == "") {
    $('#firstname_error').html("Name field should not be empty.");
    $('#firstname_error').css("color", "red");
    $('#firstname_error').show();
    return false;
  }
  else if (!regex.test(name)) {
    $('#firstname_error').html("Please input only characters.");
    $('#firstname_error').css("color", "red");
    $('#firstname_error').show();
    return false;
  }
  else {
    $('#firstname_error').hide();
    return true;
  }
}


validatecompanyname = function () {

  var name = $('#company_name').val();
  var regex = /^([a-zA-Z ])+$/;

  if (name == "") {
    $('#firstname_error').html("Name field should not be empty.");
    $('#firstname_error').css("color", "red");
    $('#firstname_error').show();
    return false;
  }
  // else if (!regex.test(name)) {
  //   $('#firstname_error').html("Please input only characters.");
  //   $('#firstname_error').css("color", "red");
  //   $('#firstname_error').show();
  //   return false;
  // }
  else {
    $('#firstname_error').hide();
    return true;
  }
}


validatelastname = function () {

  var name = $('#last_name').val();
  var regex = /^([a-zA-Z ])+$/;

  if (name == "") {
    $('#lastname_error').html("Name field should not be empty.");
    $('#lastname_error').css("color", "red");
    $('#lastname_error').show();
    return false;
  }
  else if (!regex.test(name)) {
    $('#lastname_error').html("Please input only characters.");
    $('#lastname_error').css("color", "red");
    $('#lastname_error').show();
    return false;
  }
  else {
    $('#lastname_error').hide();
    return true;
  }
}





validate_education_details = function () {
  var flag = 0;
  if (validateschoolname())
    flag++;
  if (validatedegree())
    flag++;
  if (validatefield())
    flag++;
  if (validategrade())
    flag++;
  if (validate_activities())
    flag++;
  if (validate_description())
    flag++;
  if (validate_year())
    flag++;
  if (flag == 7)
    return true;
  else
    return false;
}

validateschoolname = function () {

  var name = $('#school').val();
  var regex = /^([a-zA-Z ])+$/;

  if (name == "") {
    $('#schoolname_error').html("This field is required*.");
    $('#schoolname_error').css("color", "red");
    $('#schoolname_error').show();
    return false;
  }
  // else if (!regex.test(name)) {
  //   $('#schoolname_error').html("Please input only characters.");
  //   $('#schoolname_error').css("color", "red");
  //   $('#schoolname_error').show();
  //   return false;
  // } 
  else {
    $('#schoolname_error').hide();
    return true;
  }
}

validatelocation = function () {

  var name = $('#location').val();
  var regex = /^([a-zA-Z ])+$/;

  if (name == "") {
    $('#locationerror').html("City and Country should not be empty.");
    $('#locationerror').css("color", "red");
    $('#locationerror').show();
    return false;
  }
  // else if (!regex.test(name)) {
  //   $('#locationerror').html("Please input only characters.");
  //   $('#locationerror').css("color", "red");
  //   $('#locationerror').show();
  //   return false;
  // } 
  else {
    $('#locationerror').hide();
    return true
  }
}
validatedegree = function () {
  var name = $('#degree').val();
  var regex = /^([a-zA-Z'-.* ])+$/;
  if (name == "") {
    $('#degreename_error').html("This field is required*.");
    $('#degreename_error').css("color", "red");
    $('#degreename_error').show();
    return false;
  }
  else if (!regex.test(name)) {
    $('#degreename_error').html("Please input only characters.");
    $('#degreename_error').css("color", "red");
    $('#degreename_error').show();
    return false;
  } else {
    $('#degreename_error').hide();
    return true;
  }
}

validatecity = function () {
  var name = $('#city').val();
  var regex = /^([a-zA-Z ])+$/;
  if (name == "") {
    $('#cityname_error').html("This field is required*.");
    $('#cityname_error').css("color", "red");
    $('#cityname_error').show();
    return false;
  }
  else if (!regex.test(name)) {
    $('#cityname_error').html("Please input only characters.");
    $('#cityname_error').css("color", "red");
    $('#cityname_error').show();
    return false;
  } else {
    $('#cityname_error').hide();
    return true;
  }
}

employement = function () {
  var flag = 0;

  if (validatecompanyname())
    flag++;
  if (validatelocation())
    flag++;
  if (validatetitle())
    flag++;
  if (!$("#currently").is(":checked") && validate_year_employment()) {
    flag++;
  }
  if ($("#currently").is(":checked") && validate_start_year()) {
    flag++;
  }
  if (flag == 4)
    return true;
  else
    return false;
}


validate_start_year = function () {
  var from_month = $('#from_month').val();
  var from_year = $('#from_year1').val();

  var current_date = new Date()
  var current_month = current_date.getMonth()
  console.log("Current Month" + current_month)
  var current_year = current_date.getFullYear()
  console.log("Current Year" + current_year)

  if (from_month == "" || from_year == "") {
    $('#frommontherror').html("Please enter your joining Month and year.");
    $('#frommontherror').css("color", "red");
    $('#frommontherror').show();
    return false;
  } else if (from_month && from_year && current_year == from_year && parseInt(from_month) > current_month) {
    $('#frommontherror').html("You can't select future month of current year.");
    $('#frommontherror').css("color", "red");
    $('#frommontherror').show();
    return false;
  } else {
    $('#frommontherror').hide();
    $('#errors').hide();
  }
  return true
}



validate_year_employment = function () {


  var from_month = $('#from_month').val();
  console.log("from_month" + from_month)

  var to_month = $('#to_month').val();
  console.log("to_month" + to_month)

  from_year = $('#from_year1').val();
  console.log("from_year" + from_year)

  to_year = $('#to_year1').val();
  console.log("to_year" + to_year)

  var current_date = new Date()
  var current_month = current_date.getMonth()
  console.log("Current Month" + current_month)
  var current_year = current_date.getFullYear()
  console.log("Current Year" + current_year)

  if (from_month && from_year && (from_year == current_year) && (parseInt(from_month) > current_month + 1)) {
    $('#frommontherror').html("You can't select future month of current year.");
    $('#frommontherror').css("color", "red");
    $('#frommontherror').show();
    return false;
  } else {
    $('#frommontherror').hide();
    $('#errors').hide();
  }

  if (to_month && to_year && (to_year == current_year) && (parseInt(to_month) > current_month + 1)) {
    $('#montherror').html("You can't select future month of current year.");
    $('#montherror').css("color", "red");
    $('#montherror').show();
    return false;
  } else {
    $('#frommontherror').hide();
    $('#errors').hide();
  }

  if (from_month != "" && to_month != "" && (from_month > to_month) && (from_year == to_year)) {
    $('#montherror').html("Please select valid Month.");
    $('#montherror').css("color", "red");
    $('#montherror').show();
    return false;
  }
  else if (from_year && to_year && from_year > to_year) {
    $('#errors').html("Please enter valid durations.");
    $('#errors').css("color", "red");
    $('#errors').show();
    return false;
  }
  else {
    $('#montherror').hide();
    $('#errors').hide();
  }
  return true;
}


// validateemployeeneed = function () {
//   var flag = 0;

//   if (validateemployee())
//     flag++;

//   if (flag == 1)
//     return true;
//   else
//     return false;
// }


validateemployee = function () {

  var employee_need = $('#employee').val();
  var regex = /^([[0-9])+$/;

  if (employee_need == "") {
    $('#employeeerror').html("Field should not be empty.");
    $('#employeeerror').css("color", "red");
    $('#employeeerror').show();
    return false;
  }
  else if (!regex.test(employee_need)) {
    $('#employeeerror').html("Please input only digits.");
    $('#employeeerror').css("color", "red");
    $('#employeeerror').show();
    return false;
  } else {
    $('#employeeerror').hide();
    return true;
  }
}

validatefield = function () {

  var name = $('#field_of_study').val();
  var regex = /^([a-zA-Z'-.* ])+$/;

  if (name == "") {
    $('#field_error').html("This field is required*.");
    $('#field_error').css("color", "red");
    $('#field_error').show();
    return false;
  }
  else if (!regex.test(name)) {
    $('#field_error').html("Please input only characters.");
    $('#field_error').css("color", "red");
    $('#field_error').show();
    return false;
  } else {
    $('#field_error').hide();
    return true;
  }
}

validategrade = function () {

  var name = $('#grade').val();
  var regex = /^([a-zA-Z ])+$/;
  return true
  // if (name == "") {
  //   $('#grade_error').html("This field is required*.");
  //   $('#grade_error').css("color", "red");
  //   $('#grade_error').show();
  //   return false;
  // }
  // else {
  //   $('#grade_error').hide();
  //   return true;
  // }
}

validate_activities = function () {

  var name = $('#activities_socities').val();
  var regex = /^([a-zA-Z ])+$/;
  return true
  if (name == "") {
    $('#validate_activities_error').html("This field is required*.");
    $('#validate_activities_error').css("color", "red");
    $('#validate_activities_error').show();
    return false;
  }
  else if (!regex.test(name)) {
    $('#validate_activities_error').html("Please input only characters.");
    $('#validate_activities_error').css("color", "red");
    $('#validate_activities_error').show();
    return false;
  } else {
    $('#validate_activities_error').hide();
    return true;
  }
}

validate_description = function () {

  var name = $('#education_description').val();
  var regex = /^([a-zA-Z ])+$/;
  return true
  if (name == "") {
    $('#description_error').html("This field is required*.");
    $('#description_error').css("color", "red");
    $('#description_error').show();
    return false;
  }
  else if (!regex.test(name)) {
    $('#description_error').html("Please input only characters.");
    $('#description_error').css("color", "red");
    $('#description_error').show();
    return false;
  } else {
    $('#description_error').hide();
    return true;
  }
}
function validate_year() {
  from_year = document.getElementById('from_year').value;
  to_year = document.getElementById('to_year').value;

  if (parseInt(from_year) > parseInt(to_year)) {
    link = document.getElementById('errors')
    document.getElementById('errors').innerHTML = "*Your end year can’t be earlier than your start year.";
    link.style.display = 'block';
  }
  else {
    link = document.getElementById('errors')
    link.style.display = 'none';
    return true;
  }
  return false;
}



isValidmobile = function () {

  var mobile = $('#mobile').val();
  var regex = /^([[0-9&\/\\#,+()$~%.'":*?<>{}-])+$/;


  if (mobile == "") {
    $('#mobile_error').html("Mobile number cannot be empty*.");
    $('#mobile_error').css("color", "red");
    $('#mobile_error').show();
    return false;
  }
  else if (!regex.test(mobile)) {
    $('#mobile_error').html("Please input only digits.");
    $('#mobile_error').css("color", "red");
    $('#mobile_error').show();
    return false;
  }
  else {
    $('#mobile_error').hide();
    return true;
  }
}


Deletepostedjob = function (uuid) {
  $(".loaderdiv").show()
  $.ajax({
    url: '/posted-job-delete/' + uuid,
    type: "GET",
    dataType: 'json',
    data: {
      'uuid': uuid,
    },
    success: function (success) {
      $('#deleteJobModal').modal("hide");
      deletedpostedjobs.hidden = true;
      $('#profile-tab a[href="#tab2"]').tab('show');
      $(".loaderdiv").hide()
    }
  });

}
var deletedpostedjobs;
function DeleteJob(element) {
  deletedpostedjobs = $(element).parents("li")[0];
  //  console.log($(element).parents("li"))
}




validatetitle = function () {

  var name = $('#title').val();
  var regex = /^([a-zA-Z ])+$/;

  if (name == "") {
    $('#title_error').html("Job title field should not be empty.");
    $('#title_error').css("color", "red");
    $('#title_error').show();
    return false;
  }
  // else if (!regex.test(name)) {
  //   $('#title_error').html("Please input only characters.");
  //   $('#title_error').css("color", "red");
  //   $('#title_error').show();
  //   return false;
  // }
  else {
    $('#title_error').hide();
    return true;
  }
}

jobstep1validation = function () {
  var flag = 0;

  if (validatetitle())
    flag++;
  if (flag == 1)
    return true;
  else
    return false;
}

heartcolour = function () {
  $(".heart").toggle(
    function () {
      $(this).css({ "color": "#007bff" });
      $(this).show();
    },
    function () {
      $(this).css({ "color": "#7adb4c" });
      $(this).show();
    });
}

function favouritejobs() {
  if (document.getElementById("heart").style.color == 'dimgrey') {
    document.getElementById("heart").style = 'color:#7adb4c';

  }
  else {
    document.getElementById("heart").style = 'color:dimgrey'
  }

}


set_location = function () {
  var flag = 0;

  if (isValidmobile())
    flag++;
  if (validatecity())
    flag++;
  if (validate_postal_code())
    flag++;

  if (flag == 3)
    return true;
  else
    return false;
}

validate_postal_code = function () {

  var pincode = $('#postal_code').val();
  var regex = /^([[a-zA-z0-9 ])+$/;


  if (pincode == "") {
    $('#postal_error').html("This field is required*.");
    $('#postal_error').css("color", "red");
    $('#postal_error').show();
    return false;
  }
  else if (!regex.test(pincode)) {
    $('#postal_error').html("Please input only alphanumeric.");
    $('#postal_error').css("color", "red");
    $('#postal_error').show();
    return false;
  } else {
    $('#postal_error').hide();
    return true;
  }
}

validate_hours = function () {

  var hours = $('#hours').val();


  if (hours == "") {
    $('#hours_error').html("This field is required*.");
    $('#hours_error').css("color", "red");
    $('#hours_error').show();
    return false;
  }
  else {
    $('#hours_error').hide();
    return true;
  }
}