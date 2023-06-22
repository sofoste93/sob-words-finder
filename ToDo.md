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

## Backend logic for utils

>> authentication.py
>
>import random
>import string


>>def generate_credentials():
    """Generate a random username and a 5-digit PIN."""
    username = ''.join(random.choices(string.ascii_letters, k=5))
    pin = ''.join(random.choices(string.digits, k=5))
    return username, pin


>>def verify_credentials(username, pin, session):
    """Verify if the provided username and PIN match the ones stored in session."""
    return session.get('username') == username and session.get('pin') == pin 

>> finder.py
> 
>import os
>from PyPDF2 import PdfFileReader


>>def find_word_in_txt(file_path, word):
    """Search for the word in a .txt file and return the line numbers where it was found."""
    with open(file_path, 'r') as file:
        lines = file.readlines()

    results = [i for i, line in enumerate(lines) if word in line]
    return results


>>def find_word_in_pdf(file_path, word):
    """Search for the word in a .pdf file and return the page numbers where it was found."""
    with open(file_path, 'rb') as file:
        pdf = PdfFileReader(file)
        results = []

        for i in range(pdf.getNumPages()):
            page = pdf.getPage(i)
            if word in page.extractText():
                results.append(i)

    return results


>>def find_word(file_path, word):
    """Choose the right function depending on the file's extension and execute it."""
    _, extension = os.path.splitext(file_path)

    if extension == '.txt':
        return find_word_in_txt(file_path, word)
    elif extension == '.pdf':
        return find_word_in_pdf(file_path, word)

>> operations.py
>
>import operator
>import random
> 
>>def generate_operation():
    """Generate a random arithmetic operation and its result."""
    ops = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.floordiv
    }
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    op = random.choice(list(ops.keys()))
    result = ops[op](num1, num2)
    return f"{num1} {op} {num2}", result
> 
>>def verify_answer(answer, session):
    """Verify if the provided answer matches the stored result."""
    return session.get('result') == int(answer)

## Flask app logic

>> app.py
>
 