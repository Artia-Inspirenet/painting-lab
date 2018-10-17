# Generated by Django 2.0.7 on 2018-10-17 06:38

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
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Cut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_file', models.FileField(upload_to='')),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('w', models.IntegerField()),
                ('h', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='webapp.Author')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('index', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('partnum', models.PositiveSmallIntegerField()),
                ('cluster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Cluster')),
                ('cut', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Cut')),
            ],
        ),
        migrations.CreateModel(
            name='KeyPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('visible', models.NullBooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='PSDFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
                ('psdfile', models.FileField(upload_to='')),
                ('w', models.IntegerField(null=True)),
                ('h', models.IntegerField(null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.Author')),
                ('episode', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.Episode')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='webapp.Author')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='psdfile',
            name='work',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.Work'),
        ),
        migrations.AddField(
            model_name='episode',
            name='work',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='webapp.Work'),
        ),
        migrations.AddField(
            model_name='cut',
            name='episode',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.Episode'),
        ),
        migrations.AddField(
            model_name='cut',
            name='pre_cut',
            field=models.OneToOneField(null=True, on_delete=None, related_name='previous_cut', to='webapp.Cut'),
        ),
        migrations.AddField(
            model_name='cluster',
            name='work',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='webapp.Work'),
        ),
    ]
