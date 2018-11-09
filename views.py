from django.http import HttpResponse
from .models import *
from django.shortcuts import render,redirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponseRedirect
import string
import random
import requests,json
global_name=None
global_studentid=None
global_ug=None
global_email=None
global_mobileno=None
#To authenicate Faculty,Worker login    

def login1(request):
	
	if request.method=='POST':
		
		try:
			x = user_details.objects.get(uid=request.POST['uid'])
			print(x.password)
		except(KeyError, user_details.DoesNotExist):
		
			template = loader.get_template('student/login.html')
			context = {
					'IDinvalid':"Invalid Username !",
				}
			return HttpResponse(template.render(context,request))
			
		if (request.POST['log']=='Login'):
			if request.POST['password'] != x.password:
				#PassWord is incorrect
				template = loader.get_template('student/login.html')
				context = {
						'Passwordinvalid':"Incorrect password!",
					}
				return HttpResponse(template.render(context,request))
				

			else:
				#Both UserID and Password are Correct
				k=x.did
				
				log.objects.all().delete()
				u = log()
				u.uid = x.uid
				u.name = x.name
				u.email_id=x.email_id
				u.block=x.block
				u.room_no=x.room_no
				u.mobile_no=x.mobile_no
				u.save()
				u = log.objects.all()[0].uid
				#print( log.objects.all()[0].email_id)
				
				if k==1:
					#To open Faculty home page
					template = loader.get_template('faculty/facultyhome.html')
					context = {
						'current' : u 
					}
					return HttpResponse(template.render(context,request))
				elif k==2:
					#To open Manger home page
					template = loader.get_template('manager/BH1.html')
					context = {
						'current' : u 
					}
					return HttpResponse(template.render(context,request))
				elif k==3:
					#To open Security home page
					template = loader.get_template('sworker/attendance.html')
					context = {
						'current' : u 
					}
					return HttpResponse(template.render(context,request))
		#Email is sent when you click forgot password			
		if (request.POST['log']=='Forgot Password'):
			print(x.email_id)
			#Random Password is generated
			paswd=''.join(random.choice(string.ascii_uppercase+string.ascii_lowercase+string.digits) for _ in range(8))
			print(paswd)
			subject='New Password'
			message='THIS MESSAGE IS SENT TO GIVE YOU TEMPORARY PASSWORD FOR LOGIN. New Password :- '+paswd
			from_email=settings.EMAIL_HOST_USER
			to_list = [x.email_id]
			email1=EmailMessage(subject,message,from_email,to_list)
			email1.send(fail_silently=False)
			#Password is updated in database
			user_details.objects.filter(email_id=x.email_id).update(password=paswd)
			template = loader.get_template('student/login.html')
			context = {
					'Check your Email',
				}
			return HttpResponse(template.render(context,request))
			
def studenthome1(request,token_id):
	global global_studentid
	global global_name
	global global_email
	global global_mobileno
	global global_ug
	
	#get token id from api
	print("This is token id {}".format(token_id))
	payload={'token':token_id,
	'secret':"2528e298230fa89724afb0052609123ce1860d214531ccad33e2e24fdbb2078e8254e2206a79734161e2f8da103b31721ce17b876364859fe09057990beea34d"
	}
	url="https://serene-wildwood-35121.herokuapp.com/oauth/getDetails"
	response=requests.post(url,data=payload)
	data=response.json()
	print("Details from API:",data)
	print("************************",data['student'][0]['Student_ID'])
	global_studentid=data['student'][0]['Student_ID']
	global_name=data['student'][0]['Student_First_Name']
	global_email=data['student'][0]['Student_Email']
	global_mobileno=data['student'][0]['Student_Mobile']
	global_ug=data['student'][0]['Student_Cur_YearofStudy']
	return HttpResponseRedirect('/gate')


def managerhome(request):
	return render(request,'manager/managernotifications.html')

def studenthome(request):
	global global_studentid
	gp=student_service_details.objects.all().filter(uid__exact=global_studentid)
	print(gp)
	
	gp1=book_cab_details.objects.all().filter(uid__exact=global_studentid)
	print(gp1)
	
	gp2=laundry_details.objects.all().filter(uid__exact=global_studentid)
	print(gp2)
	
	context={"student_service_detailss":gp,"book_cab_detailss":gp1,"laundry_detailss":gp2}	
	
	return render(request,'student/studenthome.html',context)
    


def login(request):
	return render(request,'student/login.html')
    

def gate_pass(request):
	global global_studentid
	#get data from table and show in html page
	gp=gatepass.objects.all().filter(uid__exact=global_studentid)
	print(gp)
	context={"gatepasss":gp}
	return render(request,'student/gatepass.html',context)
    

def sservices(request):
	    
	return render(request,'student/sservices.html')
    

def complaint(request):
	global global_studentid
	#get data from table and show in html page
	gp=complaints.objects.all().filter(uid__exact=global_studentid)
	print(gp)
	context={"complaintss":gp}
	return render(request,'student/complaint.html',context)
    
def profile(request):
	global global_studentid
	global global_name
	global global_email
	global global_mobileno
	global global_ug
	
	context={"uid":global_studentid,"name":global_name,"email":global_email,"mobileno":global_mobileno,"ug":global_ug}
	
	return render(request,'student/profile.html',context)
    
    
def details(request):
	return render(request,'student/details.html')
    
def facultyhome(request):
	return render(request,'faculty/facultyhome.html')
 
def getgatepass(request):
	global global_studentid
	global global_name
	#get data from form and fill in database
	if request.method=='POST':
		
		stud=gatepass()
		stud.uid=global_studentid
		stud.name=global_name
		stud.purpose=request.POST['purpose']
		stud.entry_created_by=global_studentid
		stud.last_modified_by=global_studentid
		print(stud)
		stud.save()
	#get data from table and show in html page
	gp=gatepass.objects.all().filter(uid__exact=global_studentid)
	print(gp)
	context={"gatepasss":gp}	
		
	return render(request,'student/gatepass.html',context)
		
def complaint1(request):
	global global_studentid
	#get data from form and fill in database
	if request.method=='POST':
		stud=complaints()
		stud.uid=global_studentid
		stud.block="BH2"
		stud.entry_created_by=global_studentid
		stud.last_modified_by=global_studentid
		stud.complaint=request.POST['complaint']
		
		stud.save()
	#get data from table and show in html page	
	gp=complaints.objects.all().filter(uid__exact=global_studentid)
	print(gp)
	context={"complaintss":gp}
	return render(request,'student/complaint.html',context)
	
def bh1(request):
	gpl=laundry_details.objects.all().filter(block__exact="BH1").filter(status=0)
	ll=gpl.count()
	gph=student_service_details.objects.all().filter(room_no__exact="BH1").filter(status=0)
	lh=gph.count()
	gp=complaints.objects.all().filter(block__exact="BH1").filter(status=0)
	l=gp.count()
	context={"complaintss":gp,"lenght":l,"house":gph,"lenh":lh,"laundry":gpl,"lenl":ll}
	return render(request,'manager/BH1.html',context)
	
def bh2(request):
	gpl=laundry_details.objects.all().filter(block__exact="BH2").filter(status=0)
	ll=gpl.count()
	gph=student_service_details.objects.all().filter(room_no__exact="BH2").filter(status=0)
	lh=gph.count()
	gp=complaints.objects.all().filter(block__exact="BH2").filter(status=0)
	l=gp.count()
	context={"complaintss":gp,"lenght":l,"house":gph,"lenh":lh,"laundry":gpl,"lenl":ll}
	return render(request,'manager/BH2.html',context)

def gh1(request):
	gpl=laundry_details.objects.all().filter(block__exact="GH1").filter(status=0)
	print(gpl)
	ll=gpl.count()
	gph=student_service_details.objects.all().filter(room_no__exact="GH1").filter(status=0)
	lh=gph.count()
	gp=complaints.objects.all().filter(block__exact="GH1").filter(status=0)
	l=gp.count()
	context={"complaintss":gp,"lenght":l,"house":gph,"lenh":lh,"laundry":gpl,"lenl":ll}
	return render(request,'manager/GH1.html',context)
	
def fbuilding(request):
	gpl=laundry_details.objects.all().filter(block__exact="FB").filter(status=0)
	ll=gpl.count()
	gph=student_service_details.objects.all().filter(room_no__exact="FB").filter(status=0)
	lh=gph.count()
	gp=complaints.objects.all().filter(block__exact="FB").filter(status=0)
	l=gp.count()
	context={"complaintss":gp,"lenght":l,"house":gph,"lenh":lh,"laundry":gpl,"lenl":ll}
	return render(request,'manager/facultybuilding.html',context)
	
def attendance(request):
	#get data from table and show in html page
	gp=gatepass.objects.all()
	print(gp)
	context={"gatepasss":gp}
	return render(request,'sworker/attendance.html',context)
	
def addvisitor(request):
	return render(request,'sworker/addvisitor.html')
	
def stuhouse(request):
	global global_studentid
	global global_name
	#get data from form and fill in database
	if request.method=='POST':
		
		stud=student_service_details()
		stud.uid=global_studentid
		stud.name=global_name
		stud.room_no="BH1"
		stud.date=request.POST['date']
		
		stud.tm=request.POST['time']
		stud.entry_created_by=global_studentid
		stud.last_modified_by=global_studentid
		stud.save()
	#get data from table and show in html page	
	gp=student_service_details.objects.all().filter(uid__exact=global_studentid)
	print(gp)
	context={"student_service_detailss":gp}	
	
	return render(request,'student/studenthome.html',context)
	
def bookcab(request):
	global global_studentid
	#get data from form and fill in database
	if request.method=='POST':
		stud=book_cab_details()
		stud.uid=global_studentid
		stud.entry_created_by=global_studentid
		stud.last_modified_by=global_studentid
		#stud.block=log.objects.all()[0].working_block
		
		stud.from_palce=request.POST['from_palce']
		stud.to_palce=request.POST['to_palce']
		stud.date=request.POST['date']
		
		stud.tm=request.POST['time']
		stud.date1=request.POST['date1']
		
		stud.time1=request.POST['time1']
		
		stud.save()
	#get data from table and show in html page	
	gp=book_cab_details.objects.all().filter(uid__exact=global_studentid)
	print(gp)
	context={"book_cab_detailss":gp}
	return render(request,'student/studenthome.html',context)
		
def laundry(request):
	global global_studentid
	#get data from form and fill in database
	if request.method=='POST':
		
		stud=laundry_details()
		stud.uid=global_studentid
		stud.room_no=request.POST['room_no']
		stud.date=request.POST['date']
		stud.block=request.POST['block']
		stud.tm=request.POST['time']
		stud.no_of_trousers=request.POST['trousers']
		stud.no_of_shirts=request.POST['shirts']
		stud.other=request.POST['other']
		stud.entry_created_by=global_studentid
		stud.last_modified_by=global_studentid
		stud.save()
	#get data from table and show in html page	
	gp=laundry_details.objects.all().filter(uid__exact=global_studentid)
	print(gp)
	context={"laundry_detailss":gp}	
	
	return render(request,'student/studenthome.html',context)
	
def addvisitor1(request):
	global global_studentid
	#get data from form and fill in database
	if request.method=='POST':
		
		stud=add_visitor()
		#stud.uid=global_studentid
		stud.name=request.POST['name']
		stud.mobile_no=request.POST['mobile_no']
		stud.purpose=request.POST['purpose']
		stud.address=request.POST['address']
		stud.entry_created_by=global_studentid
		stud.last_modified_by=global_studentid
		stud.save()
	#get data from table and show in html page	
	'''gp=add_visitor.objects.all()
	print(gp)
	context={"add_visitors":gp}'''	
	
	return render(request,'student/studenthome.html')
	
def searchby_date(request):
	global global_studentid
	if request.method=='POST':
		
		
		stud_date=request.POST['date']
		
	gp1=laundry_details.objects.all().filter(uid__exact=global_studentid).filter(date__exact=stud_date)
	gp=student_service_details.objects.all().filter(uid__exact=global_studentid).filter(date__exact=stud_date)
	context={"laundry_detailss ":gp1,"student_service_detailss":gp}
	return render(request,'student/studenthome.html',context)
		
