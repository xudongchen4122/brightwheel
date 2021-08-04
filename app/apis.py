from rest_framework import serializers, generics
from rest_framework.exceptions import APIException
from .models import Email
from enum import Enum
from setup.settings import API_KEYS, DEFAULT_EMAIL_PROVIDER
import requests
import re


# QUEUED and FAILED enums only apply to snailgun
class Status(Enum):
    QUEUED = 'QUEUED'
    SENT = 'SENT'
    FAILED = 'FAILED'


# EmailListSerializer handles creating emails and sending emails in the backend
class EmailListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Email

        fields = (
            'id',
            'to_email',
            'to_name',
            'from_email',
            'from_name',
            'subject',
            'body',
            'status',
            'email_id',
            'sent_date',
            'update_date',
        )

    # When a POST on BASE_URL + emails is called, it will call this create method to create the email, send it to the
    # email provider defined in DEFAULT_EMAIL_PROVIDER and then save it to the database
    def create(self, validated_data):
        email = Email(**validated_data)
        email.subject = email.subject.strip()
        email.body = email.body.strip()
        email.to_name = email.to_name.strip()
        email.to_email = email.to_email.strip()
        email.from_name = email.from_name.strip()
        email.from_email = email.from_email.strip()

        if email.subject == '':
            raise APIException('Subject cannot be empty!')

        if email.to_name == '':
            raise APIException('To_name cannot be empty!')

        if email.to_email == '':
            raise APIException('To_email cannot be empty!')
        elif not EmailListSerializer.validate_email(email.to_email):
            raise APIException('Invalid to_email format!')

        if email.from_name == '':
            raise APIException('From_name cannot be empty!')

        if email.from_email == '':
            raise APIException('From_email cannot be empty!')
        elif not EmailListSerializer.validate_email(email.from_email):
            raise APIException('Invalid from_email format!')

        data = None
        # the data is little different between spendgrid and snailgun
        if DEFAULT_EMAIL_PROVIDER == 'spendgrid':
            data = {
                'sender': f'{email.from_name} <{email.from_email}>',
                'recipient': f'{email.to_name} <{email.to_email}>',
                'subject': email.subject,
                'body': email.body
            }
        elif DEFAULT_EMAIL_PROVIDER == 'snailgun':
            data = {
                'from_email': email.from_email,
                'from_name': email.from_name,
                'to_email': email.to_email,
                'to_name': email.to_name,
                'subject': email.subject,
                'body': email.body
            }

        if data is None:
            raise APIException('DEFAULT_EMAIL_PROVIDER must be either spendgrid or snailgun')
        else:
            response = self.send_email(data)

            # sending email process on spendgrid is synchronous, so it must have been sent out
            # successfully if it has the response back. Just mark the status as SENT
            if DEFAULT_EMAIL_PROVIDER == 'spendgrid':
                email.status = Status.SENT.value
            # sending email process on snailgun is asynchronous, so the status could be FAILED
            # or QUEUED when it gets response back. Mark this status and save the email into database
            else:
                email.status = str(response['status']).upper()
                email.email_id = response['id']

        email.save()
        return email

    # This method handle the POST request to snailgun or spendgrid to send the email
    def send_email(self, data):
        url = API_KEYS[f'{DEFAULT_EMAIL_PROVIDER}_url']
        api_key = API_KEYS[f'{DEFAULT_EMAIL_PROVIDER}_api_key']
        request_headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': api_key
        }

        try:
            response = requests.post(url, json=data, headers=request_headers)

            if response.status_code != 201 and response.status_code != 200:
                msg = f'Error in posting the request (status code: {response.status_code})'
                print(msg)
                raise APIException(msg)
            else:
                response = response.json()
                return response
        except Exception as ex:
            print(ex)
            raise ex

    #This method validate if the email address is correct or not
    @staticmethod
    def validate_email(email_address):
        reg_expr = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.match(reg_expr, email_address)

# Create email -- POST BASE_URL + emails/
# Get a single email:
#       1) GET BASE_URL + emails/?id={email's primary key in the app_email table}
#       2) GET BASE_URL + emails/?email_id={snailgun's returned email id in the response. This only applies to snailgun)
class EmailList(generics.ListCreateAPIView):
    serializer_class = EmailListSerializer

    def get_queryset(self):
        id = self.request.query_params.get('id', None)
        email_id = self.request.query_params.get('email_id', None)

        if email_id is None and id is None:
            q_set = Email.objects.all()
        else:
            if id is not None:
                q_set = Email.objects.filter(pk=id)
            else:
                q_set = Email.objects.filter(email_id=email_id)

            # If this email is snailgun email, need to check if this email is already sent out.
            # If not, need to send the request to snailgun to retrieve its most recent status
            # and save it back to the database
            if DEFAULT_EMAIL_PROVIDER == 'snailgun' and q_set is not None and len(q_set) > 0:
                email = q_set[0]
                email_id = email.email_id
                status = email.status.upper()

                if status == Status.QUEUED.value:
                    url = API_KEYS['snailgun_url'] + '/' + email_id
                    api_key = API_KEYS[f'{DEFAULT_EMAIL_PROVIDER}_api_key']
                    request_headers = {
                        'Content-Type': 'application/json',
                        'X-Api-Key': api_key
                    }
                    response = requests.get(url, headers=request_headers)
                    if response.status_code == 200:
                        response = response.json()
                        email.status = str(response['status']).upper()
                        email.save()

        return q_set

