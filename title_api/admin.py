from django.contrib import admin
from django.db.models import Avg

from title_api.models import Category, Genre, Title, Review, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', )
    search_fields = ('name', )
    list_display_links = ('pk', 'name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', )
    search_fields = ('text', )
    list_display_links = ('pk', )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'pub_date', )
    search_fields = ('name', )
    list_display_links = ('pk', )
    list_filter = ('author', 'pub_date')
    date_hierarchy = 'pub_date'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'pub_date', 'score')
    search_fields = ('text', )
    list_filter = ('author', 'title', 'pub_date')
    empty_value_display = '-not filled-'
    list_display_links = ('pk', )
    date_hierarchy = 'pub_date'
    fields = ('author', 'title', 'pub_date', 'score', 'text',)


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'rating',)
    search_fields = ('name', 'description', )
    list_filter = ('genre', 'category', 'year')
    empty_value_display = '-not filled-'
    list_display_links = ('pk', 'name',)
    fields = ('name', 'year', 'genre', 'category', 'description',)
    inlines = [ReviewInline, ]

    def get_queryset(self, request):
        return Title.objects.annotate(
            rating=Avg('reviews__score')
        )

    def rating(self, obj):
        return obj.rating
