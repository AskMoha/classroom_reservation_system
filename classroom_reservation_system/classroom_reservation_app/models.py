from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

class CustomUser(AbstractUser):
    user_type_data = ((1,"Admin"), (2,"Enseignant"), (3,"Etudiant"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)

    def check_email(self):
        if CustomUser.objects.filter(email=self.email):
            return True
        return False

class Administrateurs(models.Model):
    idadministrateur = models.AutoField(db_column='IDAdministrateur', primary_key=True)  # Field name made lowercase.
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    objects = models.Manager()


class Batiment(models.Model):
    num_batiment = models.AutoField(db_column='Num_batiment', primary_key=True)  # Field name made lowercase.
    nom = models.CharField(db_column='Nom', max_length=30)  # Field name made lowercase.
    heure_ouverture = models.IntegerField()
    heure_fermeture = models.IntegerField()
    objects = models.Manager()


class Enseignants(models.Model):
    idenseignant = models.AutoField(db_column='IDEnseignant', primary_key=True)  # Field name made lowercase.
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    objects = models.Manager()


class Etudiants(models.Model):
    idetudiant = models.AutoField(db_column='IDEtudiant', primary_key=True)  # Field name made lowercase.
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    objects = models.Manager()


class Reservation(models.Model):
    idreservation = models.AutoField(db_column='IDReservation', primary_key=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date')  # Field name made lowercase.
    heure_debut = models.IntegerField(db_column='Heure_debut')  # Field name made lowercase.
    nb_participants = models.IntegerField(db_column='Nb_participants')  # Field name made lowercase.
    idsalle = models.ForeignKey('Salle', on_delete=models.CASCADE, db_column='IDSalle')  # Field name made lowercase.
    idenseignant = models.ForeignKey('Enseignants', on_delete=models.CASCADE, db_column='IDEnseignant', blank=True, null=True)  # Field name made lowercase.
    idetudiant = models.ForeignKey(Etudiants, on_delete=models.CASCADE, db_column='IDEtudiant', blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()


class Salle(models.Model):
    idsalle = models.AutoField(db_column='IDSalle', primary_key=True)  # Field name made lowercase.
    num_salle = models.IntegerField(db_column='Num_salle')  # Field name made lowercase.
    capacite = models.IntegerField(db_column='Capacite')  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=30)  # Field name made lowercase.
    id_batiment = models.ForeignKey('Batiment', db_column='ID_batiment', on_delete=models.CASCADE)  # Field name made lowercase.


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type==1:
            Administrateurs.objects.create(admin=instance)
        if instance.user_type==2:
            Enseignants.objects.create(admin=instance)
        if instance.user_type==3:
            Etudiants.objects.create(admin=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type==1:
        instance.administrateurs.save()
    if instance.user_type==2:
        instance.enseignants.save()
    if instance.user_type==3:
        instance.etudiants.save()