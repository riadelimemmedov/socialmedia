from django import template
from article.models import Category, Post,Comment,Like, Tag
from account.models import Profile

register = template.Library()

@register.simple_tag(name='post_count')
def all_post_count():#custom taglarin her birinde self olmur cunki class filan istifade etmirik burda
    return Post.author.objects.all().count()


@register.simple_tag(name='categories_all')
def all_categories():
    return Category.objects.all()

@register.simple_tag(name='tags_all')
def all_tags():
    return Tag.objects.all() 

@register.simple_tag(name='hitpost')
def hitler():
    return Post.objects.all().order_by('hit')#hit_postlari siralayiram

@register.simple_tag(name='profiller')
def profil_listeleri():
    return Profile.objects.all().count()