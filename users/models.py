from django.db import models
import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
import StringIO
import tests
from django.views.decorators.csrf import csrf_exempt
import unittest
from django.template import RequestContext

SUCCESS               =   1  # : a success
ERR_BAD_CREDENTIALS   =  -1  # : (for login only) cannot find the user/password pair in the database
ERR_USER_EXISTS       =  -2  # : (for add only) trying to add a user that already exists
ERR_BAD_USERNAME      =  -3  # : (for add, or login) invalid user name (only empty string is invalid for now)
ERR_BAD_PASSWORD      =  -4

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length = 128)
    password = models.CharField(max_length = 128)
    count = models.IntegerField()

@csrf_exempt
def client(request):
    return render_to_response('client.html',{},context_instance=RequestContext(request))

@csrf_exempt
def login(request):
    data = json.loads(request.body)
    user = data["user"]
    pw = data["password"]
    if (user == ""):
        return HttpResponse(json.dumps({"errCode" : ERR_BAD_USERNAME}), content_type="application/json")
    userExists = User.objects.filter(username__exact = user).exists()
    if (userExists == False):
        return HttpResponse(json.dumps({"errCode" : ERR_BAD_CREDENTIALS}), content_type="application/json")
    if (userExists == True):
        key = User.objects.get(username__exact = user)
        if (pw != key.password):
            return HttpResponse(json.dumps({"errCode" : ERR_BAD_CREDENTIALS}), content_type="application/json")
        count = key.count
        User.objects.get(username__exact = user).delete()
        key = User(username=user, password=pw, count=count+1)
        key.save()
        return HttpResponse(json.dumps({"errCode" : SUCCESS, "count" : key.count}), content_type="application/json")

@csrf_exempt
def add(request):
    data = json.loads(request.body)
    user = data["user"]
    pw = data["password"]
    key = User.objects.filter(username__exact = user).exists()
    if (key == True):
        return HttpResponse(json.dumps({"errCode" : ERR_USER_EXISTS}), content_type="application/json")
    if (user == "" or len(user)>128):
        return HttpResponse(json.dumps({"errCode" : ERR_BAD_USERNAME}), content_type="application/json")
    if (len(pw)>128):
        return HttpResponse(json.dumps({'errCode' : ERR_BAD_PASSWORD}), content_type="application/json")
    newuser = User(username=user, password=pw, count=1)
    newuser.save()
    return HttpResponse(json.dumps({"errCode" : SUCCESS, "count" : newuser.count}), content_type="application/json")

@csrf_exempt
def TESTAPI_resetFixture(request):
    User.objects.all().delete()
    return HttpResponse(json.dumps({"errCode" : SUCCESS}), content_type="application/json")

@csrf_exempt
def TESTAPI_unitTests(request):
    buffer = StringIO.StringIO()
    suite = unittest.TestLoader().loadTestsFromTestCase(tests.Tests)
    result = unittest.TextTestRunner(stream = buffer, verbosity = 2).run(suite)

    results = {"totalTests": result.testsRun, "nrFailed": len(result.failures), "output": buffer.getvalue()}
    return HttpResponse(json.dumps(results), content_type = "application/json")

