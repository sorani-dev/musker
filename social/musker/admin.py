from django.contrib import admin
from django.contrib.auth.models import Group, User

from musker.models import Meep, Profile

# Unregister Groups
admin.site.unregister(Group)


# Mix Profile info into User info
class ProfileInline(admin.StackedInline):
    model = Profile


# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    # Just display username fields on admin page
    fields = ['username']
    inlines = [ProfileInline]


# Unregister initial User
admin.site.unregister(User)
# Reregister User
admin.site.register(User, UserAdmin)

# Register Meeps
admin.site.register(Meep)
