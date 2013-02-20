ERR_BAD_CREDENTIALS = -1;
ERR_USER_EXISTS = -2;
ERR_BAD_USERNAME = -3;
ERR_BAD_PASSWORD  = -4;

function makeJsonRequest(page, dict, success)
{
    $.ajax({
        type: "POST",
        url: page,
        data: JSON.stringify(dict),
        contentType: "application/json",
        dataType: "json",
        success: success,
    });
}

function getErrorMessage(errCode)
{
    if(errCode == ERR_BAD_CREDENTIALS)
    {
        return ("Invalid username and password combination. Please try again.");
    }
    else if(errCode == ERR_BAD_USERNAME)
    {
        return ("The user name should not be empty. Please try again.");
    }
    else if(errCode == ERR_USER_EXISTS)
    {
        return ("This user name already exists. Please try again.");
    }
    else if(errCode == ERR_BAD_PASSWORD)
    {
        return ("The password should be at most 128 characters long. Please try again.");
    }
}
