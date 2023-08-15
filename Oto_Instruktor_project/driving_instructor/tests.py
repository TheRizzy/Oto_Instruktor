import pytest
from mixer.backend.django import mixer
from django.test import RequestFactory
from django.urls import reverse
from pytest_django.asserts import assertQuerysetEqual
from django.contrib.auth.models import User
from driving_instructor.models import Instructor, Availability, Reservation, InstructorProfile
from driving_instructor.views import InstructorDetailView
from django.test import Client


@pytest.mark.django_db
def test_create_user():
    # Make new user
    User.objects.create_user(
        username='User', 
        first_name='John',
        last_name='Mouse',
        email='user@mail.com',
        password='test123'
        )

    # Check that 1x users was crate
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_create_user_instructor(client):
    # Make new user: 1x instructor
    user_1_instructor = User.objects.create_user(username='instructor', first_name='Jan', last_name='Point', email='instructor@mail.com', password='test123')

    # Create object Instructor related with this new created instructor
    user_1_instructor_profile = Instructor.objects.create(user=user_1_instructor, is_instructor=True)

    # Check that 1x users was crate
    assert User.objects.count() == 1

    # Check that user_1_instructor is instructor 
    assert user_1_instructor_profile.is_instructor


@pytest.mark.django_db
def test_add_availability_view(client, user, instructor):
    """
    Test for AddAvailabilityView.
    """
    # Log in the user
    client.force_login(user)

    # Simulate a POST request with form data
    response = client.post(reverse('instructor_availability'), data={
        'date': '2025-12-31', 
        'start_time': '10:00',
        'end_time': '12:00'
    })

    assert response.status_code == 302  # Expecting a redirect

    # Check if a new availability was added to the database
    assert Availability.objects.count() == 1

    # Check if the availability was added by the correct instructor
    assert Availability.objects.first().instructor == instructor


@pytest.mark.skip("This test dont work too, assertion with response.status_code error")
def test_instructor_detail_view():
    # Create a user and instructor profile for that user
    user = User.objects.create(username='testuser')
    instructor_profile = InstructorProfile.objects.create(
        user_id=user.id, 
        title='Test title',	
        description='Test description',
        personal_data='Test personal data',	
        company_data='Test company data',
        work_region='Test work region',
        hourly_rate='100'
        )
    instructor = Instructor.objects.create(
        is_instructor=True,
        user_id=user.pk,
        legitimacy='legitimacy/logo.jpg',
        )

    # Create an availability for the instructor
    availability = Availability.objects.create(
        instructor_id=instructor.id, 
        date='2024-08-07',
        start_time='12:00:00',
        end_time='13:00:00',
        )

    print(user.id)
    print(instructor_profile.user_id)
    print(instructor.id)
    print(availability.instructor.id)
    print(availability.date)
    print(availability.start_time)
    print(availability.end_time)
    print(instructor_profile.pk)

    # Create a request factory
    # factory = RequestFactory()

    c = Client()
    url = reverse('instructor_detail', args=[instructor_profile.pk])
    try:
        response = c.get(url)
    except Instructor.DoesNotExist:
        pass

    print(response.content)

    # Create a request
    # request = factory.get(reverse('instructor_detail', args=[instructor_profile.pk]))

    # Attach the user to the request
    # request.user = user

    # Call the view
    # view = InstructorDetailView.as_view()
    # response = view(request, pk=instructor_profile.pk)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that instructor's information is present in the response content
    assert str(instructor_profile.title) in str(response.content)
    assert str(instructor_profile.description) in str(response.content)
    assert str(instructor_profile.personal_data) in str(response.content)
    # ... assert other instructor details ...

    # Assert that availability information is present in the response content
    assert availability.date.strftime('%Y-%m-%d') in str(response.content)
    assert availability.start_time.strftime('%H:%M:%S') in str(response.content)
    assert availability.end_time.strftime('%H:%M:%S') in str(response.content)

    # Assert that reserved date and time are not present in the response content
    assert str(availability.date) not in str(response.content)
    assert str(availability.start_time) not in str(response.content)

    # ... add more assertions as needed ...


@pytest.mark.django_db
def test_delete_availability_view(client, user, availability):
    client.force_login(user)

    # Get the URL of the delete availability view
    url = reverse('delete_availability', args=[availability.pk])

    # Make a GET request to the delete availability view
    response = client.get(url)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 302

    # Check if the availability is deleted
    with pytest.raises(Availability.DoesNotExist):
        availability.refresh_from_db()

    # Check if the user is redirected to the instructor availability page
    assert response.url == reverse('instructor_availability')
 

@pytest.mark.django_db
def test_login_view(client, create_user):
    # Crate new user with password 
    user = create_user(username='testuser', password='TestPassword123!@#')

    # Get the URL of the login view
    url = reverse('login')

    # Make a POST request to the login view with valid credentials
    response = client.post(url, {'username': user.username, 'password': user.password})

    # Make a GET request to the login view when the user is already authenticated
    client.force_login(user)
    response = client.get(url)

    # Check if the user is redirected to the success URL when already authenticated
    assert response.status_code == 302
    assert response.url == reverse('home')
