from django.contrib import admin
from django.urls import path
from school import views
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('upload-csv/', views.contact_upload, name ="contact_upload"),
    path('performance_upload1/', views.performance_upload, name ="performance_upload"),
    path('home/', views.index, name='index'),
    path('emailsent/', views.success, name="success"),
    path('map/', views.mapdetails, name='mapdetails'),
    path('table/', views.leaguetable, name ='leaguetable'),
    path('signup/',views.signup_view,name="signup"),
    path('login/',views.login_view,name="login"),
    path('add/',views.add_view,name="add"),
    path('deleteRow/',views.deleteRow_view,name="deleteRow"),
    path('mylist/',views.display_mylist,name="list"),
    path('logout/',views.logout_view,name="logout"),
    path('editprofile/',views.userUpdateDetails,name="editprofile"),
    path('detailschanged/',views.UserUpdateSuccess,name="UserUpdateSuccess"),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
