# Generated by Django 2.2.2 on 2019-06-08 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zoo_checks', '0010_auto_20190608_0234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animalcount',
            name='condition',
            field=models.CharField(choices=[('SE', 'seen'), ('NA', 'Needs Attention'), ('BA', 'BAR (Sr. Avic.)'), ('MI', 'Missing (Avic. only)')], max_length=2),
        ),
    ]