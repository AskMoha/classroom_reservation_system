from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from .models import Reservation, Salle, Etudiants, Batiment, CustomUser


def student_home(request):
    if 'search' in request.GET:
        search = request.GET['search']
        batiment = Batiment.objects.filter(nom__icontains=search)
    else:
        batiment = Batiment.objects.all()
    return render(request, 'student_templates/student_home_template.html', {"batiment": batiment})

def edit_student(request):
    return render(request, 'student_templates/edit_student_template.html')

def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        id = request.POST.get("id")
        username = request.POST.get("num_etudiant")
        nom = request.POST.get("last_name")
        prenom = request.POST.get("first_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            staff = CustomUser.objects.get(id=id)
            staff.username = username
            staff.last_name = nom
            staff.first_name = prenom
            staff.email = email
            staff.password = password
            staff.save()
            messages.success(request, "Vos informations ont été modifiées !")
            return HttpResponseRedirect("/edit_student")
        except:
            messages.success(request, "Erreur, veuillez resaisir les informations !")
            return HttpResponseRedirect("/edit_student")

def add_reservation(request, id_bat):
    batiment = Batiment.objects.get(num_batiment=id_bat)
    return render(request, 'student_templates/add_reservation_template.html', {"batiment": batiment})

def add_reservation2(request, id_bat, date, materiel, nb_pers, duree):
    batiment = Batiment.objects.get(num_batiment=id_bat)
    classe = Salle.objects.filter(id_batiment=id_bat)
    reservation = Reservation.objects.filter(idsalle=classe, date=date)
    return render(request, 'student_templates/add_reservation_template2.html',{"batiment": batiment, "date": date, "materiel": materiel, "nb_pers": nb_pers, "duree": duree})

def add_reservation3(request, id_bat, date, materiel, nb_pers, duree, heure_debut):
    batiment = Batiment.objects.get(num_batiment=id_bat)
    sallereservee = Reservation.objects.filter(date=date, heure_debut=heure_debut, idsalle__id_batiment=id_bat, idsalle__type=materiel).values('idsalle')
    classedispo = Salle.objects.filter(id_batiment=id_bat, type=materiel).exclude(idsalle__in=sallereservee)
    return render(request, 'student_templates/add_reservation_template3.html', {"batiment":batiment, "date": date, "materiel": materiel, "nb_pers": nb_pers, "duree": duree, "heure_debut": heure_debut, "classedispo": classedispo})

def add_reservation_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")

    else:
        date = request.POST.get("date")
        heure_debut = request.POST.get("heure")
        duree = request.POST.get("durée")
        nb_participants = request.POST.get("nb_pers")
        idsalle = request.POST.get("id")
        idetudiant = request.POST.get("id_user")
        batiment_id = request.POST.get("batiment_id")
        materiel = request.POST.get("Matériels")
        email = request.POST['email']

        salle = Salle.objects.get(idsalle=idsalle)
        etudiant = Etudiants.objects.get(idetudiant=idetudiant)
        try:
            heure_temp = heure_debut
            for x in range(int(duree)):
                reservation = Reservation(date=date, heure_debut=heure_debut, nb_participants=nb_participants,
                                      idsalle=salle, idetudiant=etudiant)
                reservation.save()
                heure_debut = int(heure_debut)+1;

            expediteur = 'settings.EMAIL_HOST_USER'
            send_mail('Votre réservation a bien été prise en compte',
                      'Détails de votre réservation:'+date,
                      expediteur,
                      [email],
                      fail_silently=False)
            return HttpResponseRedirect("manage_reservation_student/"+idetudiant)
        except:
            messages.error(request, "Erreur, veuillez ressaisir les informations !")
            return HttpResponseRedirect("/add_reservation_student/" + batiment_id+"/"+date+"/"+materiel+"/"+nb_participants+"/"+duree+"/"+heure_temp)

def manage_reservation(request, etudiant_id):
    reservation = Reservation.objects.filter(idetudiant=etudiant_id)
    return render(request, 'student_templates/manage_reservation_template.html', {"reservation": reservation})


def delete_reservation(request, reservation_id):
    reservation = Reservation.objects.get(idreservation=reservation_id)
    return render(request, 'student_templates/delete_reservation_template.html', {"reservation": reservation})

def delete_reservation_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")

    else:
        reservation_id = request.POST.get("id")
        etudiant_id = request.POST.get("idetudiant")
        try:
            reservation = Reservation.objects.get(idreservation=reservation_id)
            reservation.delete()
            messages.success(request, "La réservation a été supprimée !")
            return HttpResponseRedirect("manage_reservation_student/"+etudiant_id)

        except:
            messages.error(request, "Erreur, la réservation n'est pas supprimée !")
            return HttpResponseRedirect("/delete_reservation_student/"+reservation_id)

