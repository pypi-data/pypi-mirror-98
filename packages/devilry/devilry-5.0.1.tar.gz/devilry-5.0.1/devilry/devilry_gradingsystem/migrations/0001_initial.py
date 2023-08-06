# -*- coding: utf-8 -*-


from django.db import models, migrations
from django.conf import settings
import devilry.devilry_gradingsystem.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedbackDraft',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feedbacktext_editor', models.CharField(default='devilry-markdown', max_length='20', choices=[('devilry-markdown', 'Markdown editor'), ('wysiwyg-html', 'WYSIWYG html')])),
                ('feedbacktext_raw', models.TextField(null=True, blank=True)),
                ('feedbacktext_html', models.TextField(null=True, blank=True)),
                ('points', models.PositiveIntegerField()),
                ('published', models.BooleanField(default=False, help_text='Has this draft been published as a StaticFeedback? Setting this to true on create automatically creates a StaticFeedback.')),
                ('save_timestamp', models.DateTimeField(help_text='Time when this feedback was saved. Since FeedbackDraft is immutable, this never changes.')),
                ('delivery', models.ForeignKey(related_name='devilry_gradingsystem_feedbackdraft_set', to='core.Delivery', on_delete=models.CASCADE)),
                ('saved_by', models.ForeignKey(related_name='devilry_gradingsystem_feedbackdraft_set', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
                ('staticfeedback', models.OneToOneField(related_name='devilry_gradingsystem_feedbackdraft_set', null=True, blank=True, to='core.StaticFeedback', help_text='The StaticFeedback where this was published if this draft has been published.', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ['-save_timestamp'],
            },
        ),
        migrations.CreateModel(
            name='FeedbackDraftFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.TextField()),
                ('file', models.FileField(upload_to=devilry.devilry_gradingsystem.models.feedback_draft_file_upload_to)),
                ('delivery', models.ForeignKey(related_name='+', to='core.Delivery', on_delete=models.CASCADE)),
                ('saved_by', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ['filename'],
            },
        ),
    ]
