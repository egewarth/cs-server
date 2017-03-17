# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-16 19:51
from __future__ import unicode_literals

import codeschool.questions.coding_io.models.validators
import codeschool.questions.models
import codeschool.vendor.wagtailmarkdown.blocks
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import modelcluster.fields
import uuid
import wagtail.contrib.wagtailroutablepage.models
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0002_initial_formats'),
        ('wagtailcore', '0032_add_bulk_delete_page_permission'),
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.TextField(blank=True, help_text='Source code for the correct answer in the given programming language.', verbose_name='answer source code')),
                ('placeholder', models.TextField(blank=True, help_text='This optional field controls which code should be placed in the source code editor when a question is opened. This is useful to put boilerplate or even a full program that the student should modify. It is possible to configure a global per-language boilerplate and leave this field blank.', verbose_name='placeholder source code')),
                ('source_hash', models.CharField(default='d41d8cd98f00b204e9800998ecf8427e', help_text='Hash computed from the reference source', max_length=32)),
                ('error_message', models.TextField(blank=True, help_text='If an error is found on post-validation, an error message is stored in here.', verbose_name='error message')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.ProgrammingLanguage')),
            ],
            options={
                'verbose_name': 'answer key',
                'verbose_name_plural': 'answer keys',
            },
        ),
        migrations.CreateModel(
            name='CodingIoFeedback',
            fields=[
                ('feedback_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='activities.Feedback')),
                ('for_pre_test', models.BooleanField(default=False, help_text='True if its grading in the pre-test phase.', verbose_name='Grading pre-test?')),
                ('json_feedback', jsonfield.fields.JSONField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(codeschool.questions.models.QuestionMixin, 'activities.feedback'),
        ),
        migrations.CreateModel(
            name='CodingIoProgress',
            fields=[
                ('progress_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='activities.Progress')),
            ],
            options={
                'abstract': False,
            },
            bases=(codeschool.questions.models.QuestionMixin, 'activities.progress'),
        ),
        migrations.CreateModel(
            name='CodingIoQuestion',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('short_description', models.CharField(help_text='A short textual description to be used in titles, lists, etc.', max_length=140, verbose_name='short description')),
                ('author_name', models.CharField(blank=True, help_text="The author's name, if not the same user as the question owner.", max_length=100, verbose_name="Author's name")),
                ('visible', models.BooleanField(default=bool, help_text='Makes activity invisible to users.', verbose_name='Invisible')),
                ('closed', models.BooleanField(default=bool, help_text='A closed activity does not accept new submissions, but users can see that they still exist.', verbose_name='Closed to submissions')),
                ('group_submission', models.BooleanField(default=bool, help_text='If enabled, submissions are registered to groups instead of individual students.', verbose_name='Group submissions')),
                ('max_group_size', models.IntegerField(default=6, help_text='If group submission is enabled, define the maximum size of a group.', verbose_name='Maximum group size')),
                ('disabled', models.BooleanField(default=bool, help_text='Activities can be automatically disabled when Codeshool encounters an error. This usually produces a message saved on the .disabled_message attribute.', verbose_name='Disabled')),
                ('disabled_message', models.TextField(blank=True)),
                ('has_submissions', models.BooleanField(default=bool)),
                ('has_correct_submissions', models.BooleanField(default=bool)),
                ('body', wagtail.wagtailcore.fields.StreamField((('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('heading', wagtail.wagtailcore.blocks.CharBlock(classname='full title')), ('markdown', codeschool.vendor.wagtailmarkdown.blocks.MarkdownBlock()), ('html', wagtail.wagtailcore.blocks.RawHTMLBlock())), blank=True, help_text='Describe what the question is asking and how should the students answer it as clearly as possible. Good questions should not be ambiguous.', null=True, verbose_name='Question description')),
                ('comments', wagtail.wagtailcore.fields.RichTextField(blank=True, help_text='(Optional) Any private information that you want to associate to the question page.', verbose_name='Comments')),
                ('import_file', models.FileField(blank=True, help_text='Fill missing fields from question file. You can safely leave this blank and manually insert all question fields.', null=True, upload_to='question-imports', verbose_name='import question')),
                ('num_pre_tests', models.PositiveIntegerField(default=3, help_text='The desired number of test cases that will be computed after comparing the iospec template with the correct answer. This is only a suggested value and will only be applied if the response template uses input commands to generate random input.', validators=[codeschool.questions.coding_io.models.validators.positive_integer_validator], verbose_name='# of pre-test examples')),
                ('pre_tests_source', models.TextField(blank=True, help_text='Template used to grade I/O responses. See http://pythonhosted.org/iospec for a complete reference on the template format.', validators=[codeschool.questions.coding_io.models.validators.iospec_source_validator], verbose_name='response template')),
                ('num_post_tests', models.PositiveIntegerField(default=20, validators=[codeschool.questions.coding_io.models.validators.positive_integer_validator], verbose_name='# of post-test examples')),
                ('post_tests_source', models.TextField(blank=True, help_text='These tests are used only in a second round of corrections and is not immediately shown to users.', validators=[codeschool.questions.coding_io.models.validators.iospec_source_validator], verbose_name='response template (post evaluation)')),
                ('test_state_hash', models.CharField(blank=True, help_text='A hash to keep track of iospec sources updates.', max_length=32)),
                ('timeout', models.FloatField(blank=True, default=1.0, help_text='Defines the maximum runtime the grader will spend evaluating each test case.', validators=[codeschool.questions.coding_io.models.validators.timeout_validator], verbose_name='timeout in seconds')),
                ('default_placeholder', models.TextField(blank=True, help_text='Default placeholder message that is used if it is not defined for the given language. This will appear as a block of comment in the beginning of the submission.', verbose_name='placeholder')),
                ('error_field', models.CharField(blank=True, max_length=20)),
                ('error_message', models.TextField(blank=True)),
                ('ignore_programming_errors', models.BooleanField(default=False, help_text='Mark this if you want to ignore programming errors this time. It will ignore errors once, but you still have to fix the source of those errors to make the question become operational.')),
                ('language', models.ForeignKey(blank=True, help_text='Programming language associated with question. Leave it blank in order to accept submissions in any programming language. This option should be set only for questions that tests specific programming languages constructs or require techniques that only make sense for specific programming languages.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.ProgrammingLanguage')),
            ],
            options={
                'verbose_name': 'Programming question (IO-based)',
                'verbose_name_plural': 'Programming questions (IO-based)',
            },
            bases=(wagtail.contrib.wagtailroutablepage.models.RoutablePageMixin, 'wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='CodingIoSubmission',
            fields=[
                ('submission_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='activities.Submission')),
                ('source', models.TextField(blank=True)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ProgrammingLanguage')),
            ],
            options={
                'abstract': False,
            },
            bases=(codeschool.questions.models.QuestionMixin, 'activities.submission'),
        ),
        migrations.CreateModel(
            name='TestState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(max_length=32)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('pre_tests_source', models.TextField(blank=True)),
                ('post_tests_source', models.TextField(blank=True)),
                ('pre_tests_source_expansion', models.TextField(blank=True)),
                ('post_tests_source_expansion', models.TextField(blank=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coding_io.CodingIoQuestion')),
            ],
        ),
        migrations.AddField(
            model_name='answerkey',
            name='question',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='coding_io.CodingIoQuestion'),
        ),
        migrations.AlterUniqueTogether(
            name='teststate',
            unique_together=set([('question', 'hash')]),
        ),
        migrations.AlterUniqueTogether(
            name='answerkey',
            unique_together=set([('question', 'language')]),
        ),
    ]
