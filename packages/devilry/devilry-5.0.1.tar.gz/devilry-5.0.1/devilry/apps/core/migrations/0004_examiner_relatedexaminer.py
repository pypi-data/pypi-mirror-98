# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150917_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='examiner',
            name='relatedexaminer',
            field=models.ForeignKey(default=None, blank=True, to='core.RelatedExaminer', null=True, on_delete=models.CASCADE),
        ),
    ]
