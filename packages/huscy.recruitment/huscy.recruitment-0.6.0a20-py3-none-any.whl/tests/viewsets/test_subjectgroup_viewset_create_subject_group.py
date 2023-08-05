import pytest

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN

from huscy.recruitment import models

pytestmark = pytest.mark.django_db


def test_admin_user_can_create_subject_group(admin_client, experiment):
    response = create_subject_group(admin_client, experiment)

    assert response.status_code == HTTP_201_CREATED


def test_user_without_permission_can_create_subject_group(client, experiment):
    response = create_subject_group(client, experiment)

    assert response.status_code == HTTP_201_CREATED


def test_anonymous_user_cannot_create_subject_group(anonymous_client, experiment):
    response = create_subject_group(anonymous_client, experiment)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_attribute_filterset_created(client, experiment):
    assert not models.SubjectGroup.objects.exists()
    assert not models.AttributeFilterSet.objects.exists()

    create_subject_group(client, experiment)

    assert models.SubjectGroup.objects.exists()
    assert models.AttributeFilterSet.objects.exists()


def create_subject_group(client, experiment):
    return client.post(
        reverse('subjectgroup-list', kwargs=dict(experiment_pk=experiment.pk)),
        data=dict(
            description='description',
            name='name',
        )
    )
