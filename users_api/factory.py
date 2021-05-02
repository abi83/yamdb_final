import factory
from django.utils.text import slugify
from factory import fuzzy
from faker import Faker

from users_api.models import YamdbUser


class YamdbUserFactory(factory.Factory):
    class Meta:
        model = YamdbUser

    @factory.lazy_attribute
    def bio(self):
        fake = Faker(locale='en-US')
        return fake.paragraph(nb_sentences=3)

    @factory.lazy_attribute
    def first_name(self):
        fake = Faker(locale='en-US')
        return fake.first_name()

    @factory.lazy_attribute
    def last_name(self):
        fake = Faker(locale='en-US')
        return fake.last_name()

    @factory.lazy_attribute
    def email(self):
        return slugify(self.username) + '@fake.fake'

    username = factory.Sequence(lambda n: f'fake_user_{n}')
    role = fuzzy.FuzzyChoice(
        YamdbUser.Role.choices,
        getter=lambda c: c[0]
    )
