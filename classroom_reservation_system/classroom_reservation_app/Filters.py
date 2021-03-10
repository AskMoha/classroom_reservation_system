import django_filters
from .models import Salle, Batiment

class SalleFilter(django_filters.FilterSet):
    id_batiment__nom = django_filters.CharFilter(label='Batiment')
    idsalle = django_filters.NumberFilter(label='Identifiant')
    num_salle = django_filters.NumberFilter(label='Numéro')
    capacite = django_filters.NumberFilter(label='Capacité')
    class Meta:
        model = Salle
        fields = ['idsalle','num_salle', 'type', 'capacite', 'id_batiment__nom',]

class BatimentFilter(django_filters.FilterSet):
    num_batiment = django_filters.CharFilter(label='Identifiant')

    class Meta:
        model = Batiment
        fields = ['num_batiment','nom',]

