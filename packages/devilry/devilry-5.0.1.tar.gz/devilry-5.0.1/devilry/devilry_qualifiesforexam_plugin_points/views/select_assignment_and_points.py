# -*- coding: utf-8 -*-


# Django imports
from django.http import HttpResponseRedirect
from django import forms

# Devilry imports
from django.utils.translation import ugettext_lazy

from devilry.devilry_qualifiesforexam.views.plugin_base_views import base_multiselect_view
from devilry.devilry_qualifiesforexam.views.plugin_base_views.base_multiselect_view import SelectedQualificationItem, \
    SelectableQualificationItemValue
from devilry.devilry_qualifiesforexam_plugin_points import resultscollector
from devilry.devilry_qualifiesforexam.views import plugin_mixin


class PluginSelectAssignmentsAndPoints(base_multiselect_view.SelectedQualificationForm):
    """
    Add extra field ``min_points_to_achieve`` to
    :class:`~.devilry.devilry_qualifiesforexam.views.plugin_base_views.base_multiselect_view.SelectedQualificationForm`
    """
    min_points_to_achieve = forms.IntegerField(
            min_value=0,
            required=False,
            help_text=ugettext_lazy(
                'If no points are given, the sum of all the qualifying assignments minimum points is needed '
                'to qualify.'),
    )


class WithPointsFormDataTargetRenderer(base_multiselect_view.QualificationItemTargetRenderer):
    """
    Add ``min_points_to_achieve`` field to target renderer.
    """
    def get_field_layout(self):
        return [
            'min_points_to_achieve'
        ]


class SelectedAssignmentItem(SelectedQualificationItem):
    def get_title(self):
        return self.value.long_name


class SelectableAssignmentItemValue(SelectableQualificationItemValue):
    selected_item_renderer_class = SelectedAssignmentItem

    def get_title(self):
        return self.value.long_name


class PluginSelectAssignmentsAndPointsView(base_multiselect_view.QualificationItemListView, plugin_mixin.PluginMixin):
    plugintypeid = 'devilry_qualifiesforexam_plugin_points.plugin_points'
    value_renderer_class = SelectableAssignmentItemValue

    def get_period_result_collector_class(self):
        return resultscollector.PeriodResultSetCollector

    def get_form_class(self):
        return PluginSelectAssignmentsAndPoints

    def get_target_renderer_class(self):
        return WithPointsFormDataTargetRenderer

    def get_pagetitle(self):
        return 'Select assignments'

    def form_valid(self, form):
        # Collect qualifying Assignment IDs
        qualifying_assignmentids = self.get_qualifying_itemids(posted_form=form)

        # Points to achieve.
        min_points_to_achieve = form.cleaned_data['min_points_to_achieve']

        collector_class = self.get_period_result_collector_class()
        passing_relatedstudentids = collector_class(
            custom_min_passing_score=min_points_to_achieve,
            period=self.request.cradmin_role,
            qualifying_assignment_ids=qualifying_assignmentids
        ).get_relatedstudents_that_qualify_for_exam()

        # Attach collected data to session.
        self.request.session['passing_relatedstudentids'] = passing_relatedstudentids
        self.request.session['plugintypeid'] = PluginSelectAssignmentsAndPointsView.plugintypeid
        return HttpResponseRedirect(str(self.request.cradmin_app.reverse_appurl('preview')))
