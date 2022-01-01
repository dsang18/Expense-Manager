# Generated by Django 3.2.6 on 2021-11-29 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Credentials',
            fields=[
                ('UID', models.AutoField(primary_key=True, serialize=False)),
                ('fullname', models.CharField(max_length=50)),
                ('email_id', models.CharField(max_length=50)),
                ('phone_no', models.BigIntegerField()),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.BinaryField()),
            ],
        ),
        migrations.CreateModel(
            name='expense_categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_type', models.CharField(max_length=40)),
                ('user', models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.CASCADE, to='budget_app.credentials')),
            ],
        ),
        migrations.CreateModel(
            name='expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense_type', models.CharField(max_length=50)),
                ('expense_amnt', models.IntegerField()),
                ('expense_day', models.CharField(max_length=15)),
                ('expense_date', models.CharField(max_length=20)),
                ('expense_time', models.CharField(max_length=20)),
                ('user', models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.CASCADE, to='budget_app.credentials')),
            ],
        ),
        migrations.CreateModel(
            name='budget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
                ('total_budget', models.IntegerField()),
                ('left_budget', models.IntegerField()),
                ('user_exp', models.ForeignKey(db_column='user_exp', on_delete=django.db.models.deletion.CASCADE, to='budget_app.credentials')),
            ],
        ),
    ]