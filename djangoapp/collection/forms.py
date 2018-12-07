from django import forms
from django.forms import widgets
from collection.models import Post

MODEL_CHOICES= [
    ('knn', 'K Nearest Neighbor'),
    ('svd', 'SVD'),
    ('third', 'Third Model'),
    ('fourth', 'Fourth Model' ),
]

class HomeForm(forms.ModelForm):
    post = forms.CharField(widget=forms.TextInput(
        attrs={
            'id': 'formGroupExampleInput',
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Enter Book Title...',
        }
    ))

    model_type = forms.ChoiceField(required = True, choices=MODEL_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Post
        fields = ('post', 'model_type')
