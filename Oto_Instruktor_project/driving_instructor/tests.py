from django.test import Client
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from pytest_django.asserts import assertQuerysetEqual
from driving_instructor.models import Instructor

@pytest.mark.django_db
def test_create_user_instructor(client):
    # Make new user: 1x instructor
    user_1_instructor = User.objects.create_user(username='instructor', first_name='Jan', last_name='Point', email='instructor@mail.com', password='test123')

    # Create object Instructor related with this new created instructor
    user_1_instructor_profile = Instructor.objects.create(user=user_1_instructor, is_instructor=True)

    # Check that 2x users was crate
    assert User.objects.count() == 2

    # Check that user_1_instructor is instructor 
    assert user_1_instructor_profile.is_instructor 

    # Check that list property shows on main page (home)
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200
    assertQuerysetEqual(
        response.context['instructors'],
        [repr(user_1_instructor)],
        transform=repr
    )

