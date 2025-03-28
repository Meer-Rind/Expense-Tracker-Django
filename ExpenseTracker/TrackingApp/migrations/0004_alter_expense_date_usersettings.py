# Generated by Django 5.1.7 on 2025-03-25 17:42

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TrackingApp', '0003_expense'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preferred_currency', models.CharField(choices=[('USD', 'US Dollar'), ('PKR', 'Pakistani Rupee'), ('EUR', 'Euro')], default='USD', max_length=5)),
                ('dark_mode', models.BooleanField(default=False)),
                ('custom_categories', models.JSONField(default=list)),
                ('notify_when_low_balance', models.BooleanField(default=True)),
                ('notify_via_email', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
