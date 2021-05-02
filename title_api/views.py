import django_filters
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets, permissions, filters

from title_api.filters import TitleFilter
from title_api.models import Review, Title, Category, Genre
from title_api.permissions import AuthorPermissions
from title_api.serializers import (
    ReviewSerializer, CommentSerializer, TitlePostSerializer,
    TitleViewSerializer, CategorySerializer, GenreSerializer)
from users_api.permissions import IsYamdbAdmin, IsYamdbModerator, YamdbReadOnly


class SuperViewSet(
    viewsets.ViewSetMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView
):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        AuthorPermissions | IsYamdbAdmin | IsYamdbModerator
    ]

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, ]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        AuthorPermissions | IsYamdbAdmin | IsYamdbModerator
    ]
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by(
        'name', 'year'
    )
    permission_classes = [
        YamdbReadOnly | IsYamdbAdmin
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleViewSerializer
        return TitlePostSerializer


class CategoryViewSet(SuperViewSet):
    permission_classes = [
        YamdbReadOnly | IsYamdbAdmin
    ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ['=name', ]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'


class GenreViewSet(SuperViewSet):
    permission_classes = [
        YamdbReadOnly | IsYamdbAdmin
    ]
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('name',)
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save()
