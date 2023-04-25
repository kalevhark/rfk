from django import forms


class AnnetusForm(forms.Form):
    eesnimi = forms.CharField(label="Eesnimi", max_length=50)
    perenimi = forms.CharField(label="Perenimi", max_length=50)
