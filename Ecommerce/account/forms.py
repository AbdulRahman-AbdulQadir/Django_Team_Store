from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from Products.models import Profile
from django.contrib.auth import get_user_model

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

User = get_user_model()

TAILWIND_INPUT_CLASSES = 'w-full p-3 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500'
class UserProfileForm(UserChangeForm):
    password = None

    # -- User fields (as before) --
    full_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': TAILWIND_INPUT_CLASSES,
            'placeholder': 'Your Full Name'
        }),
        label='Full Name'
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

    # -- Profile fields (new) --
    phone    = forms.CharField(max_length=20, required=False,
                    widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES}),
                    label='Phone Number')
    address1 = forms.CharField(max_length=200, required=False,
                    widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES}),
                    label='Address Line 1')
    address2 = forms.CharField(max_length=200, required=False,
                    widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES}),
                    label='Address Line 2')
    city     = forms.CharField(max_length=200, required=False,
                    widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES}),
                    label='City')
    state    = forms.CharField(max_length=200, required=False,
                    widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES}),
                    label='State/Province')
    zipcode  = forms.CharField(max_length=20, required=False,
                    widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES}),
                    label='ZIP/Postal Code')
    country  = forms.CharField(max_length=200, required=False,
                    widget=forms.TextInput(attrs={'class': TAILWIND_INPUT_CLASSES}),
                    label='Country')

    class Meta:
        model = User
        fields = ('username', 'full_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': TAILWIND_INPUT_CLASSES,
                'placeholder': 'Username'
            }),
        }
        labels = {
            'username': 'Username',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 1) Populate full_name from first_name/last_name
        if self.instance and self.instance.pk:
            self.fields['full_name'].initial = f"{self.instance.first_name} {self.instance.last_name}".strip()
        # 2) Populate profile‐side fields
        try:
            profile = self.instance.profile
        except Profile.DoesNotExist:
            profile = None

        if profile:
            for fld in ('phone','address1','address2','city','state','zipcode','country'):
                self.fields[fld].initial = getattr(profile, fld, '')

        # 3) Tidy up labels & attrs exactly as before
        for name, field in self.fields.items():
            field.label_suffix = ''
            if hasattr(field.widget, 'attrs'):
                # leave Tailwind classes in place
                pass
            # optional HTMX attributes you had:
            field.widget.attrs['hx-target'] = 'this'
            field.widget.attrs['hx-swap']   = 'outerHTML'

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name','').strip()
        if not full_name:
            # clear both names
            self.cleaned_data['first_name'] = ''
            self.cleaned_data['last_name']  = ''
        return full_name

    def save(self, commit=True):
        # 1) Save the User bits
        user = super().save(commit=False)

        # split and set names
        full_name = self.cleaned_data.get('full_name','').strip()
        if full_name:
            parts = full_name.split(' ',1)
            user.first_name = parts[0]
            user.last_name  = parts[1] if len(parts)>1 else ''
        else:
            user.first_name = user.last_name = ''

        user.email = self.cleaned_data.get('email','')
        if commit:
            user.save()

        # 2) Save the Profile bits
        profile, created = Profile.objects.get_or_create(user=user)
        for fld in ('phone','address1','address2','city','state','zipcode','country'):
            setattr(profile, fld, self.cleaned_data.get(fld,'').strip())
        if commit:
            profile.save()

        return user

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
    