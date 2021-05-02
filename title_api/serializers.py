from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from title_api.models import Review, Comment, Title, Category, Genre


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов"""
    title = serializers.StringRelatedField()
    author = serializers.StringRelatedField()

    def validate(self, data):
        request = self.context.get('request')
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method != "PATCH" and Review.objects.filter(
                author=request.user, title=title).exists():
            raise serializers.ValidationError(
                'Validation error. Review object with current author'
                'and title already exists!')
        return data

    class Meta:
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date',)
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев"""
    author = serializers.StringRelatedField()

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий"""
    class Meta:
        model = Category
        exclude = ['id']
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров"""
    class Meta:
        model = Genre
        exclude = ['id']
        lookup_field = 'slug'


class TitleViewSerializer(serializers.ModelSerializer):
    """Сериализатор вывода списка произведений"""
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.FloatField()

    class Meta:
        fields = '__all__'
        model = Title


class TitlePostSerializer(serializers.ModelSerializer):
    """Сериализатор создания произведений"""
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )

    class Meta:
        fields = '__all__'
        model = Title
