import csv
import io
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .Filters import SalleFilter, BatimentFilter

from .models import Enseignants, Etudiants, Salle, Batiment, CustomUser

def admin_home(request):
    batiment = Batiment.objects.all()
    return render(request, 'admin_templates/admin_home_template.html', {"batiment": batiment})

def edit_admin(request):
    return render(request, 'admin_templates/edit_admin_template.html')

def edit_admin_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")
    else:
        id = request.POST.get("id")
        username = request.POST.get("username")
        nom = request.POST.get("last_name")
        prenom = request.POST.get("first_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            admin = CustomUser.objects.get(id=id)
            admin.username = username
            admin.last_name = nom
            admin.first_name = prenom
            admin.email = email
            admin.password = password
            admin.save()
            messages.success(request, "Vos informations ont été modifiées !")
            return HttpResponseRedirect("/edit_admin")
        except:
            messages.success(request, "Erreur, veuillez resaisir les informations !")
            return HttpResponseRedirect("/edit_admin")

def add_staff(request):
    return render(request, 'admin_templates/add_staff_template.html')

def add_staff_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")

    else:
        username = request.POST.get("username")
        prenom = request.POST.get("first_name")
        nom = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.create_user(username=username, email=email, password=password, last_name=nom, first_name=prenom, user_type=2)
            user.save()
            messages.success(request, "L'enseignant a été ajouté !")
            return HttpResponseRedirect("add_staff")
        except:
            messages.error(request, "Erreur, veuillez ressaisir les informations !")
            return HttpResponseRedirect("add_staff")

def add_student(request):
    return render(request, 'admin_templates/add_student_template.html')

def add_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")

    else:
        username = request.POST.get("num_etudiant")
        prenom = request.POST.get("first_name")
        nom = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, last_name=nom, first_name=prenom, user_type=3)
            user.save()
            messages.success(request, "L'étudiant a été ajouté !")
            return HttpResponseRedirect("add_student")
        except:
            messages.error(request, "Erreur, veuillez ressaisir les informations !")
            return HttpResponseRedirect("add_student")

def add_classroom(request):
    batiments = Batiment.objects.all()
    return render(request, 'admin_templates/add_classroom_template.html', {"batiments": batiments})

def add_classroom_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")

    else:
        numero = request.POST.get("num_salle")
        capacite = request.POST.get("capacite")
        type = request.POST.get("type")
        batiment_id = request.POST.get("batiment")
        batiment = Batiment.objects.get(num_batiment=batiment_id)

        try:
            salle = Salle(num_salle=numero, capacite=capacite, type=type, id_batiment=batiment)
            salle.save()
            messages.success(request, "La salle a été ajoutée !")
            return HttpResponseRedirect("add_classroom")
        except:
            messages.error(request, "Erreur, veuillez ressaisir les informations !")
            return HttpResponseRedirect("add_classroom")

def manage_classroom(request):
    classe = Salle.objects.all()
    myFilter = SalleFilter(request.GET, queryset=classe)
    classe = myFilter.qs
    return render(request, "admin_templates/manage_classroom_template.html", {"classe": classe, "myFilter": myFilter})

def edit_classroom(request, classe_id):
    classe = Salle.objects.get(idsalle=classe_id)
    batiment = Batiment.objects.all()
    return render(request, "admin_templates/edit_classroom_template.html", {"classe": classe, "batiment": batiment})

def edit_classroom_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")

    else:
        classe_id = request.POST.get("id")
        numero = request.POST.get("num_salle")
        capacite = request.POST.get("capacite")
        type = request.POST.get("type")
        batiment_id = request.POST.get("batiment")

        try:
            salle = Salle.objects.get(idsalle=classe_id)
            salle.num_salle = numero
            salle.capacite = capacite
            salle.type = type
            batiment = Batiment.objects.get(num_batiment=batiment_id)
            salle.id_batiment = batiment
            salle.save()
            messages.success(request, "La salle a été modifiée !")
            return HttpResponseRedirect("/edit_classroom/"+classe_id)

        except:
            messages.error(request, "Erreur, veuillez ressaisir les informations !")
            return HttpResponseRedirect("/edit_classroom/"+classe_id)

def delete_classroom(request, classe_id):
    salle = Salle.objects.get(idsalle=classe_id)
    return render(request, "admin_templates/delete_classroom_template.html", {"salle": salle})

def delete_classroom_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")

    else:
        salle_id = request.POST.get("id")
        try:
            salle = Salle.objects.get(idsalle=salle_id)
            salle.delete()
            return HttpResponseRedirect("manage_classroom")

        except:
            messages.error(request, "Erreur, la salle n'est pas supprimée !")
            return HttpResponseRedirect("/delete_classroom/"+salle_id)

def add_building(request):
    return render(request, 'admin_templates/add_building_template.html')

def add_building_save(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed")

    else:
        nom = request.POST.get("nom")
        ouverture = request.POST.get("heure_ouverture")
        fermeture = request.POST.get("heure_fermeture")
        uploaded_file = request.FILES['document']
        uploaded_file.name = nom + ".PNG"
        try:
            batiment = Batiment(nom=nom, heure_ouverture=ouverture, heure_fermeture=fermeture)
            batiment.save()
            fs = FileSystemStorage()
            fs.save(uploaded_file.name, uploaded_file)
            messages.success(request, "Le batiment a été ajouté !")
            return HttpResponseRedirect("add_building")
        except:
            messages.error(request, "Erreur, veuillez ressaisir les informations !")
            return HttpResponseRedirect("add_building")

def manage_building(request):
    batiment = Batiment.objects.all()
    myFilter = BatimentFilter(request.GET, queryset=batiment)
    batiment = myFilter.qs
    return render(request, "admin_templates/manage_building_template.html", {"batiment": batiment, "myFilter": myFilter})

def edit_building(request, batiment_id):
    batiment = Batiment.objects.get(num_batiment=batiment_id)
    return render(request, "admin_templates/edit_building_template.html", {"batiment": batiment})

def edit_building_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")

    else:
        batiment_id = request.POST.get("num_batiment")
        nom = request.POST.get("nom")
        ouverture = request.POST.get("ouverture")
        fermeture = request.POST.get("fermeture")

        try:
            batiment = Batiment.objects.get(num_batiment=batiment_id)
            batiment.nom = nom
            batiment.heure_ouverture = ouverture
            batiment.heure_fermeture = fermeture
            batiment.save()
            messages.success(request, "Le batiment a été modifié !")
            return HttpResponseRedirect("/edit_building/"+batiment_id)

        except:
            messages.error(request, "Erreur, veuillez ressaisir les informations !")
            return HttpResponseRedirect("/edit_building/"+batiment_id)

def delete_building(request, batiment_id):
    batiment = Batiment.objects.get(num_batiment=batiment_id)
    return render(request, "admin_templates/delete_building_template.html", {"batiment": batiment})

def delete_building_save(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed")

    else:
        batiment_id = request.POST.get("id")
        try:
            batiment = Batiment.objects.get(num_batiment=batiment_id)
            batiment.delete()
            return HttpResponseRedirect("manage_building")

        except:
            messages.error(request, "Erreur, le batiment n'est pas supprimé !")
            return HttpResponseRedirect("/delete_building/"+batiment_id)

def export(request,id_bat):
    response = HttpResponse(content_type='text/csv')
    writer  = csv.writer(response)
    writer.writerow(['id salle','numero de la salle','capacite','type','id du batiment'])
    for salle in Salle.objects.filter(id_batiment=id_bat).values_list('idsalle','num_salle','capacite','type','id_batiment'):
        writer.writerow(salle)
    response['Content-Disposition']='attachment; filename="salle.csv"'
    return response

def export_json(request,id_bat):
    data = serializers.serialize("json", Salle.objects.filter(id_batiment=id_bat))
    out = open("Salle.json", "w")
    out.write(data)
    out.close()
    return HttpResponseRedirect("/admin_home")

def importation(request):
    csv_file = request.FILES['document']
    decoded_file = csv_file.read().decode('utf-8')
    io_string = io.StringIO(decoded_file)
    for row in csv.DictReader(io_string):
        num_salle=row['numero de la salle']
        capacite=row['capacite']
        type=row['type']
        id_batiment=Batiment.objects.get(num_batiment=row['id du batiment'])
        new_salles=Salle(num_salle=num_salle,capacite=capacite,type=type,id_batiment=id_batiment)
        new_salles.save()
    return HttpResponseRedirect("admin_home")

