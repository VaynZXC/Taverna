from django.db import models
from django.contrib.auth.models import User

# Create your models here.

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
    return f'Автор #{self.pk}'

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

  news_or_proposal = models.CharField(max_length= 2, default = news, choices=TYPE)
  time_in = models.DateTimeField(auto_now_add = True)
  category = models.ManyToManyField(Category, through = 'PostCategory')
  title = models.CharField(max_length= 255)
  text = models.TextField(default = "Текст не указан")
  post_rating = models.IntegerField(default = 0)

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete= models.CASCADE)

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
    