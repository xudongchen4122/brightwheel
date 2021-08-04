import requests
from setup.settings import BASE_URL
from setup.settings import DEFAULT_EMAIL_PROVIDER


def test_send_email():
    url = BASE_URL + 'emails/'
    data = {
        "from_email": "noreply@mybrightwheel.com",
        "from_name": "brightwheel",
        "to_email": "susan@abcpreschool.org",
        "to_name": "Miss Susan",
        "subject": "Your Weekly Report",
        "body": "<h1>Weekly Report</h1><p>You saved 10 hours this week!</p>"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 201


def test_get_emails():
    url = BASE_URL + 'emails/'
    response = requests.get(url)
    assert response.status_code == 200


def test_get_email():
    if DEFAULT_EMAIL_PROVIDER == 'snailgun':
        url = BASE_URL + 'emails/?id=1'
        response = requests.get(url)
        assert response.status_code == 200

# test_send_email()
# test_get_emails()
# test_get_email()



