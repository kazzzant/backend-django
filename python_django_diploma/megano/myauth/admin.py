from django.contrib import admin

from .models import Avatar, Profile

admin.site.register(Avatar)
admin.site.register(Profile)


# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = 'fullName', 'email', 'phone', 'user'
#     # search_fields = 'fullName', 'user'
#
#     def get_queryset(self, request):
#         return Profile.objects.select_related('user').prefetch_related('avatar')
