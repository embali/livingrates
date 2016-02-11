from django.shortcuts import render
from django.views import generic
from django.template import RequestContext
from django.http import JsonResponse

from .models import Address


class Status(object):
    DONE = 'done'
    DETAILS = 'details'


class Web(generic.View):
    def get(self, request):
        return render(request, 'web/web.html', RequestContext(request, {}))


class Map(generic.View):
    def get(self, request):
        lat_left_get = float(request.GET['lat_left'])
        lng_lower_get = float(request.GET['lng_lower'])
        lat_right_get = float(request.GET['lat_right'])
        lng_upper_get = float(request.GET['lng_upper'])

        marks = []
        for mark in Address.objects.filter(latitude__gte=lat_left_get,
                                           latitude__lte=lat_right_get,
                                           longitude__gte=lng_lower_get,
                                           longitude__lte=lng_upper_get):
            marks.append(dict(lat=mark.latitude, lng=mark.longitude))
        return JsonResponse(dict(
            status=Status.DONE,
            marks=marks))


class Search(generic.View):
    def get(self, request):
        address_get = request.GET['address']
        lat_get = float(request.GET['lat'])
        lng_get = float(request.GET['lng'])

        address, created = Address.objects.get_or_create(address=address_get)
        if created:
            address.latitude = lat_get
            address.longitude = lng_get
            address.save()

        return JsonResponse(dict(
            status=Status.DONE,
            lat=address.latitude,
            lng=address.longitude))
