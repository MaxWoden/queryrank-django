import requests
from django.conf import settings

class YandexMapsService:
    """Сервис для работы с Яндекс.Картами"""
    
    def __init__(self):
        self.api_key = settings.YANDEX_MAPS_API_KEY
    
    def geocode_address(self, address):
        """Преобразование адреса в координаты"""
        url = "https://geocode-maps.yandex.ru/1.x/"
        params = {
            'apikey': self.api_key,
            'geocode': address,
            'format': 'json'
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            try:
                coords = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
                lon, lat = coords.split()
                return {'lat': float(lat), 'lon': float(lon)}
            except (KeyError, IndexError):
                return None
        return None