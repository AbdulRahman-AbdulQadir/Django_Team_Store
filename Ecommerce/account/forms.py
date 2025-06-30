from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User


class ChangePasswordForm(SetPasswordForm):
    # SetPasswordForm already provides new_password1 and new_password2 fields.
    # We just need to apply the Tailwind classes to them if we want to
    # maintain consistent styling with your SignUpForm.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Tailwind classes to the password fields
        self.fields['new_password1'].widget.attrs.update({
            'class': TAILWIND_INPUT_CLASSES,
            'placeholder': '••••••••'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': TAILWIND_INPUT_CLASSES,
            'placeholder': '••••••••'
        })



TAILWIND_INPUT_CLASSES = 'w-full p-3 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500 text-gray-800 placeholder-gray-400'
TAILWIND_BUTTON_CLASSES = 'bg-indigo-600 text-white py-3 px-6 rounded-full text-lg font-semibold hover:bg-indigo-700 transition-colors duration-200 shadow-md transform hover:scale-105'
TAILWIND_LABEL_CLASSES = 'block text-sm font-medium text-gray-700 mb-1'
# Continue in forms.py

class UserProfileForm(UserChangeForm):
    password = None
    full_name = forms.CharField(
        max_length=150,
        required=False, # Make it not strictly required if you want to allow empty first/last names
        widget=forms.TextInput(attrs={
            'class': TAILWIND_INPUT_CLASSES,
            'placeholder': 'Your Full Name'
        }),
        label='Full Name' # Custom label
    )
    email = forms.EmailField(
        max_length=254,
        required=False,
        widget=forms.EmailInput(attrs={
            'class': TAILWIND_INPUT_CLASSES,
            'placeholder': 'you@example.com'
        }),
        label='Email Address'
    )
    # You might want to include other fields from the User model or custom fields.
    # For example, if you have a custom User model with a 'phone_number' field:
    # phone_number = forms.CharField(
    #     max_length=20,
    #     required=False,
    #     widget=forms.TextInput(attrs={
    #         'class': TAILWIND_INPUT_CLASSES,
    #         'placeholder': '+1 (123) 456-7890'
    #     }),
    #     label='Phone Number'
    # )

    class Meta:
        model = User
        # Exclude password fields as UserChangeForm handles password changes separately
        # You'll likely want to create a separate form for password changes.
        fields = ('username', 'full_name', 'email') # Add other fields you want to allow editing here

        widgets = {
            'username': forms.TextInput(attrs={
                'class': TAILWIND_INPUT_CLASSES,
                'placeholder': 'Username'
            }),
            # 'first_name': forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES}),
            # 'last_name': forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES}),
        }
        labels = {
            'username': 'Username',
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize the 'full_name' field from existing first_name and last_name
        if self.instance and self.instance.pk:
            self.fields['full_name'].initial = f"{self.instance.first_name} {self.instance.last_name}".strip()
        
        # Apply styling to existing UserChangeForm fields if they are included in 'fields'
        for field_name in self.fields:
            if field_name not in ['full_name', 'email']: # exclude custom fields already handled
                # Check if the field exists and is a widget that supports attrs
                if hasattr(self.fields[field_name].widget, 'attrs'):
                    current_classes = self.fields[field_name].widget.attrs.get('class', '')
                    if TAILWIND_INPUT_CLASSES not in current_classes:
                        self.fields[field_name].widget.attrs['class'] = f"{TAILWIND_INPUT_CLASSES} {current_classes}".strip()
            
            # Apply labels explicitly for better styling
            self.fields[field_name].label_suffix = '' # Remove default colon
            self.fields[field_name].widget.attrs['hx-target'] = 'this' # Example for htmx, can be removed
            self.fields[field_name].widget.attrs['hx-swap'] = 'outerHTML' # Example for htmx, can be removed

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not full_name:
            # If full_name is optional and empty, clear first/last name
            self.cleaned_data['first_name'] = ''
            self.cleaned_data['last_name'] = ''
        return full_name

    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = self.cleaned_data.get('full_name', '').strip()

        if full_name:
            names = full_name.split(' ', 1)
            user.first_name = names[0]
            if len(names) > 1:
                user.last_name = names[1]
            else:
                user.last_name = '' # Clear last name if only one name is provided
        else:
            user.first_name = ''
            user.last_name = ''

        user.email = self.cleaned_data.get('email') # Ensure email is saved from the form

        if commit:
            user.save()
        return user

TAILWIND_INPUT_CLASSES = 'w-full p-3 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500'

class SignUpForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': TAILWIND_INPUT_CLASSES,
            'placeholder': 'John Doe'
        })
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': TAILWIND_INPUT_CLASSES,
            'placeholder': 'you@example.com'
        })
    )
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': TAILWIND_INPUT_CLASSES,
            'placeholder': '••••••••'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': TAILWIND_INPUT_CLASSES,
            'placeholder': '••••••••'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': TAILWIND_INPUT_CLASSES,
                'placeholder': 'Username'
            }),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = self.cleaned_data.get('full_name')
        names = full_name.strip().split(' ', 1)
        user.first_name = names[0]
        if len(names) > 1:
            user.last_name = names[1]
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user
    