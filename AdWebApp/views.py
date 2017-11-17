import json
from django.shortcuts import render, render_to_response

from django.http import Http404, HttpResponse, HttpResponseRedirect
from util import token
from ElasticsearchDAO import *

def index(request):
    return render(request, 'index.html')

def post(request):
    paperInput = ''
    if (request.is_ajax() and request.POST):
        paperInput = token(request.POST.get('paper'))
    adsList = getAdsList(paperInput)
    context = {
        'adList': adsList
    }
    return HttpResponse(json.dumps(context, default=lambda o: o.__dict__, sort_keys=True, indent=4), content_type='application/json')

def result(request):
    return render(request, 'AdPage.html')
