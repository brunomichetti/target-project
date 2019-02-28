# Generated by Django 2.1.7 on 2019-02-26 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('targets', '0004_auto_20190218_1433'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(choices=[('Football', 'Football'), ('Travel', 'Travel'), ('Politics', 'Politics'), ('Art', 'Art'), ('Dating', 'Dating'), ('Music', 'Music'), ('Movies', 'Movies'), ('Series', 'Series'), ('Food', 'Food')], max_length=50)),
                ('target_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_1', to='targets.Target')),
                ('target_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_2', to='targets.Target')),
            ],
        ),
    ]
