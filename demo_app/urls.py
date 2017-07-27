from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'',views.signup_view),
    url(r'^register/success/',views.register_success)


]
