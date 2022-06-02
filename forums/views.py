from forums import serializers
from forums.models import Post, Category, Comment, Likes
from forums.permissions import IsAuthor

from rest_framework import generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.decorators import api_view

from django_filters.rest_framework import DjangoFilterBackend


class StandartPaginationClass(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    pagination_class = StandartPaginationClass
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('owner', 'category')
    search_fields = ('name',)


@api_view(['POST'])
def like(request, pk):
    post = Post.objects.get(id=pk)
    if request.user.liked.filter(post=post).exists():
        return Response('Вы уже лайкали данный пост', status=status.HTTP_400_BAD_REQUEST)
    Likes.objects.create(post=post, user=request.user)
    return Response('Добавлено в понравившийся', status=status.HTTP_201_CREATED)


@api_view(['POST'])
def liked(request, pk):
    post = Post.objects.get(id=pk)
    if not request.user.liked.filter(post=post).exists():
        return Response('Данный пост отсутствует в списке понравившийся', status=status.HTTP_400_BAD_REQUEST)
    request.user.liked.filter(post=post).delete()
    return Response('Убрано из списка понравившийся', status=status.HTTP_204_NO_CONTENT)


class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostUpdateView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = (permissions.IsAuthenticated, IsAuthor)


class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = (permissions.IsAuthenticated, IsAuthor)


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthor, )


class RatingCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.RatingSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)