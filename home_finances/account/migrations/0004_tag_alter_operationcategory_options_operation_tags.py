# Generated by Django 4.0.4 on 2022-08-21 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_operation_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AlterModelOptions(
            name='operationcategory',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='operation',
            name='tags',
            field=models.ManyToManyField(blank=True, to='account.tag'),
        ),
    ]
