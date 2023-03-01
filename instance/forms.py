from django import forms

class UpdateForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    entry_time = forms.CharField(max_length=100, required=False)
    exit_time = forms.CharField(max_length=100, required=False)
    call_stoploss = forms.CharField(max_length=100, required=False)
    put_stoploss = forms.CharField(max_length=100, required=False)
    stop_loss = forms.CharField(max_length=100, required=False)
    moneyness1 = forms.CharField(max_length=100, required=False)
