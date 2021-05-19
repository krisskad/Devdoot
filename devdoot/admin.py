from django.contrib import admin
from .models import ExtendedUser, ProblemReport, ProblemType, PublicProblem, States, Cities, Countries, SolvedProblem

# from django.contrib.auth.models import User, Group
# admin.site.unregister(User)
# admin.site.unregister(Group)


# Register your models here.
class StatesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country_id')


class CitiesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'state_id')


class CountriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'sortname', 'name', 'phonecode')


class ProblemTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'problem_title', 'problem_title_m', 'problem_title_h')


class PublicProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'mobile',
                    'state', 'city',
                    'problem_type', 'description', 'timestamp')


class SolvedProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'solved_problem', 'is_solved', 'solved_by', 'when')


# Register your models here.
class ExtendedUserAdmin(admin.ModelAdmin):
    list_display = ('user',
                    'state', 'city', 'address',
                    'profession', 'gender', 'account_type')


class ProblemReportAdmin(admin.ModelAdmin):
    list_display = ('submitted_by',
                    'title', 'description',
                    'reported_to', 'timestamp')


admin.site.register(States, StatesAdmin)
admin.site.register(Cities, CitiesAdmin)
admin.site.register(Countries, CountriesAdmin)
admin.site.register(ProblemType, ProblemTypeAdmin)
admin.site.register(PublicProblem, PublicProblemAdmin)
admin.site.register(SolvedProblem, SolvedProblemAdmin)
admin.site.register(ExtendedUser, ExtendedUserAdmin)
admin.site.register(ProblemReport, ProblemReportAdmin)

