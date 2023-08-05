from itertools import cycle

import pytest
from model_bakery import baker

from huscy.recruitment.models import SubjectGroup
from huscy.recruitment.services import delete_subject_group

pytestmark = pytest.mark.django_db


def test_experiment_has_only_one_subject_group(subject_group):
    assert SubjectGroup.objects.count() == 1

    with pytest.raises(ValueError) as e:
        delete_subject_group(subject_group)

    assert str(e.value) == ('Cannot delete subject group. At least one subject group must remain '
                            'for the experiment.')


def test_experiment_has_multiple_subject_groups(experiment):
    subject_groups = baker.make(SubjectGroup, experiment=experiment, _quantity=2)

    delete_subject_group(subject_groups[1])

    assert SubjectGroup.objects.count() == 1


def test_decrementing_order_of_remaining_subject_groups(experiment):
    subject_groups = baker.make(SubjectGroup, experiment=experiment, order=cycle([0, 1, 2, 3, 4]),
                                _quantity=5)

    delete_subject_group(subject_groups[1])

    assert [0, 1, 2, 3] == list(SubjectGroup.objects.order_by('order')
                                                    .values_list('order', flat=True))
