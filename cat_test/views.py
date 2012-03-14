from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from cat_test.models import CatTest
from item_banks.models import ItemBank

def start_test(request):
      #check for log in
  if not request.user.is_authenticated():
    return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
  #Get post info
  if request.method == 'POST':
    item_bank_id = request.POST['item_bank_id']
    cat_test_id = request.POST['cat_test_id']
    #Retrieve item bank
    item_bank = ItemBank.objects.get(pk=item_bank_id)
    cat_test = CatTest.objects.get(pk=cat_test_id)
  #Create cat_test for user with info from item bank
  return render_to_response('start_test.html', {"item_bank": item_bank,"cat_test":cat_test})