from langchain.retrievers import BM25Retriever
from openai import OpenAI
import maritalk
import pandas as pd
import os

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

class UVQuADChatBotRetriever:
    def __init__(self, data_path: str = "../data/processed/context_data.csv"):
        self.data = pd.read_csv(data_path)
        self.from_texts(self.data['context'].to_list())
        
    def from_texts(self, texts: list):
        self.retriever = BM25Retriever.from_texts(texts)
        
    def get_relevant_documents(self, question: str, n_docs: int = 1):
        result = self.retriever.get_relevant_documents(question)
        return result

class GPT3ChatBot:
    def __init__(self, model: str = "gpt-3.5-turbo",
                api_key: str = os.getenv("OPENAI_API_KEY"),
                retriever_data_path: str = "../data/processed/context_data.csv"):
        self.model = model
        self.agent = OpenAI(
            api_key= api_key,
        )
        self.retriever = UVQuADChatBotRetriever(retriever_data_path)
        self.conv = ConvHistory()
        self.conv.set_system_message("Vocé é um chatbot para o Vestibular da Unicamp 2024.")
        
    def retriever_set_message(self, question: str):
        context = self.retriever_get_context(question)
        user_message = f"Com base no contexto: {context}, responda a pergunta: {question}. Resposta:"
        self.conv.append_message("user", user_message)
        # return context['context']
    
    def retriever_get_context(self, question: str):
        relevant_documents = self.retriever.get_relevant_documents(question)
        return relevant_documents
    
    def get_answer_from_conversation(self, conversation: list):
        return self.get_answer(conversation)
    
    def get_answer_from_gpt3(self, question: str):
        self.retriever_set_message(question)
        response = self.agent.chat.completions.create(
            model=self.model,
            messages=self.conv.to_openai_api_messages(),
            max_tokens=100,
        )
        self.conv.append_message("assistant", response.choices[0].message.content)
        return response.choices[0].message.content


class MariTalkConvHistory(ConvHistory):
    def __init__(self):
        super().__init__()
    
    def to_maritalk_api_messages(self):
        """Convert the conversation to OpenAI chat completion format."""
        ret = [{"role": "assistant", "content": self.system_message}]
        for i, (_, msg) in enumerate(self.messages[self.offset :]):
            if i % 2 == 0:
                ret.append({"role": "user", "content": msg})
            else:
                if msg is not None:
                    ret.append({"role": "assistant", "content": msg})
        return ret

class MariTalkChatBot:
    
    def __init__(self,
                api_key: str = os.getenv("MARITALK_API_KEY"),
                retriever_data_path: str = "../data/processed/context_data.csv"):
        
        self.agent = maritalk.MariTalk(key=api_key)
        self.retriever = UVQuADChatBotRetriever(retriever_data_path)
        self.conv = MariTalkConvHistory()
        self.conv.set_system_message("Eu sou um chatbot para o Vestibular da Unicamp 2024.")
        
    def retriever_set_message(self, question: str):
        context = self.retriever_get_context(question)
        user_message = f"""Com base no contexto: "{context.page_content}", responda a pergunta: "{question}". Resposta:"""
        self.conv.append_message("user", user_message)
        # return context['context']
    
    def retriever_get_context(self, question: str):
        relevant_documents = self.retriever.get_relevant_documents(question)
        return relevant_documents[0]
    
    def get_answer_from_conversation(self, conversation: list):
        return self.get_answer(conversation)
    
    def get_answer_from_maritalk(self, question: str):
        self.retriever_set_message(question)
        messages = self.conv.to_maritalk_api_messages()
        # print(f"Input Messages: {messages}\n")
        try:
            response = self.agent.generate(
                messages,
                do_sample=True,
                max_tokens=100,
                temperature=0.7,
                top_p=0.95)
            self.conv.append_message("assistant", response)
            return response
        except Exception as e:
            return {"Erro": e}
        