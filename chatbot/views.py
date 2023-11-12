from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .forms import PreguntaForm
from .src.utils import GPT3ChatBot, MariTalkChatBot

import os
from dataclasses import dataclass
from typing import List, Tuple

from .apps import ChatbotConfig

# chatbot = MariTalkChatBot(
#             retriever_data_path="data/processed/context_data.csv")

chatbot = GPT3ChatBot(
            retriever_data_path="data/processed/context_data.csv")

mesg = []

def chatbot_view(request):
    global mesg
    
    print(f"chatbot: {chatbot}")
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        
        #### Uncomment the next tow lines to use MariTalk
        # response = chatbot.get_answer_from_maritalk(user_input)
        # mesg = chatbot.conv.to_maritalk_api_messages(chatbot.conv.input_messages)
        
        #### Comment the next tow lines if you want to use MariTalk
        response = chatbot.get_answer_from_gpt3(user_input)
        mesg = chatbot.conv.to_openai_api_messages(chatbot.conv.input_messages)
        
        return render(request, 'chat.html', {'response': response,
                                            'user_input': user_input,
                                            "messages": mesg,
                                            })
    else:
        response = "¡Hola! Soy tu chatbot para el Vestibular da Unicamp 2024. ¿En qué puedo ayudarte?"
    return render(request, 'chat.html', {'response': response,
                                        })