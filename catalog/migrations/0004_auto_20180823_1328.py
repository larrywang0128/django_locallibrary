# Generated by Django 2.1 on 2018-08-23 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20180823_1030'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_view_all_borrow', 'View all borrowed books'), ('can_renew_book', 'Renew a book'))},
        ),
    ]