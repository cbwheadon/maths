from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from cat_test.models import CatTest, UserCatTest
from item_banks.models import ItemBank, ItemBankFractionQuestion
from fractionqs.forms import FractionForm

def start_test(request):
  #check for log in
  if not request.user.is_authenticated():
    return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
  user = request.user    
  #Get post info
  if request.method == 'GET':
    item_bank_id = request.GET['item_bank_id']
    cat_test_id = request.GET['cat_test_id']
    #Retrieve item bank
    item_bank = ItemBank.objects.get(pk=item_bank_id)
    cat_test = CatTest.objects.get(pk=cat_test_id)
    #Reset user_cat_test
    UserCatTest.objects.filter(user=user).delete()
    user_cat_test = UserCatTest()
    user_cat_test.user = user
    user_cat_test.item_bank = item_bank
    user_cat_test.cat_test = cat_test
    user_cat_test.save()
    
  #Create cat_test for user with info from item bank
  return render_to_response('start_test.html', {"item_bank": item_bank,"cat_test":cat_test})
  
def question(request):
  #check for log in
  if not request.user.is_authenticated():
    return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
  if request.method == 'GET':     
    user = request.user
    user_cat_test = UserCatTest.objects.get(user=user)
    #get next question
    cat_test_item = user_cat_test.nextQuestion()
    ibq = cat_test_item.item_bank_question
    #check item type
    if user_cat_test.item_bank.name == "Fractions":
      ifq = ItemBankFractionQuestion.objects.get(item_bank_question=ibq)
      q = ifq.fraction_bank_question.question
      form = FractionForm()
    return render_to_response('question.html',{"user_cat_test":user_cat_test,"question":q,'form': form})
  else:
    #process then redirect to feedback
    return HttpResponseRedirect('/feedback/')
	
def feedback(request):
  #check for log in
  if not request.user.is_authenticated():
    return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
  return render_to_response('feedback.html')