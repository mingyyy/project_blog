from django.forms import ModelForm, DateInput, EmailField, TextInput, Form, CharField, Textarea
from .models import Event


class ContactForm(Form):
    from_email = EmailField(required=True)
    subject = CharField(max_length=50,required=True, help_text='50 characters max.')
    content = CharField(widget=Textarea(attrs={'placeholder': 'Enter your message here.'}),
                        required=True)


class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ["author",]
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local', 'class': 'datetimepicker'},
                                    format='%Y/%m/%d %H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local','class': 'datetimepicker'},
                                  format='%Y/%m/%d %H:%M'),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ('%Y/%m/%d %H:%M',)
        self.fields['end_time'].input_formats = ('%Y/%m/%d %H:%M',)


class EventDeleteForm(Form):
    confirm = CharField(max_length=7, widget=Textarea(attrs={'placeholder': 'confirm', 'rows': 1, 'cols': 4}),
                        required=False, label='')



