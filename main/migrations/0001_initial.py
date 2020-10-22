# Generated by Django 3.1.1 on 2020-10-20 20:17

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('avatar', models.ImageField(max_length=250, upload_to='categories')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('avatar', models.ImageField(max_length=250, upload_to='categories')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.category')),
            ],
        ),
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('avatar', models.ImageField(upload_to='tutorials')),
                ('short_desc', models.TextField()),
                ('description', ckeditor.fields.RichTextField()),
                ('url', models.CharField(max_length=250)),
                ('total_views', models.IntegerField(default=0)),
                ('price', models.FloatField()),
                ('pricing', models.CharField(choices=[('free', 'Free'), ('paid', 'Paid')], max_length=50)),
                ('medium', models.CharField(choices=[('video', 'Video'), ('blog', 'Blog'), ('book', 'Book')], max_length=50)),
                ('level', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], max_length=50)),
                ('is_active', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('down_vote', models.ManyToManyField(blank=True, related_name='down_vote', to=settings.AUTH_USER_MODEL)),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.subcategory')),
                ('up_vote', models.ManyToManyField(blank=True, related_name='up_vote', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('text', models.TextField(max_length=200)),
                ('pricing', models.CharField(choices=[('free', 'Free'), ('paid', 'Paid')], max_length=50)),
                ('medium', models.CharField(choices=[('video', 'Video'), ('blog', 'Blog'), ('book', 'Book')], max_length=50)),
                ('level', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], max_length=50)),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.subcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('tutorial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.tutorial')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
