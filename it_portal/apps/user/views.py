from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Profile, ProfileSubscriber
from apps.custom_auth.views import session_account_manager
from django.views.generic import View
from .forms import subscribeForm
from apps.portal.models import Article, Comment, ReplyComment
from django.http import Http404

class ProfileView(View):
    def get(self, request, get_username):
        title = "IT-blog | " + get_username
        template = 'user/profile.html'
        name = 'top'

        is_sub = None

        request = session_account_manager(request)
        saved_account = request.session['saved_account']
        request.session['last_page'] = request.path

        user = get_object_or_404(User, username = get_username)

        try:
            profile = Profile.objects.get(user=user)
        except:
            profile = Profile.objects.create(user=user)
            profile.save()

        Subscribers = profile.get_subscribers()

        if request.user.is_authenticated:
            if ProfileSubscriber.objects.filter(user=request.user, author=profile).count() == 0:
                is_sub = False
            else:
                is_sub = True

        sub_str = profile.get_subscribers_str(Subscribers)

        profileArticles = Article.objects.filter(author=profile).order_by('-view')[:6]
        if profileArticles.count() == 0:
            profileArticles = None
            art_count = None
        else:

            art_count = str(profileArticles.count()) + ' стать'

            str_value = str(profileArticles.count())

            if str_value[-1] == '1':
                art_count += 'я'
            elif int(str_value[-1]) >= 5 or int(str_value[-1]) == 0:
                art_count += 'ей'
            else:
                art_count += 'и'

        comments = Comment.objects.filter(author=profile.user).order_by('timestamp').reverse()
        comments_split = comments[:1]

        context = { 'profile': profile, 'sub_str': sub_str, 'Subscribers': Subscribers, 'saved_account': saved_account, 'title': title, 'is_sub': is_sub, 'subscribe_form': subscribeForm(), 'profileArticles': profileArticles, 'profileArtCount': art_count, 'name': name, 'comments': comments, 'comments_split': comments_split }

        return render(request, template, context)

    def post(self, request, get_username):
        profile = Profile.objects.get(user=User.objects.get(username=get_username))
        if request.user.is_authenticated:
            if ProfileSubscriber.objects.filter(user=request.user, author=profile).count() == 0:
                is_sub = False
            else:
                is_sub = True

            if is_sub == False:
                subscribe_form = subscribeForm(request.POST)
                if subscribe_form.is_valid():
                    subscribe_form.save(request, profile)
                    return redirect(request.session['last_page'])

            else:
                subscribe_form = subscribeForm(request.POST)
                if subscribe_form.is_valid():
                    subscribe_form.delete(request, profile)
                    return redirect(request.session['last_page'])

        else:
            return redirect(request.session['last_page'])

class ProfileArticlesView(View):
    def get(self, request, get_username):
        title = "IT-blog | " + get_username
        template = 'user/articles.html'
        name = 'post'

        request = session_account_manager(request)
        saved_account = request.session['saved_account']
        request.session['last_page'] = request.path

        user = get_object_or_404(User, username=get_username)

        articles = Article.objects.filter(author=user.profile)

        context = { 'title': title, 'saved_account': saved_account, 'name': name, 'articles': articles, 'author': user }
        return render(request, template, context)

    def post(self, request, get_username):
        pass

class ProfileSubscriptionsView(View):
    def get(self, request, get_username):
        if get_object_or_404(User, username=get_username).pk == request.user.pk:
            subs = ProfileSubscriber.objects.filter(user=request.user)

            title = "Мои подписки: {}".format(subs.count())
            template = 'user/subs.html'

            context = { 'title': title, 'Subscriptions': subs }
            return render(request, template, context)

        else:
            raise Http404('У вас нет прав для просмотра данной страницы')
