# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20160111_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='deprecated_field_anonymous',
            field=models.BooleanField(default=False, help_text='Deprecated anonymous field. Will be removed in 3.1.', verbose_name='Anonymous? (deprectated field)', editable=False),
        ),
    ]
