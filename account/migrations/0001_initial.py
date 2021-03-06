# Generated by Django 3.0.6 on 2020-05-24 10:27

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
            name='availablepost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='dept',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('location', models.CharField(max_length=100)),
                ('budget', models.IntegerField()),
                ('deadline', models.DateField()),
                ('no_of_emp', models.IntegerField()),
                ('hop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='empdetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')),
                ('address', models.CharField(max_length=100)),
                ('phone_no', models.CharField(max_length=13)),
                ('age', models.IntegerField()),
                ('salary', models.IntegerField()),
                ('dno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.dept')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.availablepost')),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='attendance2020',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(max_length=20)),
                ('day1', models.CharField(default='A', max_length=2)),
                ('day2', models.CharField(default='A', max_length=2)),
                ('day3', models.CharField(default='A', max_length=2)),
                ('day4', models.CharField(default='A', max_length=2)),
                ('day5', models.CharField(default='A', max_length=2)),
                ('day6', models.CharField(default='A', max_length=2)),
                ('day7', models.CharField(default='A', max_length=2)),
                ('day8', models.CharField(default='A', max_length=2)),
                ('day9', models.CharField(default='A', max_length=2)),
                ('day10', models.CharField(default='A', max_length=2)),
                ('day11', models.CharField(default='A', max_length=2)),
                ('day12', models.CharField(default='A', max_length=2)),
                ('day13', models.CharField(default='A', max_length=2)),
                ('day14', models.CharField(default='A', max_length=2)),
                ('day15', models.CharField(default='A', max_length=2)),
                ('day16', models.CharField(default='A', max_length=2)),
                ('day17', models.CharField(default='A', max_length=2)),
                ('day18', models.CharField(default='A', max_length=2)),
                ('day19', models.CharField(default='A', max_length=2)),
                ('day20', models.CharField(default='A', max_length=2)),
                ('day21', models.CharField(default='A', max_length=2)),
                ('day22', models.CharField(default='A', max_length=2)),
                ('day23', models.CharField(default='A', max_length=2)),
                ('day24', models.CharField(default='A', max_length=2)),
                ('day25', models.CharField(default='A', max_length=2)),
                ('day26', models.CharField(default='A', max_length=2)),
                ('day27', models.CharField(default='A', max_length=2)),
                ('day28', models.CharField(default='A', max_length=2)),
                ('day29', models.CharField(default='A', max_length=2)),
                ('day30', models.CharField(default='A', max_length=2)),
                ('day31', models.CharField(default='A', max_length=2)),
                ('total_att', models.IntegerField()),
                ('overtime', models.IntegerField()),
                ('pendingsalary', models.IntegerField()),
                ('recivedsalary', models.IntegerField()),
                ('eid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='dept_in_pro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.dept')),
                ('mgr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.project')),
            ],
            options={
                'unique_together': {('pro', 'dept')},
            },
        ),
    ]
