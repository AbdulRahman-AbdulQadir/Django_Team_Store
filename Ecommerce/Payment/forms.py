from django import forms
from .models import ShippingAddress

TAILWIND_INPUT_CLASSES = 'w-full p-3 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500'
class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(max_length=250, required=True,widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES}),label='Full Name')
    shipping_email = forms.CharField(max_length=250, required=True,widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES}),label='Email Address')
    shipping_address1 = forms.CharField(max_length=250, required=True,widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES}),label='Address1')
    shipping_address2 = forms.CharField(max_length=250, required=True,widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES}),label='Address2')
    shipping_city = forms.CharField(max_length=250, required=True,widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES}),label='City')
    shipping_state = forms.CharField(max_length=250, required=False,widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES}),label='State')
    shipping_zipcode = forms.CharField(max_length=250, required=False,widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES}),label='Zipcode')
    shipping_country = forms.CharField(max_length=50, required=True,widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES}),label='Country')

    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_state', 'shipping_zipcode', 'shipping_country',]
        exclude = ['user',]