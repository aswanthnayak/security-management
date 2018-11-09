from django.urls import path,re_path
from django.conf.urls import include,url             
from . import views
from .views import *
urlpatterns = [
	#API Home Page
	url('studenthome.html/(?P<token_id>.+)$',views.studenthome1,name="studenthome1"),
	path('', views.studenthome, name='studenthome'),
	url(r'^studenthome',views.studenthome),
	#For Forms
	url(r'^login1$',views.login1,name="login1"),
	url(r'^laundry$',views.laundry,name="laundry"),
	url(r'^bookcab$',views.bookcab,name="bookcab"),
	url(r'^addvisitor1$',views.addvisitor1,name="addvisitor1"),
	url(r'^complaint1$',views.complaint1,name="complaint1"),
	url(r'^getgatepass$',views.getgatepass,name="getgatepass"),
	url(r'^stuhouse$',views.stuhouse,name="stuhouse"),
	url(r'^searchby_date$',views.searchby_date,name="searchby_date"),
	#
	url(r'^sservices',views.sservices),
	url(r'^gatepass',views.gate_pass),
	url(r'^complaint',views.complaint),
	url(r'^details',views.details),
	url(r'^profile',views.profile),
	#Login for Faculty,Worker
	url(r'^login',views.login),
	#Manager Pages
	url(r'^managernotifications',views.managerhome,name="managerhome"),
	url(r'^BH1',views.bh1),
	url(r'^BH2',views.bh2),
	url(r'^GH1',views.gh1),
	url(r'^facultybuilding',views.fbuilding),
	#Faculty Pages
	url(r'^facultyhome',views.facultyhome),
	
	#Security Pages
	url(r'^attendance',views.attendance),
	url(r'^addvisitor',views.addvisitor),
	
]

