from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from apps.user.models import Profile, ProfileSubscriber
from allauth.account.forms import LoginForm
from apps.custom_auth.views import session_account_manager
from apps.portal.models import Article, Category, Comment, ReplyComment, ArticleLike
from django.db.models import Q
from django.views.generic import View
from apps.user.forms import subscribeForm
from apps.portal.forms import commentForm

def get_User(username):
    UserObject = get_object_or_404(User, username=username)
    return UserObject

def get_Profile(username):
    user = get_User(username)
    if Profile.objects.filter(user=user).count() == 0:
        Profile.objects.create(user=user)
        
    ProfileObject = get_object_or_404(Profile, user=user)
    return ProfileObject

def get_Sub(username):
    Subscribers = ProfileSubscriber.objects.filter(author=get_Profile(username))
    return Subscribers


class Main(View):
    def get(self, request):
        title = 'IT-blog | Статьи, Уроки, Форум'
        template = 'portal/index.html'
        name = 'main'

        if request.user.is_authenticated:
            Subscribers = request.user.profile.get_subscribers()
            sub_str = request.user.profile.get_subscribers_str(Subscribers)

        else:
            sub_str = None

        request = session_account_manager(request)
        saved_account = request.session['saved_account']
        request.session['last_page'] = request.path

        context = { 'title': title, 'subscribers_value': sub_str, 'saved_account': saved_account, 'name': name }

        return render(request, template, context)

class Articles(View):
    def get(self, request):
        title = 'IT-blog | Статьи'
        name = 'post'
        template = 'portal/posts.html'

        request = session_account_manager(request)
        saved_account = request.session['saved_account']
        login_form = LoginForm()
        request.session['last_page'] = request.path

        sort = request.GET.get('sort')
        category_slug =  request.GET.get('category', 'all')
        q = request.GET.get('q')

        if q:
            request.session['post_search'] = q
            if category_slug == 'all':
                articles = Article.objects.filter(
                    Q(title__icontains=q)|
                    Q(content__icontains=q)
                ).order_by('-timestamp')

            else:
                category = get_object_or_404(Category, slug=category_slug)
                articles = Article.objects.filter(
                Q(title__icontains=q, category=category)|
                Q(content__icontains=q, category=category)
                ).order_by('-timestamp')

        else:
            request.session['post_search'] = None
            if category_slug == 'all':
                articles = Article.objects.order_by('-timestamp')
            else:
                category = get_object_or_404(Category, slug=category_slug)
                articles = Article.objects.filter(category=category).order_by('-timestamp')

        if sort == 'asc':
            articles = articles.order_by('timestamp')

        try:
            last_search_q = request.session['post_search']
        except:
            last_search_q = None

        categories = Category.objects.all()

        return render(request, template, locals())

class Post(View):
    def get(self, request, pk=0):
        template = 'portal/post-view.html'
        name = 'post'

        request = session_account_manager(request)
        saved_account = request.session['saved_account']
        login_form = LoginForm()
        request.session['last_page'] = request.path

        is_liked = None
        is_sub = None

        if pk == 0:
            return redirect('/articles/')

        else:
            article = get_object_or_404(Article, pk=pk)

            if request.GET.get('action') == None:
                article.add_view()

            comments = Comment.objects.filter(article=article)
            replyComments = ReplyComment.objects.filter(article=article)

            comments_count = len(comments) + len(replyComments)

            comments_str = str(comments_count) + ' комментар'

            if comments_count == 1:
                comments_str += 'ий'

            elif comments_count > 0 and comments_count < 5:
                comments_str += 'ия'
            
            else:
                comments_str += 'иев'


            title = 'IT-blog | ' + article.title
            subs = article.author.get_subscribers()
            if subs is not None:
                subscribers_value = str(len(subs))
            else:
                subscribers_value = 0

            if request.user.is_authenticated:
                if ArticleLike.objects.filter(profile=request.user.profile, article=article).count() == 0:
                    is_liked = False
                else:
                    is_liked = True

                if ProfileSubscriber.objects.filter(user=request.user, author=article.author).count() == 0:
                    is_sub = False
                else:
                    is_sub = True

                if request.GET.get('action') == 'like':
                    if is_liked == False:
                        like = ArticleLike.objects.create(profile=request.user.profile, article=article)
                        like.save()
                        return redirect(article.get_absolute_url() + '#like')

                if request.GET.get('action') == 'unlike':
                    if is_liked:
                        like = ArticleLike.objects.get(profile=request.user.profile, article=article)
                        like.delete()
                        return redirect(article.get_absolute_url() + '#like')

            popular = Article.objects.order_by('-view')[:5]

            context = { 'article': article, 'comments_count': comments_count, 'comments_str': comments_str, 'comments': comments,
                       'replyComments': replyComments, 'is_liked': is_liked, 'is_sub': is_sub, title: 'title',
                       'subscribe_form': subscribeForm(), 'comment_form': commentForm(), 'subs': subs, 'subscribers_value': subscribers_value,
                       'popular': popular, 'saved_account': saved_account, 'loginForm': login_form, 'name': name }

            return render(request, template, context)

    def post(self, request, pk=0):

        article = get_object_or_404(Article, pk=pk)

        if 'write_comment' in request.POST:
            comment_form = commentForm(request.POST, request.FILES)

            if comment_form.is_valid():

                comment = comment_form.save(commit=False)

                comment.author = request.user
                comment.article = article
                comment.image = request.FILES['image']
                comment.content = request.POST['content']
                
                comment.save()
            
            return redirect(article.get_absolute_url() + '#comments')


        if 'subscribe' in request.POST:

            if ProfileSubscriber.objects.filter(user=request.user, author=article.author).count() == 0:
                is_sub = False
            else:
                is_sub = True

            subscribe_form = subscribeForm(request.POST)

            if is_sub == False:
                if subscribe_form.is_valid():
                    subscribe_form.save(request, article.author)

            else:
                if subscribe_form.is_valid():
                    subscribe_form.delete(request, article.author)

            return redirect(article.get_absolute_url() + '#profileCard')
        

class ArticleNew(View):
    def get(self, request):
        name = 'post'
        title = 'IT-blog | Уроки'
        template = 'portal/post-new.html'

        request = session_account_manager(request)
        saved_account = request.session['saved_account']
        login_form = LoginForm()
        request.session['last_page'] = request.path

        return render(request, template, locals())

class Lesson(View):
    def get(self, request, pk=0):
        name = 'lesson'
        title = 'IT-blog | Уроки'
        template = 'portal/lessons.html'

        request = session_account_manager(request)
        saved_account = request.session['saved_account']
        login_form = LoginForm()
        request.session['last_page'] = request.path

        return render(request, template, locals())

class Top(View):
    def get(self, request):
        title = 'IT-blog | Топ #15'
        template = 'portal/top.html'
        name = 'top'

        request = session_account_manager(request)
        saved_account = request.session['saved_account']
        request.session['last_page'] = request.path

        top = Profile.objects.order_by('-sub_count')[:15]

        context = { 'title': title, 'saved_account': saved_account, 'top': top, 'name': name}
        return render(request, template, context)
