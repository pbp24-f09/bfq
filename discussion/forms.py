from django.forms import ModelForm
from models import Discussion, Response

class DiscussionForm(ModelForm):
    class Meta:
        model = Discussion
        fields = ["user", "product", "comment"]

class ResponseForm(ModelForm):
    class Meta:
        model = Response
        fields = ["response"]