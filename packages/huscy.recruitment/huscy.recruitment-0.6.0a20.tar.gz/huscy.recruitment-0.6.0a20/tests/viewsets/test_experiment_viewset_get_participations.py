import pytest

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

pytestmark = pytest.mark.django_db


def test_admin_user_can_retrieve_participations(admin_client, experiment):
    response = retrieve_participations(admin_client, experiment)
    assert response.status_code == HTTP_200_OK


def test_user_without_permission_can_retrieve_participations(client, experiment):
    response = retrieve_participations(client, experiment)
    assert response.status_code == HTTP_200_OK


def test_anonymous_user_cannot_retrieve_participations(anonymous_client, experiment):
    response = retrieve_participations(anonymous_client, experiment)
    assert response.status_code == HTTP_403_FORBIDDEN


def retrieve_participations(client, experiment):
    return client.get(reverse('experiment-participations', kwargs=dict(pk=experiment.pk)))
