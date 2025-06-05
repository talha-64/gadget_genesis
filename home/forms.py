from django import forms
from . models import contactUs

class contactForm(forms.ModelForm):
    class Meta:
        model = contactUs
        fields = ['name', 'email', 'phone_number', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-md bg-[#81DEB4] placeholder-gray-700',
                'placeholder': 'Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-md bg-[#81DEB4] placeholder-gray-700',
                'placeholder': 'Email',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-md bg-[#81DEB4] placeholder-gray-700',
                'placeholder': 'Phone number',
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-md bg-[#81DEB4] placeholder-gray-700',
                'placeholder': 'Message',
                'rows': 5
            }),
        }
