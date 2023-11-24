from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.conf import settings

# Create your models here.

class VerificationTokenManager(models.Manager):
    
    def get_queryset(self):
        return super().get_querset().filter(
            date_created__gte=datetime.now()-timedelta(minutes=10)
        )

class OneTimeСode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=5)
    time_in = models.DateTimeField(auto_now_add=True, db_index=True)
    
class Author(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  user_rating = models.IntegerField(default=0)

  def like(self):
    self.user_rating += 1

  def dislike(self):
    self.user_rating -= 1

  def rating_clear(self):
    self.user_rating = 0

  def __str__(self):
    return f'{self.user.username}'
  
class UserAvatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='<svg viewBox="0 0 61.80355 61.80355" xmlns="http://www.w3.org/2000/svg" fill="#000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <title></title> <g data-name="Layer 2" id="Layer_2"> <g data-name="—ÎÓÈ 1" id="_ÎÓÈ_1"> <circle cx="30.8999" cy="30.8999" fill="#9f82bb" r="30.8999"></circle> <path d="M23.255 38.68l15.907.121v12.918l-15.907-.121V38.68z" fill="#f9dca4" fill-rule="evenodd"></path> <path d="M53.478 51.993A30.814 30.814 0 0 1 30.9 61.8a31.547 31.547 0 0 1-9.23-1.402 31.124 31.124 0 0 1-13.626-8.704l1.283-3.1 13.925-6.212c0 4.535 1.519 7.06 7.648 7.153 7.57.113 8.261-2.515 8.261-7.19l12.79 6.282z" fill="#ffffff" fill-rule="evenodd"></path> <path d="M39.166 38.778v3.58c0 .297-.004.802-.029 1.273-4.155 5.56-14.31 2.547-15.771-5.053z" fill-rule="evenodd" opacity="0.11"></path> <path d="M31.129 8.432c21.281 0 12.988 35.266 0 35.266-12.266 0-21.281-35.266 0-35.266z" fill="#ffe8be" fill-rule="evenodd"></path> <path d="M18.365 24.045c-3.07 1.34-.46 7.687 1.472 7.658a31.978 31.978 0 0 1-1.472-7.658z" fill="#f9dca4" fill-rule="evenodd"></path> <path d="M44.14 24.045c3.07 1.339.46 7.687-1.471 7.658a31.997 31.997 0 0 0 1.471-7.658z" fill="#f9dca4" fill-rule="evenodd"></path> <path d="M22.035 35.1a1.879 1.879 0 0 1-.069-.504v-.005a1.422 1.422 0 0 1 1.22-1.361 1.046 1.046 0 0 0 .907 1.745 4.055 4.055 0 0 0 .981-.27c.293-.134.607-.289.943-.481a13.439 13.439 0 0 0 1.426-1.014 3.04 3.04 0 0 1 1.91-.787 2.015 2.015 0 0 1 1.293.466 2.785 2.785 0 0 1 .612.654 2.77 2.77 0 0 1 .612-.654 2.015 2.015 0 0 1 1.292-.466 3.039 3.039 0 0 1 1.911.787 13.42 13.42 0 0 0 1.426 1.014c.336.192.65.347.943.48a4.054 4.054 0 0 0 .981.271 1.046 1.046 0 0 0 .906-1.745 1.422 1.422 0 0 1 1.22 1.36h.002l-.001.006a1.879 1.879 0 0 1-.069.504c-.78 3.631-7.373 2.769-9.223.536-1.85 2.233-8.444 3.095-9.223-.536z" fill="#8a5c42" fill-rule="evenodd"></path> <path d="M26.431 5.74h9.504a8.529 8.529 0 0 1 8.504 8.504v6.59H17.927v-6.59a8.529 8.529 0 0 1 8.504-8.504z" fill="#464449" fill-rule="evenodd"></path> <path d="M12.684 19.828h36.998a1.372 1.372 0 0 1 1.369 1.368 1.372 1.372 0 0 1-1.369 1.37H12.684a1.372 1.372 0 0 1-1.368-1.37 1.372 1.372 0 0 1 1.368-1.368z" fill="#333" fill-rule="evenodd"></path> <path d="M17.927 15.858H44.44v3.97H17.927z" fill="#677079"></path> <path d="M29.42 48.273v13.49a29.098 29.098 0 0 0 3.528-.03v-13.46z" fill="#d5e1ed" fill-rule="evenodd"></path> <path d="M23.255 42.176l6.164 7.281-8.837 2.918-.023-9.023 2.696-1.176z" fill="#d5e1ed" fill-rule="evenodd"></path> <path d="M39.192 42.176l-6.164 7.281 8.838 2.918.022-9.023-2.696-1.176z" fill="#d5e1ed" fill-rule="evenodd"></path> <path d="M24.018 45.933l5.09 1.98a2.581 2.581 0 0 1 4.05.04l5.19-2.02v7.203l-5.193-2.016a2.581 2.581 0 0 1-4.044.039l-5.093 1.977z" fill="#464449" fill-rule="evenodd"></path> <path d="M15.115 46.012l3.304-1.474v14.638a34.906 34.906 0 0 1-3.304-1.706z" fill="#8a5c42" fill-rule="evenodd"></path> <path d="M46.933 46.163l-3.304-1.625v14.527a31.278 31.278 0 0 0 3.304-1.745z" fill="#8a5c42" fill-rule="evenodd"></path> </g> </g> </g></svg>')

class Category(models.Model):
    tank = 'TA'
    heal = 'HE'
    damage_diller = 'DD'
    trader = 'TR'
    guild_master = 'GM'
    quest_giver = 'QG'
    blacksmith = 'BL'
    tanner = 'TN'
    potion_makers = 'PM'
    spell_masters = 'SM'

    events = 'EV'
    guide = 'GU'

    THEMES = [
          (tank, 'Такни'),
          (heal, 'Хилы'),
          (damage_diller, 'ДД'),
          (trader, 'Торговцы'),
          (guild_master, 'Гилдмастеры'),
          (quest_giver, 'Квестгиверы'),
          (blacksmith, 'Кузнецы'),
          (tanner, 'Кожевники'),
          (potion_makers, 'Зельевары'),
          (spell_masters, 'Мастера заклинаний'),
          (events, 'Ивент'),
          (guide, 'Гайд'),
        ]
    
    category = models.CharField(max_length = 2, choices=THEMES, unique=True)
    subscribers = models.ManyToManyField(User, through='CategorySubscriber', related_name='category_set')

    def __str__(self):
      return self.get_category_display()  

class CategorySubscriber(models.Model):
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  subscriber = models.ForeignKey(User, on_delete=models.CASCADE)

class Post(models.Model):
  author = models.ForeignKey(Author, on_delete = models.CASCADE)

  news = 'NE'
  proposal = 'PR'

  TYPE = [
    (news, 'Новость'),
    (proposal, 'Предложение')
    ]

  news_or_proposal = models.CharField(max_length= 2, default = proposal, choices=TYPE)
  time_in = models.DateTimeField(auto_now_add = True)
  category = models.ManyToManyField(Category, through = 'PostCategory')
  title = models.CharField(max_length= 255)
  text = models.TextField(default = "Текст не указан")

  image = models.ImageField()

  post_rating = models.IntegerField(default = 0)

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete= models.CASCADE)

class Reply(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.TextField(default = "Откликнулся на ваш пост")
    time_in = models.DateTimeField(auto_now_add = True)

class PostReply(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    reply = models.ForeignKey(Reply, on_delete = models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    comment = models.TextField()
    time_in = models.DateTimeField(auto_now_add = True)
    comment_rating = models.IntegerField(default = 0)

    def like(self):
      self.comment_rating += 1

    def dislike(self):
      self.comment_rating -= 1

    def rating_clear(self):
      self.comment_rating = 0

def bestUser():
    max_rating = Author.objects.latest('user_rating')
    username = max_rating.user.username
    rating = max_rating.user_rating
    print('Лучший пользователь: \n Имя - ', username, '\n Рейтинг - ', rating)

def allComments(post_name):
    comments = Comment.objects.filter(post = post_name)
    for comment in comments:
      date = comment.time_in
      user = comment.user.username
      rating = comment.comment_rating
      text = comment.comment
      print('Все коменарии к посту: ', post_name, '\n Дата создания - ', date, 
            '\n Пользователь - ', user, '\n Рейтинг -', rating, '\n Текст -', text)
    