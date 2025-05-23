# Generated by Django 4.2.18 on 2025-01-22 12:09

from django.db import migrations, models
import django.db.models.deletion
import recipe_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id_recipe', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('file', models.FileField(upload_to='media/', validators=[recipe_app.models.validate_file_type])),
                ('user', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('id_recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='recipe_app.recipe')),
            ],
        ),
    ]
