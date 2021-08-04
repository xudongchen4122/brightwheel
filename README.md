How to install and run my service:

1) Download the project from https://github.com/xudongchen4122/brightwheel
2) In MacOS or Linux environment, open terminal or bash shell
3) CD to brightwheel folder (where the project resides)
4) "ls" to make sure env folder is there
5) run the command "source env/bin/activate"
6) run the command "python3 -m pip install -r requirements.txt"
7) Open setup/settings.py file and comment/uncomment the following lines to set the default email provider
    # DEFAULT_EMAIL_PROVIDER = 'snailgun'
    DEFAULT_EMAIL_PROVIDER = 'spendgrid'
8) Save the changes
9) run the command "python3 manage.py runserver"
8) Now use Postman or any online request service (eg: https://reqbin.com/) to test the following services:
    a) Send Email : 
        POST http://127.0.0.1:8000/emails/
        data : 
            {
                "from_email": "noreply@mybrightwheel.com",
                "from_name": "brightwheel",
                "to_email": "susan@abcpreschool.org",
                "to_name": "Miss Susan",
                "subject": "Your Weekly Report",
                "body": "<h1>Weekly Report</h1><p>You saved 10 hours this week!</p>"
            }
    
        *** Note: It will check if any of the above entries is empty. Also, it will check if the email 
                  addresses are in valid format.
                  
    b) Get All Emails :
        GET http://127.0.0.1:8000/emails/
        
    c) Get a Single Email:
        GET http://127.0.0.1:8000/emails/?id=1 
            *** Note: If the default email provider is snailgun, this request will also check the email's current 
                status. If the current status is not SENT, it will retrieve this email's email_id (got from the response
                of the initial send_email request) and use it to send a request to snailgun to get the most recent 
                status and update it in the database
                
        Or,
        
        GET http://127.0.0.1:8000/emails/?email_id=snailgun_email_YShL8z2OWjpXmg9KO9OMrfP4
            *** This only works if the default email provider is snailgun. It will check the email's current status.
                If the current status is not SENT, this will send a request to snailgun to get the most recent 
                status and update it in the database
                
How to run unit tests:
1) Make sure you are still in the virtual environment (check "how to run this project" above)
2) run the command "export DJANGO_SETTINGS_MODULE=setup.settings"
3) run the command "pytest"


Programming Language: Python (This is my most proficient programming language and I use it everyday)
Framework: Django and Django Rest Framework (Django and Rest Framework go with Python hand in hand. I use these everyday also)
Libraries: pytest, pytest-django, requests (pytest is for unit testing. requests library is used for sending POST and GET requests)
Database: Sqlite3 (I need a very lightweight portable database to save the emails for this small project. 
          Sqlite3 is the default database for Django project)
          

Due to time constraint, I couldn't create a good UI to make it easier for user to enter the information to send email. 
I could certainly make it better with more time!

