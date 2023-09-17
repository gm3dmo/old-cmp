
from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(
                            label='Surname to search for:',
                            widget=forms.TextInput(attrs={'size': 32})
    )

class anForm(forms.Form):
    query = forms.CharField(
                            label='Army Number to check:',
                            widget=forms.TextInput(attrs={'size': 32})
    )
