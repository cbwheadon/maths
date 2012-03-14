from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from item_banks.models import ItemBank
from centres.models import UserItemBank
from cat_test.models import CatTest

def welcome(request):
    #check for log in
    if not request.user.is_authenticated():
      return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
    user = request.user  
    user_banks = UserItemBank.objects.filter(user=user)
    cat_tests = CatTest.objects.all()    
    return render_to_response('user_item_banks.html',{'user_banks':user_banks,'cat_tests':cat_tests})
