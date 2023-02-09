function validate() // Required Fields Validation
{

    if (document.myForm.singer.value == "") {
        alert("Please enter Singer Name!", 'danger');
        document.myForm.singer.focus();
        return false;
    }

    if (document.myForm.count.value == "") {
        alert("Please enter Number of Videos!", 'danger');
        document.myForm.count.focus();
        return false;
    }

    if (document.myForm.duration.value == "") {
        alert("Please enter Duration of Each Video!", 'danger');
        document.myForm.duration.focus();
        return false;
    }

    if (document.myForm.emailid.value == "") {
        alert("Please enter Email ID!", 'danger');
        document.myForm.emailid.focus();
        return false;
    }

    if (document.myForm.count.value <= 10) {
        alert("Number of Videos must be a positive number greater than 10!", 'danger');
        document.myForm.count.focus();
        return false;
    }

    if (document.myForm.duration.value <= 20) {
        alert("Duration of Each Video must be a positive number greater than 20!!", 'danger');
        document.myForm.duration.focus();
        return false;
    }
    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if (!document.myForm.emailid.value.match(mailformat)) {
        alert("Please enter a valid Email ID!", 'danger');
        document.myForm.emailid.focus();
        return false;
    }

    return true;
}

