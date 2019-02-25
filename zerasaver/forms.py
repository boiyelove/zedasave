from django import forms
from .models import ZeraPlan, UserSavingsPlan



class ZeraPlanForm(forms.ModelForm):
	class Meta:
		model = ZeraPlan
		fields = '__all__'


class UserSavingsForm(forms.ModelForm):

	class Meta:
		model = UserSavingsPlan
		exclude = ['user', 'plan', 'active_sub', 'has_auth']



	def clean_frequency(self):
		freq = self.cleaned_data.get('frequency')
		if (freq > 3) or (freq < 1):
			raise forms.ValidationError('Invalid frequency value')
		return freq  


	def clean_day_of_month(self):
		dateday = self.cleaned_data.get('day_of_month')
		if dateday > 28 or dateday < 1:
			raise forms.ValidationError("Invalid Day of the month")
		return dateday



class QuickSaveForm(forms.Form):
	amount = forms.IntegerField()

	def clean_amount(self):
		amount = self.cleaned_data.get('amount')
		if amount >= 100:
			return amount
		raise forms.ValidationError('Minimum deposit amount is 100')