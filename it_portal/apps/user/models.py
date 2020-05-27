import re
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, post_delete
from easy_thumbnails.fields import ThumbnailerImageField
from django.dispatch import receiver

def generate_filename(instance, filename):
    filename = str(instance.user) + '.' + re.split(r'[.\s]', filename)[-1]
    return '{}/{}/{}'.format('profiles', instance, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    status = models.TextField(max_length=150, default="", blank=True, verbose_name='Статус')
    avatar = ThumbnailerImageField(resize_source={ 'size': (800, 800), 'crop': 'smart' }, upload_to=generate_filename, default='../static/img/default_avatar.png', verbose_name='Фото профиля')
    sub_count = models.PositiveIntegerField(default=0, verbose_name='Кол-во подписчиков (неточно)') # just for top page.

    def get_subscribers(self): # get profile subscribers
        subscribers = ProfileSubscriber.objects.filter(author=self)
        return subscribers

    def get_subscribers_str(self, subscribers): # get profile subscribers as string
        if subscribers is not None:
            sub_str = str(subscribers.count()) + ' подписчик'
            str_value = str(subscribers.count())

            if str_value[-1] == '1':
                pass
            elif str_value[-1] == '3':
                sub_str = sub_str + 'a'
            elif subscribers.count() % 2 == 0 and subscribers.count() != 0:
                sub_str = sub_str + 'а'
            else:
                sub_str = sub_str + 'ов'
        else:
            sub_str = ''

        return  sub_str


    def get_absolute_url(self):
        return '/profile/{}'.format(self.user.username)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

class ProfileSubscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Кто подписался') #Пользователь, который подписался
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='На кого подписался') #То, на кого он подписался
    date = models.DateTimeField(blank=True, auto_now_add=True, verbose_name='Дата') #Когда подписался(Не выводится в admin-panel, т.к имеет auto_now_add=True)

    def __str__(self):
        return str('Пользователь: {}, подписался на: {}. ({})' .format(self.user, self.author, self.date.date()))

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created == True:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except:
        pass

@receiver(post_save, sender=ProfileSubscriber)
def up_subcount(sender, instance, **kwargs):
    Profile = instance.author
    Profile.sub_count = ProfileSubscriber.objects.filter(author=Profile).count()
    Profile.save()

@receiver(post_delete, sender=ProfileSubscriber)
def down_subcount(sender, instance, **kwargs):
    Profile = instance.author
    Profile.sub_count = ProfileSubscriber.objects.filter(author=Profile).count()
    Profile.save()

