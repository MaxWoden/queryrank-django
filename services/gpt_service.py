import openai
from django.conf import settings

class YandexGPTService:
    def __init__(self):
        self.api_key = settings.YANDEX_GPT_API_KEY
        self.folder_id = settings.YANDEX_GPT_FOLDER_ID
        self.model = settings.YANDEX_GPT_MODEL
        
        # Инициализация клиента
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url="https://ai.api.cloud.yandex.net/v1",
            project=self.folder_id
        )
    
    def generate_response(self, prompt, temperature=0.7, max_tokens=500):
        """Генерация ответа от YandexGPT"""
        try:
            response = self.client.responses.create(
                model=f"gpt://{self.folder_id}/{self.model}",
                temperature=temperature,
                instructions="Ты полезный AI-ассистент интернет-магазина QueryRank",
                input=prompt,
                max_output_tokens=max_tokens
            )
            return response.output_text
        except Exception as e:
            return f"Ошибка API: {str(e)}"
    
    def answer_question(self, question):
        """Ответ на вопрос пользователя"""
        prompt = f"Ты - AI-консультант интернет-магазина QueryRank. Отвечай вежливо и полезно. Вопрос: {question}"
        return self.generate_response(prompt, temperature=0.5)
    
    def generate_product_description(self, product_name, features=None):
        """Генерация описания товара"""
        prompt = f"Напиши привлекательное описание товара для интернет-магазина: {product_name}"
        if features:
            prompt += f" Характеристики: {features}"
        return self.generate_response(prompt, temperature=0.8)