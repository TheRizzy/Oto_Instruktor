import pytest
from django.test import Client

@pytest.fixture
def client():
    """
    Fixture to crate instance of fake browser,  which can be used like a parameter in tests.py
    """
    client = Client()
    return client
