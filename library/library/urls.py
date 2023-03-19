
from django.contrib import admin
from django.urls import path, include, re_path
from authors.views import AuthorModelViewSet, BookModelViewSet, BiographyModelViewSet, ArticleModelViewSet, ProjectModelViewSet, TaskModelViewSet, MyAPIView
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from userapp.views import UserListAPIView
from rest_framework.permissions import AllowAny
from graphene_django.views import GraphQLView


router = DefaultRouter()
router.register(r'authors', AuthorModelViewSet)
router.register(r'books', BookModelViewSet)
router.register(r'biography', BiographyModelViewSet)
router.register(r'article', ArticleModelViewSet)

myrouter = DefaultRouter()
myrouter.register(r'project', ProjectModelViewSet)
myrouter.register(r'task', TaskModelViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Library",
        default_version='0.1',
        description="Documentation to out project",
        contact=openapi.Contact(email="admin@admin.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('api/', include(router.urls)),
    # path('myapi/', MyAPIView.as_view()),
    path('myapi/', include(myrouter.urls)),
    path('myproject/', ProjectModelViewSet.as_view({'get': 'list'})),
    path('api-token-auth/', views.obtain_auth_token),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # re_path(r'^api/(?P<version>\d\.\d)/users/$', UserListAPIView.as_view()),
    path('api/users/0.1', include('userapp.urls', namespace='0.1')),
    path('api/users/0.2', include('userapp.urls', namespace='0.2')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
    path("graphql/", GraphQLView.as_view(graphiql=True))

]
