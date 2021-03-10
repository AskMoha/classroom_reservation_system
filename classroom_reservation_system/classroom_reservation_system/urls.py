"""classroom_reservation_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from classroom_reservation_system import settings
from classroom_reservation_app import views, Admin_views, Staff_views, Student_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.ShowLoginPage),
    path('doLogin', views.doLogin),
    path('logout', views.logout_user),

    #URLS ADMIN
    path('admin_home', Admin_views.admin_home),
    path('edit_admin', Admin_views.edit_admin),
    path('edit_admin_save', Admin_views.edit_admin_save),
    path('add_staff', Admin_views.add_staff),
    path('add_staff_save', Admin_views.add_staff_save),
    path('add_student', Admin_views.add_student),
    path('add_student_save', Admin_views.add_student_save),
    path('add_classroom', Admin_views.add_classroom),
    path('add_classroom_save', Admin_views.add_classroom_save),
    path('manage_classroom', Admin_views.manage_classroom),
    path('edit_classroom/<str:classe_id>', Admin_views.edit_classroom),
    path('edit_classroom_save', Admin_views.edit_classroom_save),
    path('delete_classroom/<str:classe_id>', Admin_views.delete_classroom),
    path('delete_classroom_save', Admin_views.delete_classroom_save),
    path('add_building', Admin_views.add_building),
    path('add_building_save', Admin_views.add_building_save),
    path('manage_building', Admin_views.manage_building),
    path('edit_building/<str:batiment_id>', Admin_views.edit_building),
    path('edit_building_save', Admin_views.edit_building_save),
    path('delete_building/<str:batiment_id>', Admin_views.delete_building),
    path('delete_building_save', Admin_views.delete_building_save),
    path('export/<str:id_bat>',Admin_views.export),
    path('export_json/<str:id_bat>',Admin_views.export_json),
    path('importation',Admin_views.importation),

    # URLS STAFFS
    path('staff_home', Staff_views.staff_home),
    path('edit_staff', Staff_views.edit_staff),
    path('edit_staff_save', Staff_views.edit_staff_save),
    path('add_reservation/<str:id_bat>', Staff_views.add_reservation),
    path('add_reservation/<str:id_bat>/<str:date>/<str:materiel>/<str:nb_pers>/<str:duree>', Staff_views.add_reservation2),
    path('add_reservation/<str:id_bat>/<str:date>/<str:materiel>/<str:nb_pers>/<str:duree>/<str:heure_debut>',Staff_views.add_reservation3),
    path('add_reservation_save', Staff_views.add_reservation_save),
    path('manage_reservation/<str:enseignant_id>', Staff_views.manage_reservation),
    path('delete_reservation/<str:reservation_id>', Staff_views.delete_reservation),
    path('delete_reservation_save', Staff_views.delete_reservation_save),

    #URLS STUDENTS
    path('student_home', Student_views.student_home),
    path('edit_student', Student_views.edit_student),
    path('edit_student_save', Student_views.edit_student_save),
    path('add_reservation_student/<str:id_bat>', Student_views.add_reservation),
    path('add_reservation_student/<str:id_bat>/<str:date>/<str:materiel>/<str:nb_pers>/<str:duree>', Student_views.add_reservation2),
    path('add_reservation_student/<str:id_bat>/<str:date>/<str:materiel>/<str:nb_pers>/<str:duree>/<str:heure_debut>', Student_views.add_reservation3),
    path('add_reservation_save_student', Student_views.add_reservation_save),
    path('manage_reservation_student/<str:etudiant_id>', Student_views.manage_reservation),
    path('delete_reservation_student/<str:reservation_id>', Student_views.delete_reservation),
    path('delete_reservation_save_student', Student_views.delete_reservation_save),
]
