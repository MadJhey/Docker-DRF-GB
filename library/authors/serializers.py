# from .models import Users
from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer
from .models import Author, Biography, Book, Article, Project, Task


class AuthorModelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
        # exclude = ['id']


class BiographyModelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Biography
        fields = '__all__'


class BookModelSerializer(ModelSerializer):
    # author = AuthorModelSerializer(many=True)

    class Meta:
        model = Book
        fields = '__all__'


class ArticleModelSerializer(HyperlinkedModelSerializer):
    author = AuthorModelSerializer()

    class Meta:
        model = Article
        fields = '__all__'


class ProjectModelSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'


class TaskModelSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'
