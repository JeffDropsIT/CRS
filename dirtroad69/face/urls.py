from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required, permission_required
app_name = 'face'

urlpatterns = [

    url(r'^$', login_required(views.IndexView.as_view()), name='index'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^img/$', views.classification, name='classify'),
    url(r'^retrain/$', views.retrain, name='retrain'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<pk>[0-9])/$', login_required(views.DetailView.as_view()), name='detail'),
    url(r'cow/add/$', views.CowCreate.as_view(), name='cow-add'),
   # url(r'cow/get/$', login_required(views.ClassifyView.as_view()), name='classify'),
    url(r'cow/(?P<pk>[0-9])/$', views.CowUpdate.as_view(), name='cow-update'),
    url(r'cow/(?P<pk>[0-9])/delete/$', views.CowDelete.as_view(), name='cow-delete')
]
