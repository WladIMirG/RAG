from django.apps import AppConfig


class ChatbotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chatbot'
    chatbot = None
    
    def ready(self):
        from .src.utils import GPT3ChatBot, MariTalkChatBot
        # self.chatbot = GPT3ChatBot(
        # retriever_data_path="data/processed/context_data.csv")
        
        # if not self.chatbot:
        print("Initializing chatbot...")
        self.chatbot = MariTalkChatBot(
            retriever_data_path="data/processed/context_data.csv")
        