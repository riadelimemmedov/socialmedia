
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import  slugify
from django.db.models import  Q
from django.shortcuts import render,HttpResponse,get_object_or_404,redirect,reverse
from ckeditor.fields import RichTextField

# Create your models here.



class ProfileManager(models.Model):
##################################################################################################################    
    def get_all_to_invate(self,gonderen):#yeni kimlere gonderilib invate
        #Burdaki sender dostlugu gonderen istifadecidi
        profiles = Profile.objects.all().exclude(user=gonderen)#yeni dostlug atan adam ozune  yeniden dostlug atmasin,hemd eozunu gostermesin o sirada ona gore
        profile = Profile.objects.get(user=gonderen)
        qs = RelationShip.data.filter(Q(sender=profile)| Q(reciver=profile))
        
        accepted = set([])#cunki for dongusunde eyni deyerler gele biler ancag setler tekrarlanmir setlerde listeyye elave etmek ucun ise add acar sozunden istifade olunur
        
        for rel in qs:#qs den gelen her bir profil rel deyiskenine atilir
            if rel.status == 'Accepted':
                accepted.add(rel.reciver)
                accepted.add(rel.sender)
        # print(accepted)
        # print('****************************************')
        
        available = [profile for profile in profiles if profile not in accepted]#yeni burdaki kodda yeni hele istekk atilib geri donus yoxdur amma yeni dostlugu qebul elemeneyenler
        #print(available)
        return available#bu geri donen deyer viewsde istifade olunur
        

#############################################################################################################################################################################################################
    def get_all_profiles(self,me):#burda Prodile modeliden butun profilleri cekirik ve amma men ozumu cixartmaliyam ordan ogore gorede exclude ile ozumu cixardiram
        profiles = Profile.objects.all().exclude(user=me)#burdaki me views.py dan gelen request.user deyeri olacag
        return profiles#return olmasindaki sebeb gedib viewdeki funksiyalarin birinde bu funksiya adi verilerek cagiriacag ve me deyeri beraber olacag requests.user a


################################################################################################################################################################

#!Burdaki modelde Istifadeci profili yaradaciyig ve bir istifadeci profilinde neler olmalidir onlar qeyd oluncaga bu classda
class Profile(models.Model):
    CATEGORY= (
        ('Gen','Kisi'),
        ('Gen','Kadin'),
        ('Gen','Yeniyetme')
    )
        
    
    first_name = models.CharField(max_length=255,blank=False,verbose_name='Adi')
    last_name = models.CharField(max_length=255,blank=False,verbose_name='Soyad')
    user = models.OneToOneField(User,on_delete=models.CASCADE)#Burda onetoonefield yazilmasindaki sebeb yeni her istifadeciden 1 dene olsun yeni 1 dene profil 1 istifadecini temsil etsin basqa hec kim istifade ede bilmesin
    bio = RichTextField(blank=True)
    email = models.EmailField(max_length=255,blank=True,verbose_name='Email')
    country = models.CharField(max_length=255,blank=True,verbose_name='Olke')
    avatar = models.ImageField(default='users/amk.jpg',upload_to = 'users')
    friends = models.ManyToManyField(User,blank=True,related_name='dostlar',verbose_name='Dostlar')
    slug = models.SlugField(default='slug',editable=False)#editable=False yeni istifadeci terefinden deyismek olmasin
    gender = models.CharField(max_length=255,null=True,choices=CATEGORY,verbose_name='Cinsiyyet')#Burdaki choices kicik her yerde istifade olunmali olunan kategoriyalari adlandirmag ucun istifade olunur choicesden
    facebook_hesabi = models.URLField(max_length=255,blank=True)
    twitter_hesabi = models.URLField(max_length=255,blank=True)
    linkedin_hesabi = models.URLField(max_length=255,blank=True)#blank=True yeni qeyd etmesende olar pass kecsende olar hemin yeri 
    youtube_hesabi = models.URLField(max_length=255,blank=True)
    instaqram_hesabi = models.URLField(max_length=255,blank=True)
    updated = models.DateTimeField(auto_now=True)   
    created = models.DateTimeField(auto_now_add=True)
    oxudugu_yer = models.CharField(max_length=255,blank=True)
    ixtisas = models.CharField(max_length=255,blank=True)
    doguldugu_il = models.CharField(max_length=255,blank=False)
    yas = models.CharField(max_length=255,blank=False)
    yasadigi_yer = models.CharField(max_length=255,blank=True)
    islediyi_yer = models.CharField(max_length=255,blank=True)
    hesab = ProfileManager()
    
    def get_absolute_url(self):#bunu istifade etmeyi unutma yaxsi seydir
        return reverse("profile_detail", kwargs={"pk": self.pk})
    

    def get_friends(self):
        return self.friends.all()#yuxaridaki friends
    
    def get_friends_number(self):
        return self.friends.all().count()

    def post_count(self):
        return self.istifadeci.all().count()#Burdaki istifadeci related nameden gelir
    
    def postlar(self):
        return self.istifadeci.all()#Yeni post yazan butun istifadecileri cekirsen bura
    
    def likes_count(self):#elediyim likelar her like 1 dene like beraberdir like=1
        likes = self.like_set.all()
        total_liked = 0
        for item in likes:
            if item.value == 'Like':
                total_liked += 1
        return total_liked
    
    def get_likes_recived(self):#aldigim likelar postlara umumi sekilde
        posts = self.istifadeci.all()#yeni her hansi bir istifadeciden alirig like ona gore bu formada yaziildi
        total_liked = 0
        for item in posts:
            total_liked += item.liked.all().count()
        return total_liked

    
    def __str__(self):
        return f"{self.user.username}"
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(Profile,self).save(*args, **kwargs)
        
        
#!Indi ise istifadecilerin biri birine dostlug atib ve qebule elemelri ucun bir model yazag


class RelationShipManager(models.Manager):#models.Manager ile oz querylerimizi yaza bilirk model dosyasi icinde manager burdanda basa dusmek olarki yeni idare edirik
    def invatations_received(self,reciver):
        qs = RelationShip.data.filter(reciver = reciver,status ='Send')
        return qs
    
    
class RelationShip(models.Model):
    STATUS = (
        ('Send','Send'),
        ('Accepted','Accepted')
    )
    
    sender = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='sender')#Burda Profile medelini ForeignKey ile cekmeyimizdeki sebeb yeni bir istifadeci coxlu dostlug ata biler 1 profilnen yeni Profile modeli ile
    reciver = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='reciver')
    status =  models.CharField(max_length=255,choices=STATUS)#Yeni qebul eleyib dostlugu yoxsa qebul elemeyib
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    data = RelationShipManager()
    
    def __str__(self):
        return f"{self.sender}---{self.reciver}---{self.status}"
    
class Contact(models.Model):
    name = models.CharField(max_length=255,blank=False)
    email = models.EmailField(max_length=255,blank=False)
    message = models.TextField(blank=False)
    
    def __str__(self):
        return self.email