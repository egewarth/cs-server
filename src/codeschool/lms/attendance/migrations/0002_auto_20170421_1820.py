# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-21 18:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0032_add_bulk_delete_page_permission'),
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendancePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE,
                                                  parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='AttendanceSheetChild',
            fields=[
                ('attendancesheet_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE,
                                                             parent_link=True, primary_key=True, serialize=False, to='attendance.AttendanceSheet')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE,
                                                         related_name='attendance_sheet_single_list', to='attendance.AttendancePage')),
            ],
            bases=('attendance.attendancesheet',),
        ),
        migrations.AlterField(
            model_name='attendancesheet',
            name='expiration_minutes',
            field=models.SmallIntegerField(
                default=5, help_text='Time (in minutes) before attendance session expires.', verbose_name='Expiration time'),
        ),
        migrations.AlterField(
            model_name='attendancesheet',
            name='max_attempts',
            field=models.SmallIntegerField(
                default=3, help_text='How many times a student can attempt to prove attendance. A maximum is necessary to avoid a brute force attack.', verbose_name='Maximum number of attempts'),
        ),
        migrations.AlterField(
            model_name='attendancesheet',
            name='max_string_distance',
            field=models.SmallIntegerField(
                default=1, help_text='Maximum number of wrong characters that is considered acceptable when comparing the expected passphrase with the one given by thestudent.', verbose_name='Fuzzyness'),
        ),
    ]