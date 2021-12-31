from django.db import models
from django.core.validators import FileExtensionValidator #burdaki metod vasitesile seklin hansi novde oldugu deyilir tovsiye elemirem
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField
from django.http import JsonResponse
from account.models  import Profile

# Create your models here.

#!Categoriya Yaradag Postlari Kategoriyaya Bolmek Ucun
#?Categorylara bolmek ucun ForeignKey den istifade et yeni teke cox

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(editable=False)#yeni bizim terefden deyisilmesin
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug_alani = slugify(self.title)
        super(Category,self).save(*args, **kwargs)
        
    def category_count(self):
        return self.kategoriyalarimiz.all().count()
        

#!Indi ise Taglari yazag Taglara bolmek ucun postlari
#?Taglara bolmek ucun ManyToManyField den istifade edek yeni coxa cox

class Tag(models.Model):
    title =  models.CharField(max_length=255)
    slug = models.SlugField(editable=False)#editibke => yeni deyismek editible=False hemise yaz slugda
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug_alani = slugify(self.title)
        super(Tag,self).save(*args, **kwargs)
    
    def tag_sayi(self):#burda self yazilmalidir cunki Post modelinden deyisken adlari cekmey lazimdir yeni related_namedeki deyisken adini cekecikiyik
        return self.taglarimiz.all().count()


#!Post
class Post(models.Model):
    title = models.CharField(max_length=255,blank=False)
    content = RichTextField()
    resim = models.ImageField(upload_to = 'sekiller',blank=True,null=True)
    liked = models.ManyToManyField(Profile,related_name='beyenme',blank=True)#yeni sonsuz sayda postlara sonsuz like atila biler yeni 100 istifadeci mesleen 100 dene ayri posta like ede biler
    slug = models.SlugField(default='slug',editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='istifadeci')#hemise many to many ve ya foreign keylere related name at
    hit = models.PositiveIntegerField(default=0)#yeni en cok tiklanan postlar
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='kategoriyalarimiz' ,default=1,)    
    tag = models.ManyToManyField(Tag,related_name='taglarimiz')

    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post,self).save(*args, **kwargs)
    
    def num_likes(self):#like olunan postlar
        return self.beyenme.all().count()#Burdaki beyenme related_nameden gelir

    #Comment Count yazilacaga bura
    def num_comments(self):
        return self.comment_set.all().count()
    
    def count_post(self):
        return self.istifadeci.all().count()

    def koment_sayi(self):
        return self.yorum.all().count()

    
    class Meta:
        ordering = ['-created_at']
    
    
#!Comment
class Comment(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='adam')#Cunki bir istifadeci birden cox posta comment ata biler
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='yorum')#Birden cox posta yorum atila biler bir istifadeci terefinden
    body = models.TextField(max_length=255)
    update_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    sekil = models.ImageField(Profile,upload_to = 'users')
    
    def __str__(self):
        return self.body[:20]
    
    def count_comments(self):
        return self.yorum.objects.all().count() 
    
    def sekiller(self):
        return self.user.objects.all()
    
    class Meta:
        ordering = ['-created_date']


#!Like
class Like(models.Model):
    
    LIKE_CHOICES = (
        ('Like','Like'),
        ('Unlike','Unlike')
    )
    
    istifadeci = models.ForeignKey(Profile,on_delete=models.CASCADE)#Yeni bir istifadeci bir posta deyilde coxlu sayda postlara like ede biler
    paylasim = models.ForeignKey(Post,on_delete=models.CASCADE)#Yeni like olunann postu gosterir post bir denedir amma onu like eden istifadeciler coxdur
    value = models.CharField(max_length=255,choices=LIKE_CHOICES)
    guncellenme = models.DateTimeField(auto_now=True)
    yaradilma = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.value

#!Commenet modeli
