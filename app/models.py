from django.db import models


# Model definition for Email
class Email(models.Model):

    to_email = models.CharField(null=False, blank=False, max_length=200)
    to_name = models.CharField(null=False, blank=False, max_length=100)
    from_email = models.CharField(null=False, blank=False, max_length=200)
    from_name = models.CharField(null=False, blank=False, max_length=100)
    subject = models.CharField(null=False, blank=False, max_length=500)
    body = models.TextField(null=False, blank=False)
    status = models.CharField(null=True, blank=True, max_length=10)
    email_id = models.CharField(null=True, blank=True, max_length=100)  # only snailgun has value for this field
    sent_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
