from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Talk, Comment

admin.site.unregister(Group)
admin.site.unregister(User)


class ProfileInLine(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username", "email"]
    inlines = [ProfileInLine]


admin.site.register(User, UserAdmin)
admin.site.register(Talk)
admin.site.register(Comment)
