from item_banks.models import ItemBank, Domain, QuestionType, ItemBankTemplate, ItemBankFractionQuestion
from cat_test.models import CatTestItem, UserCatTest
from centres.models import UserItemBank
from django.contrib.auth.models import User
from fractionqs.models import FractionQuestionBank, Oper

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

#Give the test some questions
#Create fraction question bank
fqb = FractionQuestionBank()
oper = Oper.objects.get(pk=1)
n = 20
st = 0
en = 10
name = "Test Bank"
negatives_allowed = True
fqb.generate(name,st,en,negatives_allowed,oper,n)
#Fill item bank from fraction question bank
item_bank.fill(fqb,"fractions")