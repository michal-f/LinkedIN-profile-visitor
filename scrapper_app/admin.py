# -*- coding: utf-8 -*-
from django.contrib import admin
from scrapper_app.models import ProfilePage, ListPage, RequestException


class VisitedProfilesAdmin(admin.ModelAdmin):

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(VisitedProfilesAdmin, self).get_search_results(request, queryset, search_term)

        queryset |= self.model.objects.filter(name__contains=search_term)
        return queryset, use_distinct

    list_display = ['name', 'response_code', 'visited_date', 'visited', 'url',]
    list_filter = ['parent']
    search_fields = ['name']
    date_hierarchy = 'visited_date'

class ListPagesAdmin(admin.ModelAdmin):
    list_display = ['response_code', 'visited_date', 'url']
    date_hierarchy = 'visited_date'


class RequestExceptionAdmin(admin.ModelAdmin):
    list_display = ['url', 'status_code', 'response_header', 'response_content']



class StatisticsAdmin(admin.ModelAdmin):
    list_display = ['visited_profiles', 'status_200', 'exceptions_count']


admin.site.register(ProfilePage, VisitedProfilesAdmin)
admin.site.register(ListPage, ListPagesAdmin)
admin.site.register(RequestException, RequestExceptionAdmin)
