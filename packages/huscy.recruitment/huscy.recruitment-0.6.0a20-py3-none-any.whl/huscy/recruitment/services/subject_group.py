from django.db.models import F

from huscy.recruitment.models import SubjectGroup
from huscy.recruitment.services.attribute_filtersets import create_attribute_filterset


def create_subject_group(experiment, name, description):
    subject_group = SubjectGroup.objects.create(
        experiment=experiment,
        name=name,
        description=description,
        order=SubjectGroup.objects.filter(experiment=experiment).count(),
    )
    create_attribute_filterset(subject_group)
    return subject_group


def delete_subject_group(subject_group):
    experiment = subject_group.experiment
    if SubjectGroup.objects.filter(experiment=experiment).count() == 1:
        raise ValueError('Cannot delete subject group. At least one subject group must remain for '
                         'the experiment.')

    (SubjectGroup.objects.filter(experiment=experiment, order__gt=subject_group.order)
                         .update(order=F('order') - 1))
    subject_group.delete()


def get_subject_groups(experiment):
    return experiment.subject_groups.all()
