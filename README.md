# sob-words-finder
> A simple web app to help you find any word referenced in a text 
> file you the app allows you to upload. Logic written in python. 
> Feel free to find bug and contribute; happy coding. ;-)

## Project breakdown

>sobWordsFinder/<br>
    ├── app.py<br>
    ├── static/<br>
    │   ├── css/<br>
    │   └── js/<br>
    ├── templates/<br>
    │   ├── landing.html<br>
    │   ├── login.html<br>
    │   ├── dashboard.html<br>
    │   └── search.html<br>
    ├── uploads/<br>
    └── utils/<br>
        ├── authentication.py<br>
        ├── operations.py<br>
        └── finder.py<br>

 ## Project Components:
 
> - app.py: This is the main entry point of the application. It will initialize the Flask app, set up routes, and handle requests and responses.

> - static folder: This will contain Bootstrap files (CSS and JS), and potentially any other static files.

> - templates folder: This will contain all HTML templates.

> - landing.html: This will display a simple math question to the user. On correct answer, it redirects to the login page with auto-generated credentials.

> - login.html: This page will allow the user to login using the provided credentials. Successful login redirects to the dashboard.

> - dashboard.html: This page will contain two main buttons/links: one for the default finder and one for the custom finder.

> - search.html: This will be used for both default and custom finder pages. It will include a form for inputting a search term and for uploading a file in case of the custom finder. It will also display the search results.

> - uploads folder: This will store all uploaded files.

> - utils folder: This will contain Python scripts for the application's backend logic.

> - authentication.py: This will handle the generation of credentials and login verification.

> - operations.py: This will handle the generation of random arithmetic operations and verification of the user's answer.

> - finder.py: This will contain the logic for searching a document for a specific word, both for the default and the custom finder.

> In the front-end, we use HTML templates with Bootstrap 5 for styling.
> 