from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound, JsonResponse 
from django.shortcuts import render, redirect, get_object_or_404 
from django.urls import reverse_lazy

from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.core.paginator import Paginator
from django.core.mail import send_mail

from taggit.models import Tag

from .models import Article, Comment 
from .forms import UserLoginForm, UserRegisterForm, ArticleForm

@login_required(login_url = '/login/')
def aboutView(request):
    return render(request, 'about.html')

@login_required(login_url = '/login/')
def contactView(request):
    if request.method == 'POST':
        name = request.POST['name']
        from_email = request.POST['email']
        title = request.POST['subject']
        message = request.POST['message']
        send_mail(f'{name}: {title}', message, from_email, ['ahmadjonovibrohim062@gmail.com'])
        messages.info(request, 'Xabaringiz yaqin vaqt ichida jo\'natiladi')
        return redirect('/')
    return render(request, 'contact.html')


@login_required(login_url = '/login/')
def index(request):
    query = request.GET.get('query')
    if query:       
        articles = Article.objects.filter(Q(description__icontains = query) | Q(title__icontains = query) | Q(tags__name__icontains = query)).distinct()
        if not articles:
            messages.info(request, 'Qidiruv bo\'yicha hech nima topilmadi')
    else:
        articles = Article.objects.all()
    paginator = Paginator(articles, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        
    return render(request, 'index.html', {'page_obj': page_obj})

@login_required(login_url = '/login/')
def articleDetailView(request, id):
    article = Article.objects.get(id = id)
    tags = Tag.objects.all()
    if request.method == 'POST':
        if article.author == request.user:
            return redirect('/')
        comment = Comment.objects.create(
            article = article,
            user = request.user,
            answer = request.POST['answer'],
        )
    return render(request, 'post.html', {
        'article': article,
        'tags': tags,
    })

@login_required(login_url = '/login/')
def commentCreateView(request, id):
    if request.method == 'POST':
        if request.POST['answer']:
            # print(request.POST)
            Comment.objects.create(
                article = Article.objects.get(id = id),
                user = request.user,
                answer = request.POST['answer'],
            )
    return redirect(reverse_lazy('article_detail', args = [str(id)]))
            

@login_required(login_url = '/login/')
def replyView(request, id):
    if request.method == 'POST':
        parent_comment = Comment.objects.get(id = id)
        if request.user == parent_comment.user:
            return redirect(f'/article/{parent_comment.article.id}')
        new_comment = Comment.objects.create(
            article = parent_comment.article,   
            user = request.user,
            answer = request.POST['answer'],
            parent = parent_comment
        )
        print(request.POST['answer'])
        return redirect(f'/article/{parent_comment.article.id}')
    return render(request, 'reply.html')
    
    
@login_required(login_url = '/login/')
def articleCreateView(request):
    articleform = ArticleForm()
    if request.method == 'POST':
        articleform = ArticleForm(request.POST, request.FILES)
        if articleform.is_valid():
            dict = articleform.cleaned_data 
            article = Article.objects.create(
                title = dict['title'],
                description = dict['description'],
                author = request.user,
                image = dict['image'],                
            )
            for tag in dict['tags']: 
                article.tags.add(tag)
            print(article.title, article.description, article.tags)
            return redirect('/')
    return render(request, 'article_create.html', {'form': articleform})

@login_required(login_url = '/login/')
def articleUpdateView(request, id):
    article = Article.objects.get(id = id)
    articleform = ArticleForm(instance = article)
    if article.author != request.user:
        return redirect('/')
    if request.method == 'POST':
        articleform = ArticleForm(request.POST, request.FILES, instance = article)
        if articleform.is_valid():
            dict = articleform.cleaned_data 
            article.title = dict['title']
            article.description = dict['description']
            article.author = request.user 
            article.image = dict['image']
            article.tags.add(*dict['tags'])
            article.save()
            return redirect('/')
    return render(request, 'article_create.html', {'form': articleform})

@login_required(login_url = '/login/')
def articleDeleteView(request, id):
    article = Article.objects.get(id = id)
    if article.author != request.user:
        return redirect('/')
    if request.method == 'POST':
        article.delete()
        return redirect('/')
    return render(request, 'article_delete.html', {'article': article})
    

@login_required(login_url = '/login/')
def tagView(request, tag):
    articles = Article.objects.filter(tags__name__in = [tag])
    paginator = Paginator(articles, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'page_obj': page_obj})

def register(request):
    userform = UserRegisterForm()    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        # print(username, email, password1, password2)
        
        if password1 == password2:
            if auth.get_user_model().objects.filter(username = username).exists():
                messages.info(request, 'Foydalanuvchining ismi bazada mavjud ekan, qaytadan urinib ko\'ring')
                return redirect('signup')
            elif auth.get_user_model().objects.filter(email = email).exists():
                messages.info(request, 'Foydalanuvchining emaili bazada mavjud ekan, qaytadan urinib ko\'ring')
                return redirect('signup')           
            else:
                user = auth.get_user_model().objects.create_user(username = username, email = email, password = password1)
                return redirect('login')      
        else:
            messages.info(request, 'Parollar bir xil emas, qaytadan urinib ko\'ring')
            return redirect('signup')
    return render(request, 'register.html', {'form': userform}) 

def login(request):
    userform = UserLoginForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user:
            messages.info(request, f"Xush kelibsiz, {username}")            
            auth.login(request, user)
            return redirect('/')    
    return render(request, 'login.html', {'form': userform})


def logout(request):
    auth.logout(request)
    return redirect('/')    