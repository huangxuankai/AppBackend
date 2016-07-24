# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appUser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAvatar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_avatar', models.ImageField(upload_to=b'avatar')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
