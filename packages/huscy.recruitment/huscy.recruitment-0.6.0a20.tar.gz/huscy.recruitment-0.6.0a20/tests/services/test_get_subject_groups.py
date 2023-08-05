import pytest
from model_bakery import baker

from huscy.recruitment.services import get_subject_groups

pytestmark = pytest.mark.django_db


def test_with_no_groups(experiment):
    result = get_subject_groups(experiment)

    assert [] == list(result)


def test_with_one_group(experiment):
    subject_group = baker.make('recruitment.SubjectGroup', experiment=experiment)

    result = get_subject_groups(experiment)

    assert [subject_group] == list(result)


def test_with_multiple_groups(experiment):
    def sort_function(item):
        return getattr(item, 'id')

    subject_groups = baker.make('recruitment.SubjectGroup', experiment=experiment, _quantity=3)

    result = get_subject_groups(experiment)

    assert sorted(subject_groups, key=sort_function) == sorted(result, key=sort_function)
