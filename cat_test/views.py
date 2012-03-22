from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from cat_test.models import CatTest, UserCatTest, CatTestItem, CatTestItemFractionAnswer
from item_banks.models import ItemBank, ItemBankFractionQuestion
from fractionqs.models import FractionWithConstantForm, FractionWithConstant 

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
    #New user_cat_test
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
    return render_to_response('question.html',{"user_cat_test":user_cat_test,"question":q,'form': form})
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
      answer.const = request.POST['const']
      answer.denom = request.POST['num']
      answer.num = request.POST['denom']
      answer.save()
      ctifa = CatTestItemFractionAnswer()
      ctifa.cat_test_item = cat_test_item
      ctifa.fraction = answer
      ctifa.save()
    response = f.save(commit=False)
        
    if response == q.answer:
      correct = 1
    else:
      correct = 0
    time_taken = request.POST['time']      
    user_cat_test.updateAbility(correct,time_taken)
    cat_test_item.time_taken = time_taken
    cat_test_item.correct = correct
    cat_test_item.save()
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
  return render_to_response('feedback.html',{'cat_test_item':cat_test_item,'answer':answer,'response':response,'user_cat_test':user_cat_test,'end_test':end_test})
  
def end_test(request):
  if not request.user.is_authenticated():
    return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
  user = request.user
  return render_to_response('end_test.html')