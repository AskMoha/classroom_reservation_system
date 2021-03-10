# Generated by Django 3.1.4 on 2021-03-09 22:10

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[(1, 'Admin'), (2, 'Enseignant'), (3, 'Etudiant')], default=1, max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Batiment',
            fields=[
                ('num_batiment', models.AutoField(db_column='Num_batiment', primary_key=True, serialize=False)),
                ('nom', models.CharField(db_column='Nom', max_length=30)),
                ('heure_ouverture', models.IntegerField()),
                ('heure_fermeture', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Enseignants',
            fields=[
                ('idenseignant', models.AutoField(db_column='IDEnseignant', primary_key=True, serialize=False)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Etudiants',
            fields=[
                ('idetudiant', models.AutoField(db_column='IDEtudiant', primary_key=True, serialize=False)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Salle',
            fields=[
                ('idsalle', models.AutoField(db_column='IDSalle', primary_key=True, serialize=False)),
                ('num_salle', models.IntegerField(db_column='Num_salle')),
                ('capacite', models.IntegerField(db_column='Capacite')),
                ('type', models.CharField(db_column='Type', max_length=30)),
                ('id_batiment', models.ForeignKey(db_column='ID_batiment', on_delete=django.db.models.deletion.CASCADE, to='classroom_reservation_app.batiment')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('idreservation', models.AutoField(db_column='IDReservation', primary_key=True, serialize=False)),
                ('date', models.DateField(db_column='Date')),
                ('heure_debut', models.IntegerField(db_column='Heure_debut')),
                ('nb_participants', models.IntegerField(db_column='Nb_participants')),
                ('idenseignant', models.ForeignKey(blank=True, db_column='IDEnseignant', null=True, on_delete=django.db.models.deletion.CASCADE, to='classroom_reservation_app.enseignants')),
                ('idetudiant', models.ForeignKey(blank=True, db_column='IDEtudiant', null=True, on_delete=django.db.models.deletion.CASCADE, to='classroom_reservation_app.etudiants')),
                ('idsalle', models.ForeignKey(db_column='IDSalle', on_delete=django.db.models.deletion.CASCADE, to='classroom_reservation_app.salle')),
            ],
        ),
        migrations.CreateModel(
            name='Administrateurs',
            fields=[
                ('idadministrateur', models.AutoField(db_column='IDAdministrateur', primary_key=True, serialize=False)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]