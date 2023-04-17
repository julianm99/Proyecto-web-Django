from django import forms
from ckeditor.widgets import CKEditorWidget

class DateImput(forms.DateInput):
    input_type = 'date'


class MensajesForm(forms.Form):
    mensaje = forms.CharField(widget=CKEditorWidget())