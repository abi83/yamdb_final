from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.timezone import now

from title_api.utils import year_validator

User = get_user_model()


class Category(models.Model):
    """
    Title's category
    """
    name = models.CharField(
        max_length=200, unique=True,
        verbose_name='Category name'
    )

    slug = models.CharField(
        max_length=200, unique=True,
        blank=True, null=True,
        verbose_name='Category slug'
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    """
    Title's genres
    """
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    Work of fiction: film, book or music album:
    """
    name = models.TextField(
        max_length=100, db_index=True
    )

    year = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Year',
        validators=[year_validator]
    )
    description = models.TextField(
        max_length=500,
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['name', 'year']
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'

    def __str__(self):
        return self.name


class Review(models.Model):
    """
    Title's reviews with rating score
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    pub_date = models.DateTimeField('Publication date', default=now)
    score = models.IntegerField(
        blank=True,
        validators=[
            MaxValueValidator(10, 'Can\'t be more than 10'),
            MinValueValidator(1, 'Can\'t be less than 1')
        ]
    )
    text = models.TextField()
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        null=False,
        related_name='reviews'
    )

    class Meta:
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique_review_title_author')
        ]


class Comment(models.Model):
    """
    Review comments
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    review = models.ForeignKey(
        Review,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='comments',
        unique=False
    )
    text = models.TextField()
    pub_date = models.DateTimeField('Publication date', default=now)

    class Meta:
        ordering = ['author']
