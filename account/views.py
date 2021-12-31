from django.dispatch.dispatcher import receiver
from article.models import Post
from django.shortcuts import render,HttpResponse,get_object_or_404,redirect,reverse
from .forms import ContactForm, UpdateAccount
from django.contrib.auth.decorators import login_required
from article.models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import F,Q
from django.views.generic.list import *
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required#bu funksiyalar ucundu login required olarag
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from django.views.generic.edit import FormView
from django.urls import reverse_lazy #return redirect basqa bir formasidir tercumesi ise yonlendirmek menasini verir
from django.contrib.messages.views import SuccessMessageMixin


from .models import *
# Create your views here.

#@login_required(login_url='login')
def home_view(request):
    user = request.user
    context = {
        'user':user,#request.user hal hazirda giris eden istifadecini gosterir
    }
    return render(request,'main/home.html',context)

#@login_required(login_url='login')
def my_profile_view(request):#giris eden istifadecinin profilini gostermek lazimdir Yadda saxlaki  Her bir istifadecinin profili models.py da saxlajir
    my_account = Profile.objects.get(user=request.user)#yeni giris eden istifadecinin profilini gostersin giris eden istifadecini elde etmek ucun request.userdan istifade olunur
    my_post_count = Post.objects.filter(author=my_account).all().count()
    
    
    context = {       
        'my_account':my_account,
        'my_post_count':my_post_count,
    }
    return render(request,'main/myprofile.html',context)
    

#@login_required(login_url='login')
def friend_list(request):
    customer = Profile.objects.get(user=request.user)    
    
    context={ 
        'customer':customer,
    }
    return render(request,'main/friends.html',context)

#@login_required(login_url='login')
def detail_friend(request,id):
    profile = Profile.objects.get(user = id)#yeni hemin id li istifadecnin getirdik heminn melumatlarini gotururuk
    
    profile2 = Profile.objects.get(user=id).gender='Kisi'
    profile3 = Profile.objects.get(user=id).gender='Kadin'
    profile4 = Profile.objects.get(user=id).gender='Yeniyetme'
    
    
    context = {
        'profile':profile,
        'profile2':profile2,
        'profile3':profile3,
        'profile4':profile4,
    }
    return render(request,'main/dost.html',context)

#@login_required(login_url='login')
def updateaccount(request):#update elemek ucun accountu mutleq giris etmelisenki hesabiva duzelisler edesen ona gore giris eden istifadecini almaliyig reques.user ile1
    istifadeci = Profile.objects.get(user = request.user)
    
    form = UpdateAccount(request.POST or None,request.FILES or None,instance=istifadeci)
    
    
    if request.method == 'POST':
        form = UpdateAccount(request.POST or None,request.FILES or None,instance=istifadeci)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'Hesabiniz Ugurlu Bir Sekilde Guncellendi')
            return redirect('my_profile')
    
    context = {
        'form':form,
    }
    return render(request,'main/updateprofile.html',context)




#*RelationShip funksiyalari


#!Bize gelen istekleri onaylama ve redd etme
#@login_required(login_url='login')
def invites_recived_view(request):#*mene gelen devetleri tutur bu funksiyac yeni request.usera gelen devetleri amma modelde filterle recived sonra donder bura yeni viewe
    profile = Profile.objects.get(user = request.user)#yeni giris eden istfiadeciye gelen devetleri getirsin bu funksiya
    qs = RelationShip.data.invatations_received(profile)#qebul eden istifadeci
    results = list(map(lambda x: x.sender,qs))#yeni qs deki profile send eleyen istifadeciler yeni senderler
    
    is_empty = False
    
    if len(results) == 0:#Yenin eger result listesinin uzunlugu sifirdursa if e girsin ancag diqqtli ol if ancag true olanda isleyir ona gore is_empty e true verdik
        is_empty = True
    
    context = {
        'qs':results,
        'is_empty':is_empty
    }
    return render(request,'main/my_invites.html',context)

#@login_required(login_url='login')
def accept_invitation(request):
    if request.method == 'POST':
        
        pk = request.POST.get('profile_pk')
        istek_atan = Profile.objects.get(id=pk)
        
        qebul_eleyen = Profile.objects.get(user=request.user)
        
        rel = get_object_or_404(RelationShip,sender=istek_atan,reciver=qebul_eleyen)
        if rel.status == 'Send':#yeni bir istek gelibse ve sen qebul elemek isteyirnsese on isteyi cevir rel.status = 'Accepted' ele 
            rel.status = 'Accepted'
            rel.save()
        return redirect('my_invites')

#@login_required(login_url='admin/')
def reject_invitation(request):
    if request.method == 'POST':
        
        #Indi ise istek atan istifadecnin id sine uygun profiili secek
        pk = request.POST.get('profil_id')
        istek_atan = Profile.objects.get(id=pk)
        
        #Indi ise sayta giris eden istfiadeci yeni hesabinda olan istifadecini alag hazirda aktiv istifadecini saytda olan aktiv istifadeci yeni
        redd_eden = Profile.objects.get(user=request.user)
        
        rel = get_object_or_404(RelationShip,sender=istek_atan,reciver=redd_eden)
        rel.delete()#yeni gelen isteyi silirik
    
        return redirect('my_invites')



################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
#@login_required(login_url='login')
def profile_list_view(request):
    user = request.user
    qs = Profile.hesab.get_all_profiles(user)#Profile modeli icindeki hesab deyiskeni ProfileManager modeline baglidir get_all_profiles funksiyasida orda olduguna gore bu formada yazildi
    
    
    context = {
        'qs': qs
    }
    return render(request,'main/profile_list.html',context)


#!Her hansi bir profilin detalina getme
# class ProfileDetailView(DetailView):
#     model = Profile
#     template_name = 'main/aboutprofile.html'
    
#     def get_object(self,slug=None):
#         slug = self.kwargs('slug')#yeni contet kimi istifade edecem slugu self.kwargs('slug') vasitesile
#         profile = Profile.objects.get(slug=slug)#yeni hemin profile uygun bir slug tapilsin
#         return profile#cunki funksiya bitir ve sonda bir deyer donmelidir artig
    
#     def get_context_data(self, **kwargs):
#         context = super(ProfileDetailView,self).get_context_data(**kwargs)
#         user = User.objects.get(username__iexact = self.request.user)
#         profile = Profile.objects.get(user = user)#yeni hal hazirda aktiv olan istifadecini Profile nesnesine cevirirem
        
        
#         rel_gonderdiyim_istek = RelationShip.objects.get(sender=profile)
#         rel_mene_gelen_istek = RelationShip.objects.get(reciver= profile)
        
#         gonderdiyim_istek = []
#         gelen_istek = [] 
        
#         for item in rel_gonderdiyim_istek:
#             gonderdiyim_istek.append(item.reciver.user)#yeni qebul edecek olan istifadeci bu listeye elave olunur
            
#         for item in rel_mene_gelen_istek:
#             gelen_istek.append(item.sender.user)
            
        
#         context['gonderdiyim_istek'] = gonderdiyim_istek
#         context['gelen_istek'] = gelen_istek
#         context['posts'] = self.get_object().postlar()
#         context['len_posts'] = True if len(self.get_object().post_count()) > 0 else False
#         return context
#         #eger html da context istifade etmek isteyirsense object acar sozunden istifade et

#@login_required(login_url='login')
def profile_detali(request,pk):
    profile = Profile.objects.get(user=pk)
    posts = Post.objects.filter(author=profile).all()
    
    rel_gonderdiyim_istek = RelationShip.data.filter(sender = profile)#!yeni men ne edirem men gonderiyim istekleri sender dan cekirem,yeni hansi istifadecile isteka atiram
    rel_mene_gelen_istek = RelationShip.data.filter(reciver = profile)
    
    
    gonderdiyim_istek = []
    gelen_istek = []        
        
    for item in rel_gonderdiyim_istek:
        gonderdiyim_istek.append(item.reciver.user)
        
    for response in rel_mene_gelen_istek:
        gelen_istek.append(response.sender.user)
    
    context = {
        'profile':profile,
        'gonderdiyim_istek':gonderdiyim_istek,
        'gelen_istek':gelen_istek,
        'posts':posts,
    }
    
    return render(request,'main/aboutprofile.html',context)
    


class ProfileListView(ListView,LoginRequiredMixin):
    login_url = 'login'
    model = Profile
    template_name = 'main/profile_list.html'
    context_object_name = 'amk'
    
    def get_queryset(self):#query yazirig ona gore querysetlerden istifade edirik
        qs = Profile.hesab.get_all_profiles(self.request.user)
        return qs#burdaki qs deyeri yuxardaki context_object_nameden gelen 'amk' beraberdir

    def get_context_data(self,**kwargs):#classin icinde yazmagi unutma bunu
        context = super(ProfileListView,self).get_context_data(**kwargs)
        istifadeci = User.objects.get(username__iexact=self.request.user)#iexact o demekdriki boyuk ve ya kicik herf ferq etmir hemin istifadecinin getirsin
        profile = Profile.objects.get(user=istifadeci)
        
        rel_gonderdiyim_istek = RelationShip.data.filter(sender = profile)#!yeni men ne edirem men gonderiyim istekleri sender dan cekirem,yeni hansi istifadecile isteka atiram
        rel_mene_gelen_istek = RelationShip.data.filter(reciver = profile)#!mene gelen istekleri ise reciver tutur yeni qebul olunan ve ya gelen,yeni hansi istifadeciler teefindengelene istekler
        
        postlar = Post.objects.filter(author=profile).all()
        
        gonderdiyim_istek = []
        gelen_istek = []        
        
        for item in rel_gonderdiyim_istek:
            gonderdiyim_istek.append(item.reciver.user)
        
        for response in rel_mene_gelen_istek:
            gelen_istek.append(response.sender.user)
        
        
        context['gonderdiyim_istek'] = gonderdiyim_istek
        context['gelen_istek'] = gelen_istek
        
        context['is_empty'] = False #yeni bir istifadeci varki truedu
        context['postlar'] = postlar
        
        if len(self.get_queryset()) == 0:#yeni queyden istifadeci gelmeyibse saytda hec kim yoxdursa 
            context['is_empty'] = True #eger site adam yoxdursa true donder onsuz if true olanda isleyir mentiq ile baxanda
        
        return context

    def get_success_url(self):
        return reverse('profile_detail',kwargs={'pk':self.object.pk})

#@login_required(login_url='login')
def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.hesab.get_all_to_invate(user)
    
    context = {
        'qs':qs,
    }
    return render(request,'main/to_invite_list.html',context)



#!Create ve Delete friend islemleri
#@login_required(login_url='login')
def create_friend(request):#dostlug atma
    if request.method == 'POST':
        my_account = request.user #yeni giris etdiyim istifadeci
        my_friend = request.POST.get('profile_pk')#bura bize id deyeri donderecek ve Profile modelinden hemin id e uygun profil tapmaliyig
        
        #?Ve indi bulari profile cevirek
        sender = Profile.objects.get(user=my_account)
        reciver = Profile.objects.get(id=my_friend)#yeni hemin id li profile donder bize yeni tap bele deyim
        
        rel = RelationShip.data.create(sender=sender,reciver=reciver,status = 'Send')
        return redirect(request.META.get('HTTP_REFERER'))#yeni oz yerine qayitsin hardadisa ora formdan hansi seyfe gelibse ora qayitsin ele bil request.META('HTTP_REFERER') ISE YARAYIR
    
    #*Eger method == GET dirse onda bura girecek bir cur else dir yeni
    return redirect('my_profile')


#@login_required(login_url='login')
def remove_friend(request):#burda uje databasede var biz uje burda silme islemi eleyirik databaseden bele deyim yeni
    if request.method == 'POST':
        pk = request.POST.get('dostadi')
        user = request.user
    
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(id=pk)
        
        rel = RelationShip.data.get( (Q(sender=sender) & Q(reciver=receiver) | Q(sender=receiver) & Q(reciver=sender)))
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('my_profile')

#login_required(login_url = 'login')
def invitatons_receiver_number(request):#mene gelen isteklerin sayini alan funksiya
    if request.user.is_authenticated:
        profil = Profile.objects.get(user=request.user)#yeni hal hazirda giris eden istifadecini aliram ve Profil nesnesine donustururem
        elaqe = RelationShip.data.invatations_received(profil).count()#yeni giris eden istifadeciye gelen istejler
        return {'say':elaqe}
    return {}#bunu return olmadan yazmag ucun ise settings.py fa doysa yolunu gostermen lazimdir unutma bunu


def search_account(request):
    response = request.GET.get('q')

    if response:#eger inputda deyer girilibse gir if e eger deyer yoxdursa else gir message ver djangodaki message kitabxanasi vasitesile
        netice = Profile.objects.filter(Q(first_name__contains=response)|Q(last_name__contains=response)).order_by('-id').distinct()#| bu oparator ve ya menaisini verir yeni or & bu ise and menasini verir Js de her ikisi cut formasa islenir or ve and in  or => || and => &&
        return render(request,'main/searchprofile.html',{'netice':netice})#yeni donen neticeni html seyfesinde gosterirem
        
        # netice = Profile.objects.filter(Q(first_name__contains=response)|Q(last_name__contains=response)).order_by('-id').distinct()#| bu oparator ve ya menaisini verir yeni or & bu ise and menasini verir Js de her ikisi cut formasa islenir or ve and in  or => || and => &&
        # if response != netice:
        #     messages.add_message(request,messages.ERROR,'Bele Bir Istifadeci Tapilmadi')
        #     return redirect('home')
    
    # else:#?else hemise isleyir if ise true olanda isleyir
    #     return redirect('home')


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)#yeni giris eden istifadeci ile bir dene POST request gonderirik
        if form.is_valid():#eger formdan donnen deyer metod olarag post requeste beraberdirse if e girecek onszuda if ancag true sertlerinde isleyir
            user = form.save()
            update_session_auth_hash(request,user)#yenihal hazirdaki istiafecinin bilgilerini gucelle
            return redirect('login')
        else:
            messages.add_message(request,messages.INFO,'Dogru Deyerler Girin')
    else:
        form = PasswordChangeForm(request.user)
    return render(request,'main/password_change.html',{"form":form})


#?Contact Form Hisssesi

class ContacView(SuccessMessageMixin,FormView):
    template_name = 'main/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('my_profile')
    success_message = 'Mesajiniz Gonderildi'
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)