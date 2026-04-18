import requests
from django.conf import settings

class YandexGPTService:
    def __init__(self):
        self.api_key = settings.YANDEX_GPT_API_KEY
        self.folder_id = settings.YANDEX_GPT_FOLDER_ID
        self.model = "yandexgpt-lite"  # ЖЕСТКО
    
    def generate_response(self, prompt, temperature=0.7, max_tokens=500):
        """Генерация ответа от YandexGPT"""
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        
        headers = {
            "Authorization": f"Api-Key {self.api_key}",
            "Content-Type": "application/json"
        }
        
        body = {
            "modelUri": f"gpt://{self.folder_id}/{self.model}",
            "completionOptions": {
                "temperature": temperature,
                "maxTokens": max_tokens
            },
            "messages": [
                {
                    "role": "user",
                    "text": prompt
                }
            ]
        }
        
        try:
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()
            result = response.json()
            answer = result["result"]["alternatives"][0]["message"]["text"]
            return answer
        except Exception as e:
            return f"Ошибка API: {str(e)}"
    
    def answer_question(self, question):
        """Ответ на вопрос пользователя"""
        return self.generate_response(question, temperature=0.5)
    
    def generate_product_description(self, product_name, features=None):
        """Генерация описания товара"""
        prompt = f"Напиши привлекательное описание товара: {product_name}"
        if features:
            prompt += f" Характеристики: {features}"
        return self.generate_response(prompt, temperature=0.8)