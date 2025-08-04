from django import forms
from .models import ShippingAddress

TAILWIND_INPUT_CLASSES = 'w-full p-3 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500'
TAILWIND_INPUT_CLASSES = "w-full p-3 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(max_length=250, required=True,widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES, 'placeholder': 'ex, john'}),label='Full Name')
    shipping_email = forms.CharField(max_length=250, required=True,widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES, 'placeholder': 'ex, john@gmail.com'}),label='Email Address')
    shipping_address1 = forms.CharField(max_length=250, required=True,widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES, 'placeholder': 'ex, 123 Main St'}),label='Address1')
    shipping_address2 = forms.CharField(max_length=250, required=False,widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES, 'placeholder': 'ex, St small'}),label='Address2')
    shipping_city = forms.CharField(max_length=250, required=True,widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES, 'placeholder': 'ex, Anytown'}),label='City')
    shipping_state = forms.CharField(max_length=250, required=False,widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES, 'placeholder': 'ex, DKI'}),label='State')
    shipping_zipcode = forms.CharField(max_length=250, required=False,widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES, 'placeholder': 'ex, 9383'}),label='Zipcode')
    shipping_country = forms.CharField(max_length=50, required=True,widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES, 'placeholder': 'ex, Indonesia, Japan...'}),label='Country')

    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_state', 'shipping_zipcode', 'shipping_country',]
        exclude = ['user',]

class PaymentForm(forms.Form):
    card_name = forms.CharField(max_length=250, required=True, widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES, 'placeholder': 'Name On Card'}), label='Name on Card')
    card_number = forms.CharField(max_length=250, required=True, widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES, 'placeholder': 'XXXX XXXX XXXX XXXX'}), label='Card Number') # Updated placeholder
    card_exp_date = forms.CharField(max_length=250, required=True, widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES, 'placeholder': 'MM/YY'}), label='Expiry Date (MM/YY)') # Updated placeholder
    card_cvv_number = forms.CharField(max_length=250, required=True, widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES, 'placeholder': '123'}), label='CVV') # Updated placeholder
    card_address1 = forms.CharField(max_length=250, required=True, widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES, 'placeholder': 'Billing Address 1'}), label='Address 1')
    card_address2 = forms.CharField(max_length=250, required=False, widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES, 'placeholder': 'Billing Address 2'}), label='Address 2')
    card_city = forms.CharField(max_length=250, required=True, widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES, 'placeholder': 'Billing City'}), label='City')
    card_state = forms.CharField(max_length=250, required=True, widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES, 'placeholder': 'Billing State'}), label='State')
    card_zipcode = forms.CharField(max_length=250, required=True, widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES, 'placeholder': 'Billing Zipcode'}), label='Zipcode')
    card_country = forms.CharField(max_length=250, required=True, widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES, 'placeholder': 'Country'}), label='Country')