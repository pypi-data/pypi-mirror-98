import pytest
from model_bakery import baker

from huscy.recruitment.models import AttributeFilterSet, SubjectGroup
from huscy.recruitment.services import create_subject_group

pytestmark = pytest.mark.django_db


def test_create_first_subject_group_for_experiment(experiment):
    subject_group = create_subject_group(experiment, 'name', 'description')

    assert subject_group.experiment == experiment
    assert subject_group.name == 'name'
    assert subject_group.description == 'description'
    assert subject_group.order == 0


def test_create_second_subject_group_for_experiment(experiment):
    baker.make('recruitment.SubjectGroup', experiment=experiment)

    subject_group = create_subject_group(experiment, 'name', 'description')

    assert subject_group.order == 1


def test_create_attribute_filterset_together_with_subject_group(experiment):
    assert not SubjectGroup.objects.exists()
    assert not AttributeFilterSet.objects.exists()

    create_subject_group(experiment, 'name', 'description')

    assert SubjectGroup.objects.filter(experiment=experiment).count() == 1
    assert AttributeFilterSet.objects.filter(subject_group__experiment=experiment).count() == 1
