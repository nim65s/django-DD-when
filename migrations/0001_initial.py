from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DispoToPlay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dispo', models.NullBooleanField(default=True)),
            ],
            options={
                'ordering': ['moment', 'user'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Groupe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(unique=True, max_length=50)),
                ('jours', models.CommaSeparatedIntegerField(max_length=13)),
                ('debut', models.IntegerField()),
                ('duree', models.IntegerField()),
                ('membres', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['nom'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Moment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('moment', models.DateTimeField(unique=True)),
            ],
            options={
                'ordering': ['moment'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='groupe',
            name='moments',
            field=models.ManyToManyField(to='when.Moment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dispotoplay',
            name='moment',
            field=models.ForeignKey(to='when.Moment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dispotoplay',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='dispotoplay',
            unique_together=set([('moment', 'user')]),
        ),
    ]
