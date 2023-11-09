from django import forms

class PreguntaForm(forms.Form):
    pregunta = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={
                                    # 'class'         : 'chat-messages',
                                    "id"            : 'user-input',
                                    'placeholder'   : 'Escribe tu pregunta aquí...',
                                    "type"          : 'text',
                                    }))