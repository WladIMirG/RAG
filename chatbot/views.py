from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .forms import PreguntaForm
import maritalk

import os
from dataclasses import dataclass
from typing import List, Tuple


def chatbot_view(request):
    global messages
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        user_message = {"role": "user", "content": user_input}
        messages.append(user_message)
        response = obtener_respuesta_gpt(messages)
        chatbot_message = {"role": "assistant", "content": response}
        messages.append(chatbot_message)
        print(messages)
    else:
        response = "¡Hola! Soy tu chatbot para el Vestibular da Unicamp 2024. ¿En qué puedo ayudarte?"
    return render(request, 'chat.html', {'response': response, 'messages': messages})

def obter_resposta_maritalk(user_input):
    # Llama a la API de Maritalk para obtener una respuesta
    # Utiliza la biblioteca maritalk y tu clave de API
    model = maritalk.MariTalk(
        key= os.getenv("MARITALK_API_KEY"),
        )
    
    response = model.generate(
        messages,
        do_sample=True,
        max_tokens=200,
        temperature=0.7,
        top_p=0.95)
    
    return response

def obtener_respuesta_gpt(user_input):
    # Llama a la API de GPT-3.5 Turbo para obtener una respuesta
    # Utiliza la biblioteca openai y tu clave de API
    
    client = OpenAI(
        api_key= os.getenv("OPENAI_API_KEY"),
    )
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "Vocé é um chatbot para o Vestibular da Unicamp 2024."},
    ] + user_input,
    )
    return response.choices[0].message
