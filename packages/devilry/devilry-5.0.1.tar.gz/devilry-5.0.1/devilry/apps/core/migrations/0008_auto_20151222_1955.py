# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_assignment_gradeform_setup_json'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='parentnode',
            field=models.ForeignKey(related_name='subjects', blank=True, to='core.Node', null=True, on_delete=models.CASCADE),
        ),
    ]
