from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
from django.db.models import Sum
from django.dispatch import receiver 
from cars.models import Car, CarInventory
from openai_api.client import get_car_ai_bio

def car_inventory_update():
    cars_count = Car.objects.all().count() #Paga todos objtos da tabela Car e soma eles
    #aggregate add campos na minha Query nesse caso 'SUM'
    cars_value = Car.objects.aggregate(
        total_value = Sum('value') #campo value do DB
     #É necessario colar ['total_value'] pq aggregate esta retornando um dicionario chave e valor para ter acesso 
     # ao valor usar essa sintaxe  (['total_value'])
    )['total_value']
    CarInventory.objects.create( #Para cada novo registro  tabala CarInventory e atualizada!
        cars_count=cars_count,
        cars_value = cars_value
    )

@receiver(pre_save, sender=Car)
def car_pre_save(sender, instance, **kwargs):
    if not instance.bio:
        instance.bio = 'Sem Alteração'
        '''Aqui API Opne
        ai_bio = get_car_ai_bio(
        instance.model, instance.brand, instance.model_year)
        instance.bio = ai_bio '''


@receiver(pre_delete, sender=Car)
def car_pre_delete(sender, instance, **kwargs):
    print("### PRE DELETE ###")

@receiver(post_save, sender=Car)
def car_post_save(sender, instance, **kwargs):
    car_inventory_update()   

@receiver(post_delete, sender=Car)
def car_post_delete(sender, instance, **kwargs):
    car_inventory_update()    