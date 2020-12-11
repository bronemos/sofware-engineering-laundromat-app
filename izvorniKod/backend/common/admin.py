from django.contrib import admin
from common.models import User, Review, Laundry, Machine, Appointment, Post


admin.site.register(User)
admin.site.register(Laundry)
admin.site.register(Appointment)
admin.site.register(Post)
admin.site.register(Review)
admin.site.register(Machine)
