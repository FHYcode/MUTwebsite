# Generated by Django 3.0.3 on 2020-08-09 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Covid19metadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('virus_strain_name', models.CharField(max_length=255)),
                ('accession_id', models.CharField(blank=True, max_length=255)),
                ('data_source', models.CharField(blank=True, max_length=255)),
                ('related_id', models.CharField(blank=True, max_length=255)),
                ('nuc_completeness', models.CharField(blank=True, max_length=255)),
                ('sequence_length', models.IntegerField(blank=True, default=0)),
                ('sequence_quality', models.CharField(blank=True, max_length=255)),
                ('quality_assessment', models.TextField(blank=True)),
                ('host', models.CharField(blank=True, max_length=255)),
                ('sample_collection_date', models.DateTimeField(blank=True)),
                ('location', models.TextField(blank=True)),
                ('originating_lab', models.TextField(blank=True)),
                ('submission_date', models.DateTimeField(blank=True)),
                ('submission_lab', models.TextField(blank=True)),
                ('create_time', models.DateTimeField(blank=True)),
                ('last_update_time', models.DateTimeField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MutSamplelist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ti_tv', models.CharField(blank=True, max_length=255)),
                ('start', models.IntegerField(blank=True)),
                ('end', models.IntegerField(blank=True)),
                ('ref_var', models.TextField(blank=True)),
                ('gene', models.CharField(blank=True, max_length=255)),
                ('ns_s', models.CharField(blank=True, max_length=255)),
                ('count', models.IntegerField(blank=True)),
                ('sample', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SampleMutlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('virus_strain_name', models.CharField(max_length=255)),
                ('mutation', models.TextField(blank=True)),
                ('metadata', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mutapp.Covid19metadata')),
            ],
        ),
    ]
