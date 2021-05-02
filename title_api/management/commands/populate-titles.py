import random

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from title_api.factory import (
    CategoryFactory, GenreFactory, TitleFactory,
    ReviewFactory, CommentsFactory)
from title_api.models import Genre, Category, Title, Review
from users_api.models import YamdbUser


class Command(BaseCommand):
    help = 'Creat some categories and genres, "number" titles, (default=10)' \
           'number*3 reviews and number*12 comments'

    CATEGORIES = 10
    GENRES = 20
    TITLES = 10

    def add_arguments(self, parser):
        parser.add_argument('number', nargs='?', type=int, default=self.TITLES)

    def show_progress(self, progress, instance_name):
        width = 40
        points = int(width * progress)
        backspaces = width - points
        bar = ('[' + '.' * points + ' ' * backspaces + '] '
               + str(int(progress * 100)) + ' %')
        text = f'Populating {instance_name} '.ljust(25)
        self.stdout.write(
            self.style.SUCCESS(text + bar),
            ending='\r'
        )

    def report_success(self, number, instance_name):
        self.stdout.write(' ' * 100, ending='\r')
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {number} {instance_name}'
            ))

    def populate_categories(self, number):
        try:
            CategoryFactory.create_batch(number)
            self.report_success(number, 'Categories')
        except IntegrityError:
            self.stdout.write(
                self.style.WARNING('Categories already exists. Skipping'))

    def populate_genres(self, number):
        try:
            GenreFactory.create_batch(number)
            self.report_success(number, 'Genres')
        except IntegrityError:
            self.stdout.write(
                self.style.WARNING('Genres already exists. Skipping'))

    def populate_titles(self, number):
        genres = Genre.objects.all()
        categories = Category.objects.all()
        for i in range(number):
            self.show_progress(i / number, 'Titles')
            category = random.choice(categories)
            TitleFactory.create(genre=genres, category=category)
        self.report_success(number, 'Titles')

    def populate_reviews(self, number):
        titles = Title.objects.all()
        authors = YamdbUser.objects.all()
        i = 0
        while i < number:
            self.show_progress(i / number, 'Reviews')
            title = random.choice(titles)
            author = random.choice(authors)
            try:
                ReviewFactory.create(
                    title=title,
                    author=author
                )
                i += 1
            except IntegrityError:
                # UniqueConstraint set ['title','author']
                pass
        self.report_success(number, 'Reviews')

    def populate_comments(self, number):
        authors = YamdbUser.objects.all()
        reviews = Review.objects.all()
        for i in range(number):
            self.show_progress(i / number, 'Comments')
            review = random.choice(reviews)
            author = random.choice(authors)
            CommentsFactory.create(author=author, review=review)
        self.report_success(number, 'Comments')

    def handle(self, *args, **options):
        number = options['number']
        self.populate_categories(self.CATEGORIES)
        self.populate_genres(self.GENRES)
        self.populate_titles(number)
        self.populate_reviews(number * 3)
        self.populate_comments(number * 12)
