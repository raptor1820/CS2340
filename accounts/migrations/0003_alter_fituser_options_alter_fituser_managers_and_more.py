# Generated by Django 5.1.5 on 2025-04-14 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_fituser_groups_alter_fituser_user_permissions'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fituser',
            options={},
        ),
        migrations.AlterModelManagers(
            name='fituser',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='fituser',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='fituser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='fituser',
            name='last_name',
        ),
        migrations.AddField(
            model_name='fituser',
            name='workoutCountHistory',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AlterField(
            model_name='fituser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='fituser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='fituser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='fituser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AlterField(
            model_name='fituser',
            name='username',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
