from article.views import *
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include


urlpatterns = [
    path('',post_comment_create_and_list_view,name='main-post-view'),
    path('liked/',like_unlike,name='liked-post-view'),
    path('detail/<int:id>',detailPage,name='detail'),
    path('comment/<int:id>',addComment,name='comment'),
    path('category/<slug:slug_ismi>',kategoriyalar,name='category'),
    path('tag/<slug:slug_ismi>',taglar,name='tag'),
    path('postsahibi/<int:id>',post_sahibi,name='postsahibi'),
    path('delete/<int:id>',deletepost,name='delete'),
    path('update/<int:id>',postupdate,name='update'),#burdaki name deyiskenlerini html bu urlin yolunu bildirmek ucun istifade olunur {% url 'update' id varsa eger id yazilir her hansi id lli post olanda meselen post.id bu formada %}
    path('register/',user_register,name='register'),
    path('login/',user_login,name='login'),
    path('logout/',cixis_et,name='logout'),
    path('create-post/',create_all_post,name='create_post'),
    path('my-post-list',paylasdigim_postlar,name='postlarim'),
    path('create-tag/',tagyarat,name='create_tag'),
    
    path('reset_password/',auth_views.PasswordResetView.as_view(),name='reset_password'),#Bir kullanıcının, parolayı sıfırlamak için kullanılabilecek bir kerelik kullanım bağlantısı oluşturarak ve bu bağlantıyı kullanıcının kayıtlı e-posta adresine göndererek parolasını sıfırlamasına izin verir.
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),#return redirect kimidir PassswordResetDovieew email gonderilenden sonra qayidir her hansisa bir seyfeye,yalniz email amma hele biz o emaile girib linke tiklamamisig
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),#Burda PasswordResetConfirm view ise yeni sifremizi girmek ucun bize form gonderer
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete')#Kullanicinn sifresini basarilis bir sekilde deyisdini mesajini verer Passwordresetcompleteview
]