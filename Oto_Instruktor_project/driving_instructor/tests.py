from django.test import Client
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from pytest_django.asserts import assertQuerysetEqual

@pytest.mark.django_db
def test_create_users(client):
    # Make new users: 1x instructors and 1x default users
    instructor = User.objects.create_user(username='instructor', email='instructor@mail.com', password='test123', is_instructor=True)
    default_user = User.objects.create_user(username='default_user', email='default.user@mail.com', password='test123', is_instructor=False)

    # Check that 2x users was crate
    assert User.objects.count() == 2

    # Check that users is instructor and default user
    assert instructor.instructor.is_instructor #or instructor.is_instructor
    assert not default_user.instructor.is_instructor # or default_user.is_instructor 

    # Check that list property shows on main page (home)
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200
    assertQuerysetEqual(
        response.context['instructor'],
        [repr(instructor)],
        transform=repr
    )

