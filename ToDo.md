# How you to create this app / project

## First, create a new Python virtual environment and install necessary libraries.

>>python -m venv sobWordsFinder_env
source sobWordsFinder_env/bin/activate
pip install flask flask_bootstrap flask_uploads PyPDF2 docx2txt

## HTML Templates

>>>>>>
> 
>> landing.html 
{
<!DOCTYPE html>
<html>
<head>
    <title>Welcome Page</title>
    <link href="../static/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1>Welcome to sobWordsFinder!</h1>
        <p>Solve the following operation to proceed</p>
        <form action="/validate_operation" method="post">
            <h3>{{ operation }}</h3>
            <input type="text" id="answer" name="answer">
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    </div>
</body>
</html>

>>>>>>
> 
>> login.html 
> <!DOCTYPE html>
<html>
<head>
    <title>Login Page</title>
    <link href="../static/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1>Login</h1>
        <form action="/login" method="post">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username">
            <label for="pin">PIN:</label>
            <input type="text" id="pin" name="pin">
            <button type="submit" class="btn btn-primary">Login</button>
        </form>
    </div>
</body>
</html>

>>>>>>
> 
>> search.html
<!DOCTYPE html>
<html>
<head>
    <title>Search Page</title>
    <link href="../static/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1>{{ title }}</h1>
        <form action="/search" method="post" enctype="multipart/form-data">
            <label for="word">Word:</label>
            <input type="text" id="word" name="word">
            {% if is_custom %}
                <label for="file">Upload file:</label>
                <input type="file" id="file" name="file">
            {% endif %}
            <button type="submit" class="btn btn-primary">Search</button>
        </form>
        {% if results %}
            <h2>Results:</h2>
            <ul>
                {% for result in results %}
                    <li>{{ result }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    </div>
</body>
</html>

>>
>