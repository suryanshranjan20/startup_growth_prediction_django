from django import forms

class StartupForm(forms.Form):
    country = forms.CharField(label='Country', max_length=100)
    industry = forms.CharField(label='Industry', max_length=100)
    investment_amount = forms.FloatField(label='Investment Amount')
    employee_count = forms.IntegerField(label='Employee Count')
    years_operating = forms.IntegerField(label='Years Operating')
