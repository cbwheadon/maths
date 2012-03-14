from django import forms

class FractionForm(forms.Form):
    const = forms.IntegerField(required=False,min_value=-99,max_value=999,widget=forms.TextInput(attrs={'size':'3','maxlength':'3'}))
    num = forms.IntegerField(min_value=-99,max_value=999,widget=forms.TextInput(attrs={'size':'3','maxlength':'3'}))
    denom = forms.IntegerField(min_value=-99,max_value=999,widget=forms.TextInput(attrs={'size':'3','maxlength':'3'}))