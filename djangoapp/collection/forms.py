from django import forms
from collection.models import Post

MODEL_CHOICES= [
    ('knn', 'K Nearest Neighbor'),
    ('second', 'Second Model'),
    ('third', 'Third Model'),
    ('fourt', 'Fourth Model' ),
]


class HomeForm(forms.ModelForm):
    post = forms.CharField(widget=forms.TextInput(
        attrs={
            'id': 'formGroupExampleInput',
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Enter Product ID...',
        }
    ))

    model_type = forms.CharField(label="Please select model type", widget=forms.RadioSelect(choices=MODEL_CHOICES))


    class Meta:
        model = Post
        fields = ('post',)
