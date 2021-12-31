from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect,reverse
from account.models import Profile 
from django.urls import reverse
from .forms import PostForm, TagForms,UpdateForm,RegisterForm,LoginForm,CreatePostForm
from django.db.models import F,Q
from django.contrib.auth.models import User
from .models import Like, Post,Comment,Category,Tag
from django.views.generic import  UpdateView,DeleteView
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required#bu funksiyalar ucundu login required olarag
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
# Create your views here.

@login_required(login_url='login')#eger istifaeci giris etmeyibse admin paneline yonlensin giris edib sonra gelsin ele bil
def post_comment_create_and_list_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Post.objects.all()
    
    hit_postlar = Post.objects.filter()
    

    form = PostForm(request.POST or None,request.FILES or None)
    
    if form.is_valid():
        post = form.save(commit=False)
        post.author = profile#yeni giris eden istifadeci ile post atsin hemin adam
        post.save()
        
        return redirect('main-post-view')
    
    context = {
        'qs': qs,   
        'profile': profile,
        'form':form,
        
    }
    return render(request,'main/postlar.html',context)

@login_required(login_url='login')
def like_unlike(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)
        
        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)
        
        like,created = Like.objects.get_or_create(istifadeci=profile, paylasim_id= post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        
            
            post_obj.save()
            like.save()
            
        
        #!Burda ajax kodlari yazilcagdir
        data = {
            'value':like.value,
            'likes':post_obj.liked.all().count()
        }
    
    
    return redirect('main-post-view')
    
@login_required(login_url='login')
def detailPage(request,id):
    istifadeci = Profile.objects.get(user=request.user)

    post = get_object_or_404(Post,id=id)
    
    comments = post.yorum.all()

    # yorumistifadeci = 
    # print(yorumistifadeci)

    comment_sayi = post.yorum.all().count()
    
    hit = Post.objects.filter(id=id).update(hit=F('hit')+1)
    
    context = {
        'post': post,
        'istifadeci':istifadeci,
        'comments':comments,
        'comment_sayi':comment_sayi,
        'hit':hit,
        

        
    }
    return render(request,'main/detail.html',context)

@login_required(login_url='login')
def addComment(request,id):
    article = get_object_or_404(Post,id=id)
    
    if request.method == 'POST':
        comment_content = request.POST.get('comment_content')
        account = Profile.objects.get(user=request.user)
        
        newComment = Comment(body=comment_content,user = account)
        
        newComment.post = article
        newComment.save()
        
        return redirect(reverse('detail',kwargs={'id':id}))#yeni hemin id li posta qayit


def kategoriyalar(request,slug_ismi):
    posts = Post.objects.all().filter(category__slug = slug_ismi)

    
    context = {
        'posts':posts,
        
    }
    return render(request,'main/category.html',context)


def taglar(request,slug_ismi):
    posts = Post.objects.all().filter(tag__slug = slug_ismi)
    context = {
        'posts': posts,
    }
    
    return render(request,'main/tag.html',context)


def post_sahibi(request,id):
    profile = Profile.objects.get(user = id)
    
    
    context = {
        'profile':profile
    }
    return render(request,'main/authorsahibi.html',context)


# class PostDelete(DeleteView):
#     model = Post
#     template_name = 'main/delete.html'
#     success_url = reverse_lazy('main-post-view')#yeni defler istifade elediyimiz return redirect(url name) classlarda ise reverse_lazy den istifade olunur
    
#     def get(self,*args,**kwargs):
#         pk = self.kwargs.get('pk')#classlarda id tanimit pk ni taniyir yeni primary key 
#         obj = Post.objects.get(pk)#yeni hemin id li posta get
        
#         if obj.author.user != self.request.user:#her iki teref user olmalidir yeni user acar sozunden istifade olunmalidir cunki django casir olmasa qaristirri user ile username ve s i ona gore her iki terefde user sozunden itsifade et
#             messages.add_message(self.request,messages.WARNING,'Bu Postu Silmek Haqqiniz Yoxdur')
#         return obj



#login_required yazarsan
@login_required(login_url='login')
def deletepost(request,id):
    post = get_object_or_404(Post,id=id)
    profil = Profile.objects.get(user = post.author.user)#yeni hemin postu yazan istifadecini gotururuk
    
    if profil.user == request.user and request.method == 'POST': 
        post.delete()#yeui hemin id li postu sil
        return redirect('main-post-view')
    
    else:
        messages.add_message(request,messages.WARNING,'Bu postu sile bilmessen')
        
    context = {
        'post':post,#form vasitesile silinen bir posts oldugu ucun normaldir post post deyerini gondermeyimiz
    }
    return render(request,'main/delete.html',context)


#login_required yazarsan
@login_required(login_url='login')
def postupdate(request,id):
    post = get_object_or_404(Post,id=id)
    form = UpdateForm(request.POST or None,request.FILES or None,instance=post)
    
    if form.is_valid():
        page = form.save(commit=False)
        page.author.user = request.user#her iki terefde user deyiskeni olmalidir mutleq cunki django qatisdirir olmasa eger
        page.save()
        return redirect('main-post-view')
    return render(request,'main/update.html',{"form":form,"post":post})



def profile_pic(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        profile_pic = profile_obj.avatar
        post_count = Post.objects.filter(author=profile_obj).all().count()
        
        return {'picture':profile_pic,'profile':profile_obj,'post_count':post_count}
    return {}


@login_required(login_url='login')
def create_all_post(request):
    form = CreatePostForm(request.POST or None,request.FILES or None)
    
    if request.method == 'POST':
        form = CreatePostForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            istifadeci= form.save(commit=False)#yeni hele save etmirem
            hesab = Profile.objects.get(user = request.user)
            istifadeci.author = hesab
            istifadeci.save()
            return redirect('main-post-view')
    
    return render(request,'main/createpost.html',{"form":form})
    
#!Indi Ise regitser login logout islemlerini eleyek

# def registerPage(request):
    
#     if request.method == 'POST':
#         form = RegisterForm(request.POST or None)
#         if form.is_valid():#yeni form dogdurudrsa yeni bir POST request gedibse if e girsin
#             ad = form.cleaned_data.get('ad')
#             mail = form.cleaned_data.get('email')
#             sifre = form.cleaned_data.get('password')
#             sifre2 = form.cleaned_data.get('repassword')

#             if sifre == sifre2:
#                 if User.objects.filter(username=ad).exists():#yeni bele bir istifadeci varsa
#                     messages.add_message(request,messages.WARNING,'Bele Bir Istifaci Adi Movcuddur')
#                     return redirect('register')
#                 else:
#                     if User.objects.filter(email=mail).exists():
#                         messages.add_message(request,messages.WARNING,'Bele Bir Email Movcuddur')
#                         return redirect('register')
                    
#                     else:#eger hec bir problem yoxdursa gir else
#                         form.save()
#                         username  = form.cleaned_data.get('ad')
#                         messages.add_message(request,messages.INFO,'Hesabiniz Ugurlu Bir Sekilde Yaradildi ' + username)
#                         return redirect('main-post-view')
#             else:
#                 messages.add_message(request,messages.ERROR,'Sifrede Xeta Var')
#     else:
#         form = RegisterForm()
    
#     context = {
#         'form':form
#     }
#     return render(request,'main/register.html',context)
    #context dictionarysini hec vact if else icinde yazmag funksiyada 4 boslug sagda yaza fso
    
# def user_register(request):
#         #regustere tikladigim zaman bura gelecek html formu gelib burdakini istifade edecek ele bil
    
#     if request.method == 'POST': #eger melumatlar gorsenmirse
        
#         username = request.POST['ad']#dirnag icinde yazilan melumatlar register htmldeki form methodunun icindeki melumatlardir
#         email = request.POST['email']#registerhtmldeki melumatlatr ['email'] yazilan yer meselen
#         password = request.POST['password']
#         repassword = request.POST['repassword']
        
#         if password == repassword:#exists() TRUE ve ya FALSE deyeri donderir
#             if User.objects.filter(username = username).exists():#1 ci username register html deki usernamedir -------- ikici username ise databaseden gelen usernamedir eger onlar bir birine beraberdirse demeli bele bir istifadeci movcuddur xeta mesaji cixartmagimiz lazimdir
#                 messages.add_message(request,messages.WARNING,'Bu kullanici adi daha once alinmis')
#                 # print('Bu kullanici adi daha once alinmis')
#                 return redirect('register')
        
#         #burda ise emaile gore muqayise olunur
#             else:
#                 if User.objects.filter(email = email).exists():
#                     messages.add_message(request,messages.WARNING,'Bu email daha once alinmis')
#                     #print('Bu email daha once alinmis')
#                     return redirect('register')
                
#                 #icdeki else daha uje bunlarin hecbiri yoxdu yeni yeni ad yeni email ile bir istifadeci adi yaradilir
#                 else:
#                     user = User.objects.create_user(username=username,password=password,email=email)            
#                     user.save()
#                     messages.add_message(request,messages.SUCCESS,'Hesabiniz olsuturuldu')
#                     #print('Kullanici olusturuldur')
#                     return redirect('home')
            
#         else:
#             #messages.add_message(request,messages.WARNING,'Parolalar eslesmiyor')
#             print('Parolalar eslesmiyor')
#             return redirect('register')#urldeki name=register hissesidir
#         #yeniki istifadeci qeydiyyatdan kecenden sonra yeniden register seyfesine qayida bilir yeni avtomatik ora atir syefe onuy
    
    
#     else:
#         return render(request,'main/register.html')


def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST['repassword']

        if password == repassword:#yeni girilen iki sifrede bir birine beraberdirse register olanda
            if User.objects.filter(username=username).exists():
                messages.add_message(request,messages.WARNING,'Bele Bir Istifadeci Adi Movcuddur')
                return redirect('register')

            else:
                if User.objects.filter(email=email).exists():
                    messages.add_message(request,messages.INFO,'Bele Bir Email Movcuddur')
                    return redirect('register')

                #?!Eger hec bir problem yoxdursa bura girecek
                else:
                    user = User.objects.create_user(username=username,email=email,password=password)
                    user.save()#yeni create_user ile istifadecini yaratdigdan sonra save eleyirsen
                    messages.add_message(request,messages.SUCCESS,'Ugurlu Bir Sekilde Qeydiyyatdan Kecdiniz')
                    return redirect('login')
        else:
            messages.add_message(request,messages.ERROR,'Sifreler Uyusmur')
            return redirect('register')
    
    else:
        return render(request,'main/register.html')
    

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']#bu deyerler login.html deyi inputdaki nameden gelir
        password = request.POST['password']
        
        user = authenticate(request,username=username,password=password)
        
        if user is not None:#eger bele bir istifadeci varsa databasede
            login(request,user)
            messages.add_message(request,messages.SUCCESS,'Giris Ettiniz')
            return redirect('main-post-view')
        else:
            messages.add_message(request,messages.ERROR,'Xetali Giris')
            return redirect('login')
        
    else:
        return render(request,'main/login.html')


def cixis_et(request):
    logout(request)
    return redirect('home')


def paylasdigim_postlar(request):
    istifadeci = Profile.objects.get(user=request.user)
    postlar = Post.objects.filter(author=istifadeci).all()
    
    context = {
        'postlar': postlar,
    }
    
    return render(request,'main/paylasdigim.html',context)

def tagyarat(request):
    
    if request.method == 'POST':
        form = TagForms(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TagForms()
    return render(request,'main/createTag.html',{'form':form})
        