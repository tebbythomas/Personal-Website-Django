# Generated by Django 3.0.3 on 2020-02-06 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('github_link', models.CharField(max_length=200)),
                ('demo_link', models.CharField(blank=True, max_length=200)),
                ('description', models.TextField()),
                ('project_image', models.ImageField(upload_to='projects_photos/')),
            ],
        ),
    ]