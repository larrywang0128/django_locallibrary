# Generated by Django 2.1 on 2018-08-06 01:45

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='Enter the frist name', max_length=50)),
                ('last_name', models.CharField(help_text='Enter the last name', max_length=50)),
                ('dob', models.DateField(blank=True, help_text='Enter date of birth', null=True, verbose_name='Date of Birth')),
                ('dod', models.DateField(blank=True, help_text='Enter date of death (leave blank if still alive)', null=True, verbose_name='Date of Death')),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter the book title', max_length=200)),
                ('summary', models.TextField(help_text='Enter a brief book summary', max_length=5000)),
                ('isbn', models.CharField(help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>', max_length=13, verbose_name='ISBN')),
                ('pubdate', models.DateField(help_text='Enter the publication date')),
                ('create_dt', models.DateTimeField(auto_now_add=True, help_text='Creation datetime of the record')),
            ],
            options={
                'ordering': ['title', '-pubdate'],
            },
        ),
        migrations.CreateModel(
            name='BookInstance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular book across whole library', primary_key=True, serialize=False)),
                ('imprint', models.CharField(help_text='Enter version details', max_length=200)),
                ('due_back', models.DateField(blank=True, help_text='Enter due date to return', null=True)),
                ('status', models.CharField(blank=True, choices=[('m', 'Maintenance'), ('o', 'On loan'), ('a', 'Available'), ('r', 'Reserved')], default='m', help_text='Book availability', max_length=1)),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Book')),
            ],
            options={
                'ordering': ['due_back'],
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter genre of the book (e.g. Science Fiction)', max_length=200)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('en', 'English'), ('cn', 'Chinese'), ('sp', 'Spanish'), ('fr', 'Frech')], help_text='Select the language of the book', max_length=2)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='book',
            name='Language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Language'),
        ),
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.ForeignKey(help_text='Select the author name', null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Author'),
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(help_text='Select a genre for the book', to='catalog.Genre'),
        ),
    ]
