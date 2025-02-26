import factory

from blog.models import Article, Category
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
