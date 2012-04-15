from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from cat_test.models import CatTest, UserCatTest, CatTestItem, CatTestItemFractionAnswer
from item_banks.models import ItemBank, ItemBankFractionQuestion
from fractionqs.models import FractionWithConstantForm, FractionWithConstant 
from centres.models import UserItemBank, UserItemBankProbabilities

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
    uib = UserItemBank.objects.get(user=user,item_bank=item_bank)	
    #New user_cat_test
    user_cat_test = UserCatTest()
    user_cat_test.user = user
    user_cat_test.item_bank = item_bank
    user_cat_test.cat_test = cat_test
    user_cat_test.ability = uib.ability
    user_cat_test.stand_dev = uib.ability_stand_dev	
    user_cat_test.save()
    
  #Create cat_test for user with info from item bank
  return render_to_response('start_test.html', {"item_bank": item_bank,"cat_test":cat_test})
  
def question(request):
  #check for log in
  if not request.user.is_authenticated():
    return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
  user = request.user
  user_cat_test = UserCatTest.objects.filter(user=user)
  user_cat_test = user_cat_test.order_by('-id')[0]
  if request.method == 'GET':
  #get next question
    cat_test_item = user_cat_test.nextQuestion()
    ibq = cat_test_item.item_bank_question    
  #check item type
    if user_cat_test.item_bank.question_type.name == "fraction":
      ifq = ItemBankFractionQuestion.objects.get(item_bank_question=ibq)
      q = ifq.fraction_bank_question.question
      form = FractionWithConstantForm()    
    return render_to_response('question.html',{"user_cat_test":user_cat_test,"question":q,'form': form},context_instance=RequestContext(request))
  else:
    #process then redirect to feedback
    #get last item
    cat_test_item = CatTestItem.objects.filter(user_cat_test=user_cat_test)
    cat_test_item = cat_test_item.order_by('-id')[0]
    ibq = cat_test_item.item_bank_question     
    if user_cat_test.item_bank.question_type.name == "fraction":
      f = FractionWithConstantForm(request.POST)
      ifq = ItemBankFractionQuestion.objects.get(item_bank_question=ibq)
      q = ifq.fraction_bank_question.question
      answer = FractionWithConstant()
      if 'const' in request.POST and request.POST['const']:         
        try:
          answer.const = int(request.POST['const'])
        except:
          answer.const = 0        
      else:
        answer.const = 0
      if 'num' in request.POST and request.POST['num']:    
        try:
          answer.num = int(request.POST['num'])
        except:
          answer.num = 0        
      else:
        answer.num = 0
      if 'denom' in request.POST and request.POST['denom']:     
        try:
          answer.denom = int(request.POST['denom'])
        except:
          answer.denom = 1               
      else:
        answer.denom = 1      
      answer.save()
      ctifa = CatTestItemFractionAnswer()
      ctifa.cat_test_item = cat_test_item
      ctifa.fraction = answer
      ctifa.save()
    if answer == q.answer:
      correct = 1
    else:
      correct = 0
    if 'time' in request.POST and request.POST['time']:       
      time_taken = request.POST['time']
    else:
      time_taken = 0       
    cat_test_item.time_taken = time_taken
    cat_test_item.correct = correct
    cat_test_item.save()
    user_cat_test.simAbility()	
    return HttpResponseRedirect('/feedback/')
    
def feedback(request):
  #check for log in
  if not request.user.is_authenticated():
    return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
  user = request.user
  user_cat_test = UserCatTest.objects.filter(user=user)
  user_cat_test = user_cat_test.order_by('-id')[0]
  cat_test_item = CatTestItem.objects.filter(user_cat_test=user_cat_test)    
  cat_test_item = cat_test_item.order_by('-id')[0]
  ibq = cat_test_item.item_bank_question
  if user_cat_test.item_bank.question_type.name == "fraction":
    ctifa = CatTestItemFractionAnswer.objects.get(cat_test_item=cat_test_item)
    response = ctifa.fraction
    ifq = ItemBankFractionQuestion.objects.get(item_bank_question=ibq)
    answer = ifq.fraction_bank_question.question.answer
  end_test = user_cat_test.endTest()
  user_item_bank = UserItemBank.objects.get(user=user,item_bank=user_cat_test.item_bank)
  probs = UserItemBankProbabilities.objects.filter(user_item_bank=user_item_bank)  
  if end_test:
    end_now = 1
  else:
    end_now = 0	
  return render_to_response('feedback.html',{'cat_test_item':cat_test_item,'answer':answer,'response':response,'user_cat_test':user_cat_test,'end_test':end_now,'probs':probs})
  
def end_test(request):
  if not request.user.is_authenticated():
    return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
  user = request.user
  user_cat_test = UserCatTest.objects.filter(user=user)
  if len(user_cat_test)>0:
    user_cat_test = user_cat_test.order_by('-id')[0]
    uib = UserItemBank.objects.get(user=user,item_bank=user_cat_test.item_bank)
    uib.update(user_cat_test)
    probs = UserItemBankProbabilities.objects.filter(user_item_bank=uib)  
  
    return render_to_response('end_test.html',{'user_cat_test':user_cat_test,'probs':probs})
  else:
    return render_to_response('end_test.html',{'error':'No Test Found'})  