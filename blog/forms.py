from django.forms import ModelForm, DateInput, EmailField, TextInput, Form, DateTimeField
from .models import Event

class DateForm(Form):
    date = DateTimeField(input_formats=['%d/%m/%Y %H:%M'])

class ContactForm(ModelForm):
    from_email = EmailField()
    content = TextInput()
    class Meta:
        fields = ['content', 'from_email']


class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ["author",]
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
