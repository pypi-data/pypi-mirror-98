# -*- coding: utf-8 -*-


from django.contrib.contenttypes.models import ContentType
from django.http.response import JsonResponse, Http404
from django.utils import timezone
from django.views.generic import View
from ievv_opensource.ievv_batchframework import batchregistry
from ievv_opensource.ievv_batchframework.models import BatchOperation

from devilry.apps.core.models import ExaminerAssignmentGroupHistory, CandidateAssignmentGroupHistory
from devilry.devilry_comment.models import CommentFile
from devilry.devilry_compressionutil import models as compression_models
from devilry.devilry_group import models as group_models


class AbstractBatchCompressionAPIView(View):
    """
    Defines an API for checking the status of compressed archives.

    Returns a JsonReponse containing the status for the batchoperations that compresses archives for download,
    whether the batchoperation is not created all, created but not started, running and finished.

    Examples:
        Below are the different JSON-responses returned from subclasses of this view from GET and POST.
        If the subclasses adds more stuff, this should be documented there::
            If the ``content_object`` has no files::
                '{"status": "no-files"}'

            If the BatchOperation is NOT created::
                '{"status": "not-created"}'

            If the BatchOperation IS created, but not started::
                '{"status": "not-started"}'

            If the BatchOperation is running::
                '{"status": "running"}'

            If the BatchOperation is finished(CompressedArchiveMeta exists)::
                '{"status": "finished", "download_link": "some download link"}'

    Attributes::
        model_class: Model used, defined in subclass.

        batchoperation_type (str): This is the type of ``BatchOperation``. This must be unique for each usecase
            as there may be multiple ``BatchOperation``s running for the same model(``BatchOperation.context_object``).

        content_object: This will be a instance set in :func:`~.dispatch()` from the ``model_class``.
    """
    model_class = None
    batchoperation_type = None

    @property
    def created_by_role(self):
        return ''

    def __get_content_object(self, content_object_id):
        """
        Get the object with the ``content_object_id`` for the ``model_class`` you use.

        Args:
            content_object_id: id for model instance to get.
        """
        return self.model_class.objects.get(id=content_object_id)

    def dispatch(self, request, *args, **kwargs):
        """
        Sets ``self.content_object`` and checks if the content object has any files.
        If the content_object has no files, JsonResponse with status ``no-files`` is returned.

        Raises:
            Http404: If kwarg ``content_object_id`` is not passed.
        """
        if 'content_object_id' not in kwargs:
            raise Http404
        self.content_object = self.__get_content_object(kwargs.get('content_object_id'))

        if self.has_no_files():
            return JsonResponse({'status': 'no-files'})
        return super(AbstractBatchCompressionAPIView, self).dispatch(request, *args, **kwargs)

    def has_no_files(self):
        """
        Check if the ``self.content_object`` has any files.

        Returns:
            (bool): ``True`` if ``self.content_object`` has files associated with it, else ``False``.

        Raises:
            NotImplementedError: must be implemented by subclass.
        """
        raise NotImplementedError()

    def new_files_added(self, latest_compressed_datetime):
        """
        Check if any new files are added after the last compressed archive was created.

        Args:
            latest_compressed_datetime: Last compressed archive created datetime.

        Returns:
            bool: ``True`` if new files are added, else ``False``.
        """
        raise NotImplementedError()

    def _should_reproduce_archive(self, latest_compressed_datetime):
        """
        Check if any changes are made after the last time an compressed archive was created
        that should trigger a new compression of the files.

        Notes::
            Override this if other checks needs to be performed. Remember to return super call.

        Args:
            latest_compressed_datetime: created datetime of the latest ``CompressedArchiveMeta``.

        Returns:
            (bool): ``True`` if changes are made, else ``False``.
        """
        assignment_group_ids = self.get_assignment_group_ids()

        # Check if any changes has been made in context to examiners on the groups.
        if ExaminerAssignmentGroupHistory.objects.filter(
                assignment_group_id__in=assignment_group_ids,
                created_datetime__gt=latest_compressed_datetime).exists():
            return True

        # Check if any changes has been made in context to candidates on the groups.
        if CandidateAssignmentGroupHistory.objects.filter(
                assignment_group_id__in=assignment_group_ids,
                created_datetime__gt=latest_compressed_datetime).exists():
            return True

        # Check if a new feedbackset has been created for any of the groups.
        if group_models.FeedbackSet.objects.filter(
                group_id__in=assignment_group_ids,
                created_datetime__gt=latest_compressed_datetime).exists():
            return True

        # Check if a deadline has been moved for any of the groups.
        if group_models.FeedbackSetDeadlineHistory.objects.filter(
                feedback_set__group_id__in=assignment_group_ids,
                changed_datetime__gt=latest_compressed_datetime).exists():
            return True

        # Check if any new files are added. Implemented in subclass.
        if self.new_files_added(latest_compressed_datetime=latest_compressed_datetime):
            return True
        return False

    def start_compression_task(self, content_object_id):
        """
        Start the compression task. This function is used by POST.

        Args:
            content_object_id: Id of the object we want to compress.

        Raises:
            NotImplementedError: must be implemented by subclass.
        """
        raise NotImplementedError()

    def should_filter_by_created_by_user(self):
        """
        When checking if a compressed archive is created for the content object, should we filter on the
        user that created it?

        Why do we need this?
        We only take into account the assignment the compressed folder was made from, so if examiner_1 creates a
        compressed archive, examiner_2 will be served that compressed archive, and not the one with examiner_2s groups.

        Returns:
            bool: ``True``, if we care about who created it. ``True`` is returned by default.
        """
        return True

    def get_ready_for_download_status(self, content_object_id=None):
        """
        Override this to add the url for the download view.

        Override by adding a call to super and then add the download link to the
        entry ``download_link`` in the dictionary.

        Examples:
            Adding the downloadlink in subclass::

                def get_ready_for_download(self, content_object_id):
                    status_dict = super(BatchCompressionAPIFeedbackSetView, self).get_ready_for_download_status()
                    status_dict['download_link'] = self.request.cradmin_app.reverse_appurl(
                        viewname='feedbackset-file-download',
                        kwargs={
                            'feedbackset_id': content_object_id
                        })
                    return status_dict

        Args:
            content_object_id (int): id of the object we use as url argument for the downloadview.

        Returns:
            (dict): A dictionary with the entries ``status`` and ``download_link``
        """
        return {'status': 'finished', 'download_link': content_object_id}

    def _compressed_archive_created(self, content_object_id):
        """
        Check if an entry of :class:`~.devilry.devilry_compressionutil.models.CompressedArchiveMeta` exists.

        Args:
            content_object_id: the object referred to.

        Returns:
            (:class:`~.devilry.devilry_compressionutil.models.CompressedArchiveMeta`): instance or ``None``.
        """
        queryset = compression_models.CompressedArchiveMeta.objects \
            .filter(content_object_id=content_object_id,
                    content_type=ContentType.objects.get_for_model(model=self.content_object),
                    deleted_datetime=None)
        if self.should_filter_by_created_by_user():
            queryset = queryset.filter(created_by=self.request.user)
        return queryset.filter(created_by_role=self.created_by_role).order_by('-created_datetime').first()

    def _get_batchoperation(self):
        """
        Get the ``ievv_opensource.batchframework.BatchOperation`` object for
        the compression task. Excludes all finished ``BatchOperation``s.

        Returns:
            ``BatchOperation`` or ``None``.
        """
        queryset = BatchOperation.objects \
            .filter(context_object_id=self.content_object.id,
                    context_content_type=ContentType.objects.get_for_model(model=self.content_object),
                    operationtype=self.batchoperation_type) \
            .exclude(status=BatchOperation.STATUS_FINISHED) \
            .order_by('-created_datetime')
        if self.should_filter_by_created_by_user():
            queryset = queryset.filter(started_by=self.request.user)
        return queryset.first()

    def get_status_dict(self, context_object_id):
        """
        Checks if there exists a ``BatchOperation`` for the requested object.

        Checks the status of the ``BatchOperation`` for the requested object and builds a
        JSON-serializable dictionary with the response.

        Args:
            context_object_id: object the BatchOperation references.

        Returns:
            (dict): A JSON-serializable dictionary.
        """
        batchoperation = self._get_batchoperation()
        if not batchoperation:
            return {'status': 'not-created'}

        if batchoperation.status == BatchOperation.STATUS_UNPROCESSED:
            return {'status': 'not-started'}
        return {'status': 'running'}

    def get_response_status(self, content_object_id):
        """
        Get the built response message as a dictionary.

        Args:
            content_object_id (int): id of the object from url argument.

        Returns:
            (dict): a JSON-serializable dictionary.
        """
        return self.get_status_dict(context_object_id=content_object_id)

    def _set_archive_meta_ready_for_delete(self, compressed_archive_meta):
        """
        Sets the :attr:`~.devilry.devilry_compressionutil.CompressedArchiveMeta.deleted_datetime` and
        saves the model.

        Args:
            compressed_archive_meta: instance to update.
        """
        compressed_archive_meta.deleted_datetime = timezone.now()
        compressed_archive_meta.save()

    def get_assignment_group_ids(self):
        """
        Return a list of :class:`devilry.core.apps.models.assignment_group.AssignmentGroup` ids.
        Returns:
            list: ``AssignmentGroup`` ids.
        """
        raise NotImplementedError()

    def get(self, request, *args, **kwargs):
        """
        Expects a id of the element to download as url argument with name ``content_object_id``.

        Returns:
            (JsonResponse): Status of the compression.
        """
        content_object_id = kwargs.get('content_object_id')
        compressed_archive_meta = self._compressed_archive_created(content_object_id=content_object_id)
        if compressed_archive_meta and \
                not self._should_reproduce_archive(latest_compressed_datetime=compressed_archive_meta.created_datetime):
            return JsonResponse(self.get_ready_for_download_status(content_object_id=content_object_id))
        return JsonResponse(self.get_status_dict(context_object_id=content_object_id))

    def post(self, request, *args, **kwargs):
        """
        If no :obj:`~.devilry.devilry_compressionutil.models.CompressedArchiveMeta` exists for the
        ``content_object_id``, the compression task is started by :func:`~.start_compression_task`.

        If ``CompressedArchiveMeta`` exists for the ``content_object_id``, a check is performed to see if
        any files are added after the archive was created. If this is the case, the existing archive is marked
        for deletion, and a new compression task is started by :func:`~.start_compression_task` and the status of
        the task is returned.

        If ``CompressedArchiveMeta`` exists, and this is the latest(no changes, no new files),
        a finished status with a download-link is returned.

        Returns:
            (JsonResponse): Status of the compression.
        """
        content_object_id = self.kwargs.get('content_object_id')

        # start task or return status.
        compressed_archive_meta = self._compressed_archive_created(content_object_id=content_object_id)
        if compressed_archive_meta:
            if self._should_reproduce_archive(latest_compressed_datetime=compressed_archive_meta.created_datetime):
                self._set_archive_meta_ready_for_delete(compressed_archive_meta=compressed_archive_meta)
                self.start_compression_task(content_object_id=content_object_id)
                return JsonResponse(self.get_status_dict(context_object_id=content_object_id))
            ready_for_download_status = self.get_ready_for_download_status(content_object_id=content_object_id)
            return JsonResponse(ready_for_download_status)

        # Start compression task and return status.
        self.start_compression_task(content_object_id=content_object_id)
        return JsonResponse(self.get_status_dict(context_object_id=content_object_id))


class BatchCompressionAPIFeedbackSetView(AbstractBatchCompressionAPIView):
    """
    API for checking if a compressed ``FeedbackSet`` is ready for download.
    """
    model_class = group_models.FeedbackSet
    batchoperation_type = 'batchframework_compress_feedbackset'

    def has_no_files(self):
        return not group_models.FeedbackSet.objects\
            .filter_public_comment_files_from_students()\
            .filter(id=self.content_object.id)\
            .exists()

    def get_assignment_group_ids(self):
        return [self.content_object.group.id]

    def new_files_added(self, latest_compressed_datetime):
        group_comment_ids = group_models.GroupComment.objects \
            .filter(feedback_set=self.content_object).values_list('id', flat=True)
        if CommentFile.objects.filter(
                comment_id__in=group_comment_ids, created_datetime__gt=latest_compressed_datetime
        ).exists():
            return True

    def get_ready_for_download_status(self, content_object_id=None):
        status_dict = super(BatchCompressionAPIFeedbackSetView, self).get_ready_for_download_status()
        status_dict['download_link'] = self.request.cradmin_app.reverse_appurl(
            viewname='feedbackset-file-download',
            kwargs={
                'feedbackset_id': content_object_id
            })
        return status_dict

    def should_filter_by_created_by_user(self):
        return False

    def start_compression_task(self, content_object_id):
        batchregistry.Registry.get_instance().run(
            actiongroup_name=self.batchoperation_type,
            context_object=self.content_object,
            operationtype=self.batchoperation_type,
            started_by=self.request.user
        )
