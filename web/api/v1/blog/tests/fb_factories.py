import factory

from blog.models import Article, Category, Comment
from main.models import User


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('sentence', nb_words = 3)

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')

class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    category = factory.SubFactory(CategoryFactory)
    title = factory.Faker('sentence', nb_words = 7)
    content = factory.Faker('text')
    author = factory.SubFactory(UserFactory)

class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    user = factory.SubFactory(UserFactory)
    content = factory.Faker("text", max_nb_chars=190)
    article = factory.SubFactory(ArticleFactory)
