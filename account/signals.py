from django.db.models.signals import post_save,pre_delete
from django.contrib.auth.models import User#bri istifadeci ucun yaradilcaga prfile ona gore User getirmek sertdir
from django.dispatch import  receiver
from.models import Profile,RelationShip#?Profile modelinden profil yaranacag avtomatik

@receiver(post_save,sender=User)
def post_save_create_profile(sender,instance,created,**kwargs):
    print('Sender',sender)#Useri gosterir class olmagini
    print('Instance', instance)#Burda ise User vasitesile yaradilan istifadecinin adini gosterir
    if created:
        Profile.objects.create(user=instance)#User modelini User bildriri,yeni User modeli vasitesile yaratdigimiz acccount Profile modelini yaratmaga komek edecek bele deyim

@receiver(post_save,sender=RelationShip)#yeni 
def post_save_add_to_frinends(sender,instance,created,**kwargs):
    gonderen = instance.sender#Bunlar icinde Profile modelini tuturlar onsuz Foregeink Key vasitesile.burdaki instance = relationshipdir
    qebul = instance.reciver
    
    if instance.status == 'Accepted':
        gonderen.friends.add(qebul.user)
        qebul.friends.add(gonderen.user)#Yeni biri gonderir digeride qebul ederek dostluguna dusur bele deyim
        gonderen.save()
        qebul.save()
        
@receiver(pre_delete,sender=RelationShip)
def post_delete_remove_friends(sender,instance,**kwargs):
    gonderen_istifadeci = instance.sender
    qebul_istifadeci = instance.reciver
    
    gonderen_istifadeci.friends.remove(qebul_istifadeci.user)
    qebul_istifadeci.friends.remove(gonderen_istifadeci.user)
    
    gonderen_istifadeci.save()
    qebul_istifadeci.save()
    