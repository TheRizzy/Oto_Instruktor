import pytest
from django.test import Client
from django.contrib.auth.models import User
from mixer.backend.django import Mixer


@pytest.fixture
def client():
    """
    Fixture to crate instance of fake browser,  which can be used like a parameter in tests.py
    """
    client = Client()
    return client


@pytest.fixture
def mixer():
    """
    Fixture to crate instance of Mixer form framework mixer, to create sample of data.
    """
    return Mixer()

@pytest.fixture
def user(django_user_model, mixer):
    """
    Fixture to create a fake default user.
    """
    return mixer.blend(django_user_model)


@pytest.fixture
def create_user(django_user_model):
    def make_user(**kwargs):
        return django_user_model.objects.create_user(**kwargs)
    return make_user


@pytest.fixture
def instructor(mixer, user):
    """
    Fixture to create a fake instructor.
    """
    return mixer.blend('driving_instructor.Instructor', user=user)


@pytest.fixture
def availability(mixer, instructor):
    """
    Fixture to create a fake instructor.
    """
    return mixer.blend('driving_instructor.Availability', instructor=instructor)

