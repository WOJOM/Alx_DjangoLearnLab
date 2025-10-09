from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD for posts. List & retrieve are public. Create/update/delete requires auth and ownership.
    Supports filtering, searching and ordering.
    """
    queryset = Post.objects.select_related('author').prefetch_related('comments').all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author__id']  # optionally filter by author id
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # Extra action to list comments for a post (alternate to nested data)
    @action(detail=True, methods=['get'], url_path='comments', permission_classes=[permissions.AllowAny])
    def list_comments(self, request, pk=None):
        post = self.get_object()
        comments_qs = post.comments.all()
        page = self.paginate_queryset(comments_qs)
        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CommentSerializer(comments_qs, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD for comments. List & retrieve public. Create requires auth.
    Only comment author or staff can update/delete.
    """
    queryset = Comment.objects.select_related('author', 'post').all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['post__id', 'author__id']
    search_fields = ['content']
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def perform_create(self, serializer):
        # ensure author is set to current user
        serializer.save(author=self.request.user)
