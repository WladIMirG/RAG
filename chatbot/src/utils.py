from langchain.retrievers import BM25Retriever
import pandas as pd
import os
import openai
from openai import OpenAI


class UVQuADChatBotRetriever:
    def __init__(self):
        self.data = pd.read_csv('./data/processed/contextos.csv')
        self.from_texts(self.data['context'].to_list())
        
    def from_texts(self, texts: list):
        self.retriever = BM25Retriever.from_texts(texts)
        
    def get_relevant_documents(self, question: str, n_docs: int = 1):
        result = self.retriever.get_relevant_documents(question)
        return result[:n_docs]

class ConvHistory:
    def __init__(self):
        self.messages = []
        self.offset = 0
        self.system_message = "¡Hola! Soy tu chatbot para el Vestibular da Unicamp 2024. ¿En qué puedo ayudarte?"
        
    def set_system_message(self, system_message: str):
        """Set the system message."""
        self.system_message = system_message

    def append_message(self, role: str, message: str):
        """Append a new message."""
        self.messages.append([role, message])
    
    def to_openai_api_messages(self):
        """Convert the conversation to OpenAI chat completion format."""
        ret = [{"role": "system", "content": self.system_message}]

        for i, (_, msg) in enumerate(self.messages[self.offset :]):
            if i % 2 == 0:
                ret.append({"role": "user", "content": msg})
            else:
                if msg is not None:
                    ret.append({"role": "assistant", "content": msg})
        return ret

class GPT3ChatBot:
    def __init__(self):
        self.model = "gpt-3.5-turbo"
        self.agent = OpenAI(
            api_key= os.getenv("OPENAI_API_KEY"),
        )
        self.retriever = UVQuADChatBotRetriever()
        
    def get_answer(self, question: str):
        relevant_documents = self.retriever.get_relevant_documents(question)
        return relevant_documents[0]
    
    def get_answer_from_user_input(self, user_input: str):
        return self.get_answer(user_input)
    
    def get_answer_from_conversation(self, conversation: list):
        return self.get_answer(conversation)
    
    def get_answer_from_gpt3(self, question: str):
        response = self.agent.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Vocé é um chatbot para o Vestibular da Unicamp 2024."},
            ] + question,
        )
        return response.choices[0].message.content
    