from django import forms

class UploadForm(forms.Form):
    _name = forms.CharField(label='Username', max_length=100)
    _token = forms.CharField(label='Token', max_length=48)
    _path = forms.CharField(label='Path')
    _file = forms.FileField()
