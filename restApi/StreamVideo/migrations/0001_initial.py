# Generated by Django 5.0.1 on 2024-02-15 12:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('apellidos', models.CharField(blank=True, max_length=100, null=True)),
                ('edad', models.IntegerField(blank=True, null=True)),
                ('nombreficticio', models.CharField(blank=True, db_column='nombreFicticio', max_length=50, null=True)),
                ('foto', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'db_table': 'actor',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Comentariospeliculas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.CharField(blank=True, max_length=800, null=True)),
            ],
            options={
                'db_table': 'comentariospeliculas',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Comentariosseries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.CharField(blank=True, max_length=800, null=True)),
            ],
            options={
                'db_table': 'comentariosseries',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Favoritos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('esfavorito', models.IntegerField(blank=True, db_column='esFavorito', null=True)),
            ],
            options={
                'db_table': 'favoritos',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Peliculas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('genero', models.CharField(blank=True, max_length=200, null=True)),
                ('año', models.TextField(blank=True, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=300, null=True)),
                ('urlimagen', models.CharField(blank=True, db_column='urlImagen', max_length=5500, null=True)),
                ('duracion', models.IntegerField(blank=True, null=True)),
                ('valoracion', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'peliculas',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Plataformas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'plataformas',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('genero', models.CharField(blank=True, max_length=30, null=True)),
                ('año', models.TextField(blank=True, null=True)),
                ('numtemporadas', models.IntegerField(blank=True, db_column='numTemporadas', null=True)),
                ('descripcion', models.CharField(blank=True, max_length=300, null=True)),
                ('urlimagen', models.CharField(blank=True, db_column='urlImagen', max_length=2000, null=True)),
                ('valoracion', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'series',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('apellidos', models.CharField(blank=True, max_length=100, null=True)),
                ('contraseña', models.CharField(blank=True, max_length=200, null=True)),
                ('telefono', models.CharField(blank=True, max_length=9, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('sessiontoken', models.CharField(blank=True, db_column='sessionToken', max_length=500, null=True)),
                ('comentariopeliculaid', models.ForeignKey(blank=True, db_column='comentariopeliculaId', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='StreamVideo.comentariospeliculas')),
                ('comentarioserieid', models.ForeignKey(blank=True, db_column='comentarioserieId', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='StreamVideo.comentariosseries')),
                ('favoritoid', models.ForeignKey(blank=True, db_column='favoritoId', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='StreamVideo.favoritos')),
            ],
        ),
    ]
