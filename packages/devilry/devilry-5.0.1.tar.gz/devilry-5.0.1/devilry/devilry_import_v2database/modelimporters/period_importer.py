import pprint

from django.contrib.auth import get_user_model

from devilry.apps.core.models import Subject, Period
from devilry.devilry_account import models as account_models
from devilry.devilry_import_v2database import modelimporter


class PeriodImporter(modelimporter.ModelImporter):
    def get_model_class(self):
        return Period

    def _create_permissiongroup_user(self, permission_group, user):
        if not permission_group.users.filter(id=user.id).exists():
            permission_group_user, created = account_models.PermissionGroupUser.objects.get_or_create(
                permissiongroup=permission_group,
                user=user)
            if self.should_clean():
                permission_group_user.full_clean()
            permission_group_user.save()
            return permission_group_user

    def _create_permissiongroup(self, subject, admin_user_ids):
        # NOTE: We create a subjectadmin permissiongroup for
        # period admins since the permission logic changes
        # in 3.x makes this the most natural transition.
        permission_group, created = account_models.PermissionGroup.objects.create_or_update_syncsystem_permissiongroup(
            basenode=subject,
            grouptype=account_models.PermissionGroup.GROUPTYPE_SUBJECTADMIN)

        admin_users_queryset = get_user_model().objects.filter(id__in=admin_user_ids)
        for admin_user in admin_users_queryset.all():
            self._create_permissiongroup_user(permission_group, admin_user)
        return permission_group

    def _create_subject_permissiongroup(self, subject, admin_user_ids):
        """
        User that where admins on ``Period`` are now set as subject-admins.
        """
        if len(admin_user_ids) > 0:
            self._create_permissiongroup(
                subject=subject,
                admin_user_ids=admin_user_ids)

    def _get_subject_from_parentnode_id(self, id):
        try:
            subject = Subject.objects.get(id=id)
        except Subject.DoesNotExist:
            raise modelimporter.ModelImporterException('No Subject with id={} exists for imported Period'.format(id))
        return subject

    def _create_period_from_object_dict(self, object_dict):
        period = self.get_model_class()()
        self.patch_model_from_object_dict(
            model_object=period,
            object_dict=object_dict,
            attributes=[
                'pk',
                'long_name',
                'short_name',
                'start_time',
                'end_time',
            ]
        )
        subject = self._get_subject_from_parentnode_id(id=object_dict['fields']['parentnode'])
        period.parentnode = subject
        if self.should_clean():
            period.full_clean()
        period.save()
        self._create_subject_permissiongroup(subject=subject, admin_user_ids=object_dict['admin_user_ids'])
        self.log_create(model_object=period, data=object_dict)

    def import_models(self, fake=False):
        directory_parser = self.v2period_directoryparser
        directory_parser.set_max_id_for_models_with_auto_generated_sequence_numbers(model_class=self.get_model_class())
        for object_dict in directory_parser.iterate_object_dicts():
            if fake:
                print(('Would import: {}'.format(pprint.pformat(object_dict))))
            else:
                self._create_period_from_object_dict(object_dict=object_dict)

