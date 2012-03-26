from django.test import TestCase
from centres.models import Centre, Candidate
from item_banks.models import ItemBank, Domain, ItemBankQuestion, ItemBankFractionQuestion, QuestionType, ItemBankTemplate
from fractionqs.models import FractionQuestionBank, Oper, FractionBankQuestion
import datetime
from django.contrib.auth.models import User
from django.test.client import Client
from functional_tests import ROOT

class TestItemBankTemplate(TestCase):
    def test_create_and_save(self):
      ibt = ItemBankTemplate()
      ibt.name = "fractions.html"
      ibt.save()
      ibts = ItemBankTemplate.objects.all()[0]
      self.assertEquals(ibts.name,"fractions.html")  

class TestQuestionType(TestCase):
    def test_create_and_save_question_type(self):
      qtype = QuestionType()
      qtype.name = "fraction"
      qtype.save()
      qt = QuestionType.objects.all()[0]
      self.assertEquals(qt.name,"fraction")

class TestItemBank(TestCase):
    def test_create_and_save_item_bank(self):
      domain = Domain.objects.get(name="Number")
      item_bank = ItemBank()
      item_bank.name = "Fractions"
      item_bank.topic = "Addition"
      item_bank.domain = domain
      item_bank.template = ItemBankTemplate.objects.get(pk=1)
      item_bank.question_type = QuestionType.objects.get(pk=1)
      item_bank.save()
      n = len(ItemBank.objects.all())
      self.assertEquals(n,1)
      ib = ItemBank.objects.all()[0]
      self.assertEquals(unicode(ib),"Fractions")
      self.assertEquals(ib.topic,"Addition")
      self.assertEquals(ib.template.name,"fractions.html")
      
class TestItemBankQuestion(TestCase):
    def test_can_create_and_save_item_bank_question(self):
      fixtures = ['initial_data.yaml']    
      domain = Domain.objects.get(name="Number")
      item_bank = ItemBank()
      item_bank.name = "Fractions"
      item_bank.topic = "Addition"
      item_bank.domain = domain
      item_bank.question_type = QuestionType.objects.get(pk=1)
      item_bank.template = ItemBankTemplate.objects.get(pk=1)
      item_bank.save()
      ibq = ItemBankQuestion()
      ibq.item_bank = item_bank
      ibq.usage = 0
      ibq.difficulty = 0
      ibq.sd_difficulty = 0
      ibq.discrimination = 1
      ibq.save()
      ibq = ItemBankQuestion.objects.all()[0]
      self.assertEquals(ibq.item_bank,item_bank)
      self.assertEquals(ibq.usage,0)
      self.assertEquals(ibq.difficulty,0)
      self.assertEquals(ibq.sd_difficulty,0)
      self.assertEquals(ibq.discrimination,1)
      
class TestItemBankFractionQuestion(TestCase):
    def test_can_create_link_btwn_item_bank_and_fraction_bank(self):
      fixtures = ['initial_data.yaml']
      #create domain
      domain = Domain.objects.get(name="Number")
      #Create item bank
      item_bank = ItemBank()
      item_bank.name = "Fractions"
      item_bank.topic = "Addition"
      item_bank.domain = domain
      item_bank.question_type = QuestionType.objects.get(pk=1)
      item_bank.template = ItemBankTemplate.objects.get(pk=1)
      item_bank.save()
      #Create item bank question
      ibq = ItemBankQuestion()
      ibq.item_bank = item_bank
      ibq.usage = 0
      ibq.difficulty = 0
      ibq.sd_difficulty = 0
      ibq.discrimination = 1
      ibq.save()
      #Create fraction question bank
      fqb = FractionQuestionBank()
      oper = Oper.objects.get(pk=1)
      n = 20
      st = 0
      en = 10
      name = "Test Bank"
      negatives_allowed = True
      fqb.generate(name,st,en,negatives_allowed,oper,n)
      fbqs = FractionBankQuestion.objects.filter(fraction_question_bank=fqb)
      #Link item bank and question bank
      ibfb = ItemBankFractionQuestion()
      ibfb.item_bank_question = ibq
      ibfb.fraction_bank_question = fbqs[0]
      ibfb.save()
      ibfbs = ItemBankFractionQuestion.objects.all()[0]
      self.assertEquals(ibfbs.item_bank_question,ibq)
      self.assertEquals(ibfbs.fraction_bank_question,fbqs[0])
      
    def test_can_fill_item_bank_with_fraction_bank(self):
      fixtures = ['initial_data.yaml']      
      #create domain
      domain = Domain.objects.get(name="Number")
      #Create item bank
      item_bank = ItemBank()
      item_bank.name = "Fractions"
      item_bank.topic = "Addition"
      item_bank.domain = domain
      item_bank.question_type = QuestionType.objects.get(pk=1)
      item_bank.template = ItemBankTemplate.objects.get(pk=1)
      item_bank.save()
      #Create fraction question bank
      fqb = FractionQuestionBank()
      oper = Oper.objects.get(pk=1)
      n = 20
      st = 0
      en = 10
      name = "Test Bank"
      negatives_allowed = True
      fqb.generate(name,st,en,negatives_allowed,oper,n)
      fbqs = FractionBankQuestion.objects.filter(fraction_question_bank=fqb)
      #Fill item bank from fraction question bank
      item_bank.fill(fqb,"fractions")
      ibqs = ItemBankQuestion.objects.filter(item_bank=item_bank)
      self.assertEquals(len(ibqs),len(fbqs))