from django import forms
from collection.models import Post

class HomeForm(forms.ModelForm):
    post = forms.CharField(widget=forms.TextInput(
        attrs={
            'id': 'formGroupExampleInput',
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Enter Product ID...',
        }
    ))


    class Meta:
        model = Post
        fields = ('post',)
