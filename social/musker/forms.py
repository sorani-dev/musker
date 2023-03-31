

from django import forms


class Form(forms.ModelForm):
    
    pass

class MeepForm(forms.ModelForm):
    
    body = forms.CharField(required=True,
                           widget=forms.widgets.Textarea
                            attrs={
                                'placeholder': 'Enter Your Musker Meep!',
                                'class': 'form-control',
                            },
                            label='',
                           )
    class Meta:
        model = Meep
        exclude = ('user',)

    
