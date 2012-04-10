from item_banks.models import ItemBank, Domain, QuestionType, ItemBankTemplate, ItemBankFractionQuestion, Threshold, Grade
from cat_test.models import CatTestItem, UserCatTest
from centres.models import UserItemBank, UserItemBankProbabilities
from django.contrib.auth.models import User
from fractionqs.models import FractionQuestionBank, Oper

#Clean up
ItemBank.objects.all().delete()
UserItemBank.objects.all().delete()
FractionQuestionBank.objects.all().delete()
Threshold.objects.all().delete()
UserItemBankProbabilities.objects.all().delete()

#Set up an item bank and associate with user
user = User.objects.get(username="user") 
domain = Domain.objects.get(name="Number")
item_bank = ItemBank()
item_bank.name = "Fractions"
item_bank.topic = "Addition"
item_bank.domain = domain
item_bank.template = ItemBankTemplate.objects.get(pk=1)
item_bank.question_type = QuestionType.objects.get(pk=1)
item_bank.save()
user_item_bank = UserItemBank()
user_item_bank.user = user
user_item_bank.item_bank = item_bank
user_item_bank.save()

#Set thresholds
grd = Grade.objects.get(name="A")
thresh = Threshold()
thresh.grade = grd
thresh.item_bank = item_bank
thresh.ability = 1      
thresh.save()
grd = Grade.objects.get(name="C")
thresh = Threshold()
thresh.grade = grd
thresh.item_bank = item_bank
thresh.ability = -1      
thresh.save()
user_item_bank.probabilities()

#Give the test some questions
#Create fraction question bank
fqb = FractionQuestionBank()
oper = Oper.objects.get(pk=1)
n = 10
st = 0
en = 10
name = "Test Bank 20 Addition"
negatives_allowed = False
fqb.generate(name,st,en,negatives_allowed,oper,n)
#Fill item bank from fraction question bank
item_bank.fill(fqb,"fractions")

item_bank = ItemBank()
item_bank.name = "Fractions"
item_bank.topic = "Subtraction"
item_bank.domain = domain
item_bank.template = ItemBankTemplate.objects.get(pk=1)
item_bank.question_type = QuestionType.objects.get(pk=1)
item_bank.save()
user_item_bank = UserItemBank()
user_item_bank.user = user
user_item_bank.item_bank = item_bank
user_item_bank.save()

#Set thresholds
grd = Grade.objects.get(name="A")
thresh = Threshold()
thresh.grade = grd
thresh.item_bank = item_bank
thresh.ability = 1      
thresh.save()
grd = Grade.objects.get(name="C")
thresh = Threshold()
thresh.grade = grd
thresh.item_bank = item_bank
thresh.ability = -1      
thresh.save()
user_item_bank.probabilities()

#Create fraction question bank
fqb = FractionQuestionBank()
oper = Oper.objects.get(pk=2)
n = 10
st = 0
en = 10
name = "Test Bank 20 Subtraction"
negatives_allowed = False
fqb.generate(name,st,en,negatives_allowed,oper,n)

#Fill item bank from fraction question bank
item_bank.fill(fqb,"fractions")

item_bank = ItemBank()
item_bank.name = "Fractions"
item_bank.topic = "Multiplication"
item_bank.domain = domain
item_bank.template = ItemBankTemplate.objects.get(pk=1)
item_bank.question_type = QuestionType.objects.get(pk=1)
item_bank.save()
user_item_bank = UserItemBank()
user_item_bank.user = user
user_item_bank.item_bank = item_bank
user_item_bank.save()

#Set thresholds
grd = Grade.objects.get(name="A")
thresh = Threshold()
thresh.grade = grd
thresh.item_bank = item_bank
thresh.ability = 1      
thresh.save()
grd = Grade.objects.get(name="C")
thresh = Threshold()
thresh.grade = grd
thresh.item_bank = item_bank
thresh.ability = -1      
thresh.save()
user_item_bank.probabilities()

#Create fraction question bank
fqb = FractionQuestionBank()
oper = Oper.objects.get(pk=3)
n = 10
st = 0
en = 10
name = "Test Bank 20 Multiplication"
negatives_allowed = True
fqb.generate(name,st,en,negatives_allowed,oper,n)

#Fill item bank from fraction question bank
item_bank.fill(fqb,"fractions")

item_bank = ItemBank()
item_bank.name = "Fractions"
item_bank.topic = "Division"
item_bank.domain = domain
item_bank.template = ItemBankTemplate.objects.get(pk=1)
item_bank.question_type = QuestionType.objects.get(pk=1)
item_bank.save()
user_item_bank = UserItemBank()
user_item_bank.user = user
user_item_bank.item_bank = item_bank
user_item_bank.save()

#Set thresholds
grd = Grade.objects.get(name="A")
thresh = Threshold()
thresh.grade = grd
thresh.item_bank = item_bank
thresh.ability = 1      
thresh.save()
grd = Grade.objects.get(name="C")
thresh = Threshold()
thresh.grade = grd
thresh.item_bank = item_bank
thresh.ability = -1      
thresh.save()
user_item_bank.probabilities()

#Create fraction question bank
fqb = FractionQuestionBank()
oper = Oper.objects.get(pk=4)
n = 10
st = 0
en = 10
name = "Test Bank 20 Division"
negatives_allowed = True
fqb.generate(name,st,en,negatives_allowed,oper,n)

#Fill item bank from fraction question bank
item_bank.fill(fqb,"fractions")