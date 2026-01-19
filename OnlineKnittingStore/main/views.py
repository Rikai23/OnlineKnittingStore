from django.http import HttpResponse
from django.shortcuts import render

from goods.models import Categories

def index(request):
    """Обрабатывает запросы на главную страницу"""

    # Список текстов, которые будут исп. на главной странице
    texts = [
        {
            "title": "онлайн магазин вязаных изделий",
            "desc": "Каждое изделие создано с теплом и вниманием к деталям. Выберите уникальные вещи, которые подарят уют и подчеркнут вашу индивидуальность."
        }
    ]

    context = {
        'title': "Вязаные изделия",
        'texts': texts,
    }
    return render(request, 'main/index.html', context)

