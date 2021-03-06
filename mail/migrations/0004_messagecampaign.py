# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-04 21:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
        ('mail', '0003_auto_20170531_1253'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageCampaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Campanha')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mail.Message')),
            ],
        ),
    ]
