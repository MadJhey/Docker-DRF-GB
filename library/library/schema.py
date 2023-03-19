from authors.models import Book, Author, Task, Project
import graphene
from graphene_django import DjangoObjectType


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = '__all__'


class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = '__all__'


class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = '__all__'


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = '__all__'


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")
    all_books = graphene.List(BookType)
    all_authors = graphene.List(AuthorType)
    task_by_id = graphene.Field(TaskType, id=graphene.Int(required=True))
    task_by_project_name = graphene.List(TaskType,
                                         name=graphene.String(required=False))
    books_by_author_name = graphene.List(BookType,
                                         name=graphene.String(required=False))

    def resolve_all_books(root, info):
        return Book.objects.all()

    def resolve_all_authors(root, info):
        return Author.objects.all()

    def resolve_tasks_by_id(self, info, id):
        try:
            return Task.objects.get(id=id)
        except Task.DoesNotExist:
            return None

    def resolve_tasks_by_author_name(self, info, name=None):
        tasks = Task.objects.all()
        if name:
            tasks = tasks.filter(project__name=name)
        return tasks

    def resolve_books_by_author_name(self, info, name=None):
        books = Book.objects.all()
        if name:
            books = books.filter(author__first_name=name)
        return books


class AuthorMutation(graphene.Mutation):
    class Arguments:
        birthday_year = graphene.Int(required=True)
        id = graphene.ID()

    author = graphene.Field(AuthorType)

    @classmethod
    def mutate(cls, root, info, birthday_year, id):

        author = Author.objects.get(pk=id)
        author.birthday_year = birthday_year
        author.save()
        return AuthorMutation(author=author)


class Mutation(graphene.ObjectType):
    update_author = AuthorMutation.Field()


...
schema = graphene.Schema(query=Query, mutation=Mutation)
