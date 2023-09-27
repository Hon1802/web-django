from django import forms
from .models import Laptop, Account,Image
from django.contrib.auth.forms import UserCreationForm
from django.forms import formset_factory
from django.forms.models import inlineformset_factory

class LaptopForm(forms.ModelForm):
    class Meta:
        model = Laptop
        fields = '__all__'

   

        
    
        
        
class CustomerCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=20)
    address = forms.CharField(max_length=200)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    class Meta:
        model = Account
        fields = ('username', 'email', 'phone_number', 'address', 'password1', 'password2')
        labels = {
            'username': ('Username'),
            'email': ('Email'),
            'phone_number': ('Phone Number'),
            'address': ('Address'),
            'password1': ('Password'),
            'password2': ('Confirm Password'),
        }
        help_texts = {
            'username': None,
            'password1':None,
            'password2':None,
            
        }
        
class ImageForm(forms.ModelForm):
    image=forms.ImageField(label="Image",widget=forms.ClearableFileInput(attrs={"multiple":True}))
    class Meta:
        model = Image
        fields = ('image',)
        exclude = ['id']
        
