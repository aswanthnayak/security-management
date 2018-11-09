from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(user_details)
admin.site.register(log)
admin.site.register(worker_details)
admin.site.register(in_out)
admin.site.register(add_visitor)
admin.site.register(gatepass)
admin.site.register(student_service_details)
admin.site.register(laundry_details)
admin.site.register(faculty_service_details)
admin.site.register(book_cab_details)
admin.site.register(notify_gate)
admin.site.register(bring_groceries)
admin.site.register(medical_sevices)
admin.site.register(complaints)
admin.site.register(attendence_tracker)
admin.site.register(worker_tracker)
