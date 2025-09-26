from django.shortcuts import render
#Модуль httpResponse отвечает за вывод одиночных сообщений
from django.http import HttpResponse
from datetime import datetime
import random
# Create your views here.


def first_time_view(request):
    if request.method == 'GET':
        time_str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        return HttpResponse(time_str)
    
def random_nambers_list(request):
    if request.method == 'GET':
        number = random.randint(1, 6)
        if number == 1:
            result = 'Выпало случайное число 1'
        elif number == 2:
            result = 'Выпало случайное число 2'
        elif number == 3:
            result = 'Выпало случайное число 3'
        elif number == 4:
            result = 'Выпало случайное число 4'
        elif number == 5:
            result = 'Выпало случайное число 5'
        else:
            result = 'Выпало случайное число 10'
        return HttpResponse(result)

def show_biography(request):
    if request.method == 'GET':
        return HttpResponse(
            """
            Привет меня зовут Амантур. Кратко раскажу о себе, мне  17 лет.
            А также я учусь в школе на данный момент. Увлекаюсь бксом и баскетболом.
            На этом все. Пока!!
            
            """                
                            )
        
