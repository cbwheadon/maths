from django.test import TestCase
from maths.fractionqs.models import FractionWithConstant, FractionQuestion, Oper, FractionBank, FractionBankFraction, FractionBankQuestion, FractionQuestionBank, FractionWithConstantForm
import datetime

def createFraction(i,oper):
      if oper.oper_name == "+":      
        fs = ((3,1,2),(5,1,3)),((0,4,7),(0,2,5)),((3,2,3),(2,5,7)),((-3,3,4),(0,1,2))
        f_ans = (8,5,6),(0,34,35),(6,8,21),(-3,1,4)
      if oper.oper_name == "*":      
        fs = ((0,-1,3),(0,9,16)),((1,1,2),(2,1,5)),((-1,5,9),(-2,1,7)),((-2,3,5),(1,1,4))
        f_ans = (0,-3,16),(3,3,10),(3,1,3),(-3,1,4)        
      if oper.oper_name == "/":
        fs = ((0,1,2),(0,1,6)),((0,1,2),(3,0,1)),((2,1,2),(1,1,10)),((0,-3,4),(0,1,4))
        f_ans = (3,0,1),(0,1,6),(2,3,11),(-3,0,0)  
      if oper.oper_name == "-":
        fs = ((0,3,4),(0,1,4)),((15,3,4),(8,5,6)),((4,3,5),(1,9,10)),((0,1,2),(0,1,2))
        f_ans = (0,1,2),(6,11,12),(2,7,10),(0,1,0)
      q1 = FractionWithConstant()
      q1.const = fs[i][0][0]
      q1.num = fs[i][0][1]
      q1.denom = fs[i][0][2]
      q2 = FractionWithConstant()
      q2.const = fs[i][1][0]
      q2.num = fs[i][1][1]
      q2.denom = fs[i][1][2]
      ans = FractionWithConstant()
      ans.const = f_ans[i][0]
      ans.num = f_ans[i][1]
      ans.denom = f_ans[i][2]
      return[q1,q2,ans]

class TestOper(TestCase):         
    def test_init(self):
      opers = Oper.objects.all()
      self.assertEquals(len(opers),4)
             
class TestCreateFraction(TestCase):
    def test_basic_creation(self):
      fq = FractionWithConstant()
      fq.const = 1
      fq.num = 2
      fq.denom = 3
      fq.save()
      fqs = FractionWithConstant.objects.all()
      fq = fqs[0]
      self.assertEquals(fq.const,1)      
      self.assertEquals(fq.num,2)      
      self.assertEquals(fq.denom,3)

    def test_two_fractions_equal(self):
      fq1 = FractionWithConstant()
      fq1.const = 1
      fq1.num = 4
      fq1.denom = 2
      fq1.save()
      fq2 = FractionWithConstant()
      fq2.const = 2
      fq2.num = 1
      fq2.denom = 1
      fq2.save()
      tst = fq1 == fq2
      self.assertEquals(tst,True)
      
    def test_two_fractions_not_equal(self):
      fq1 = FractionWithConstant()
      fq1.const = 1
      fq1.num = 4
      fq1.denom = 2
      fq1.save()
      fq2 = FractionWithConstant()
      fq2.const = 2
      fq2.num = 1
      fq2.denom = 2
      fq2.save()
      tst = fq1 == fq2
      self.assertEquals(tst,False)   
      
    def test_zero_division_error(self):
      fq1 = FractionWithConstant()
      fq1.const = 1
      fq1.num = 4
      fq1.denom = 2
      fq1.save()
      fq2 = FractionWithConstant()
      fq2.const = 2
      fq2.num = 0
      fq2.denom = 0
      fq2.save()
      tst = fq1 == fq2
      self.assertEquals(tst,'ZeroDivisionError')  
      
    def test_simplest_form(self):
      fq1 = FractionWithConstant()
      fq1.const = -2
      fq1.num = 3
      fq1.denom = 2
      fq1.save()
      fq2 = fq1.simplest_form()
      self.assertEquals(fq2.const, -3)
      self.assertEquals(fq2.num, 1)      
      self.assertEquals(fq2.denom, 2)

    def test_operation(self):
      my_opers = Oper.objects.all()
      for my_oper in my_opers:     
        for i in range(0,3):
          fs = createFraction(i,my_oper)
          fq1 = fs[0]
          fq2 = fs[1]
          my_ans = fs[2]
          ans = fq1.oper(fq2,my_oper)
          self.assertEquals(ans.const, my_ans.const)
          self.assertEquals(ans.num, my_ans.num)
          self.assertEquals(ans.denom, my_ans.denom)            
        
class TestFractionsQuestion(TestCase):
    def test_creation(self):
      fq = FractionQuestion()
      oper = Oper.objects.get(pk=1)
      fs = createFraction(0,oper)
      fq.f1 = fs[0]
      fq.f2 = fs[1]
      fq.oper = Oper.objects.get(pk=1)
      fq.answer = fs[2]
      
    def test_equality(self):
      oper = Oper.objects.get(pk=1)
      fq1 = FractionQuestion()
      fs = createFraction(0,oper)
      fq1.f1 = fs[0]
      fq1.f2 = fs[1]
      fq1.oper = Oper.objects.get(pk=1)
      fq1.answer = fs[2]
      fq2 = FractionQuestion()      
      fs = createFraction(1,oper)
      fq2.f1 = fs[0]
      fq2.f2 = fs[1]
      fq2.oper = Oper.objects.get(pk=1)
      fq2.answer = fs[2]
      eq = fq1 == fq2
      self.assertEquals(eq, False)
      
class TestFractionBank(TestCase):
    def test_creation(self):
      fb = FractionBank()
      fb.name = "Bank 1"
      fb.date_created = datetime.date(2012,03,07)
      fb.save()
      fbs = FractionBank.objects.all()
      fb = fbs[0]
      self.assertEquals(fb.name,"Bank 1")
      self.assertEquals(fb.date_created,datetime.date(2012,03,07))
    
    def test_generate_question(self):
      fb = FractionBank()
      fb.name = "Bank 1"
      fb.date_created = datetime.date(2012,03,07)
      fb.save()
      st = 0
      en = 9
      i = fb.fill(st,en)
      oper = Oper.objects.get(pk=1)     
      q = fb.generate_question(oper)
      self.assertEquals(isinstance(q, FractionQuestion),True)
      
class TestFractionBankFraction(TestCase):
    def test_creation(self):
      fb = FractionBank()
      fb.name = "Bank 1"
      fb.date_created = datetime.date(2012,03,07)
      fb.save()
      oper = Oper.objects.get(pk=1)
      fbqs = createFraction(1,oper)
      fbq = fbqs[0]
      fbq.save()
      fbf = FractionBankFraction()
      fbf.fraction_bank = fb
      fbf.fraction = fbq
      fbf.save()
      fbfs = FractionBankFraction.objects.all()
      fbf = fbfs[0]
      self.assertEquals(fbf.fraction_bank.name,"Bank 1")
      self.assertEquals(fbf.fraction,fbq)
    
    def test_fill_bank(self):
      fb = FractionBank()
      fb.name = "Bank 1"
      fb.date_created = datetime.date(2012,03,07)
      fb.save()
      st = 0
      en = 10
      i = fb.fill(st,en)
      print i
      fb = FractionBankFraction.objects.all()
      self.assertEquals(len(fb),i)
      #for j in range(0,len(fb)):
        #print fb[j].fraction
        
    def test_fill_bank_with_negatives(self):
      fb = FractionBank()
      fb.name = "Bank 1"
      fb.date_created = datetime.date(2012,03,07)
      fb.save()
      st = 0
      en = 10
      fb.fill(st,en)
      
      fbn = FractionBank()
      fbn.name = "Bank 2"
      fbn.date_created = datetime.date(2012,03,07)
      fbn.save()
      st = 0
      en = 10
      fbn.fill(st,en,True)
      
      fb1 = FractionBankFraction.objects.filter(fraction_bank=fb)
      fb2 = FractionBankFraction.objects.filter(fraction_bank=fbn)
      
      self.assertEquals(2 * len(fb1),len(fb2))
      #for j in range(0,len(fb)):
        #print fb[j].fraction
        
class TestFractionBankQuestion(TestCase):
    def test_creation(self):
      fb = FractionBank()
      fb.name = "Bank 1"
      fb.date_created = datetime.date(2012,03,07)
      fb.save()
      st = 0
      en = 10
      i = fb.fill(st,en)
      fbfs = FractionBankFraction.objects.all()
      
      fqb = FractionQuestionBank()
      fqb.name = "Addition 100"
      fqb.fraction_bank = fb
      fqb.date_created = datetime.date(2012,03,07)
      fqb.save()
      
      fq = FractionQuestion()
      fq.f1 = fbfs[0].fraction
      fq.f2 = fbfs[1].fraction
      oper = Oper.objects.get(pk=1)
      ans = fq.f1.oper(fq.f2,oper)
      ans.save()
      oper = Oper.objects.get(pk=1)      
      fq.oper = oper
      fq.answer = ans
      fq.save()
      
      fbq = FractionBankQuestion()
      fbq.fraction_question_bank = fqb
      fbq.question = fq
      fbq.save()
      
      fbq = FractionBankQuestion.objects.all()[0]
      self.assertEquals(fbq.question.answer,ans)
      
class TestFractionQuestionBank(TestCase):
    def test_creation(self):
      fb = FractionBank()
      fb.name = "Bank 1"
      fb.date_created = datetime.date(2012,03,07)
      fb.save()
      fqb = FractionQuestionBank()
      fqb.name = "Addition 100"
      fqb.fraction_bank = fb
      fqb.date_created = datetime.date(2012,03,07)
      fqb.save()
      fqb = FractionQuestionBank.objects.all()[0]
      self.assertEquals(fqb.fraction_bank.name,'Bank 1')
      
    def test_add_identical_items(self):
      fb = FractionBank()
      fb.name = "Bank 0 to 4"
      fb.date_created = datetime.date(2012,03,07)
      fb.save()
      st = 0
      en = 4
      i = fb.fill(st,en)
      fbfs = FractionBankFraction.objects.all()
      
      fqb = FractionQuestionBank()
      fqb.name = "Addition 2"
      fqb.fraction_bank = fb
      fqb.date_created = datetime.date(2012,03,07)
      fqb.save()
      
      fq = FractionQuestion()
      fq.f1 = fbfs[0].fraction
      fq.f2 = fbfs[1].fraction
      oper = Oper.objects.get(pk=1)
      ans = fq.f1.oper(fq.f2,oper)
      ans.save()
      oper = Oper.objects.get(pk=1)     
      fq.oper = oper
      fq.answer = ans
      fq.save()
      
      #Add question once           
      fqb.add_question(fq)
      #Try and add same again
      fqb.add_question(fq)
      #Should fail gracefully and only one question in bank
      fbq = FractionBankQuestion.objects.all()
      self.assertEquals(len(fbq),1)
     
    def test_add_random_questions(self):
      fb = FractionBank()
      fb.name = "Bank 0 to 9"
      fb.date_created = datetime.date(2012,03,07)
      fb.save()
      st = 0
      en = 9
      i = fb.fill(st,en)    
      fqb = FractionQuestionBank()
      fqb.name = "Addition"
      fqb.fraction_bank = fb
      fqb.date_created = datetime.date(2012,03,07)
      fqb.save()
      oper = Oper.objects.get(pk=1)      
      n = 5
      fqb.add_n_questions(n,oper)
      fbq = FractionBankQuestion.objects.all()
      self.assertEquals(len(fbq),n)
      
    def test_generate(self):
      fqb = FractionQuestionBank()
      oper = Oper.objects.get(pk=1)
      n = 20
      st = 0
      en = 10
      name = "Test Bank"
      negatives_allowed = True
      fqb.generate(name,st,en,negatives_allowed,oper,n)
      fbq = FractionBankQuestion.objects.all()      
      self.assertEquals(len(fbq),n)  
                 
      #def test_fill(self): 
      #  oper1 = Oper(oper_name="+")      
      #  oper1.save()
      #  oper = Oper(oper_name="-")
      #  oper.save()
      #  oper = Oper(oper_name="/")
      #  oper.save()
      #  oper = Oper(oper_name="*")
      #  oper.save()
      #  fb = FractionBank()
      #  fb.name = "Bank 1"
      #  fb.date_created = datetime.date(2012,03,07)
      #  fb.save()
      #  st = 0
      #  en = 10
      #  fb.fill(st,en)
      #  fqb = FractionQuestionBank()
      #  fqb.name = "Addition 100"
      #  fqb.fraction_bank = fb
      #  fqb.date_created = datetime.date(2012,03,07)
      #  fqb.save()
      #  tfqbs = FractionQuestionBank.objects.all()[0]
      #  self.assertEquals(tfqbs.fraction_bank.name,"Bank 1")
      #  opers = [oper1]
      #  fqb.fill(opers)
class TestFractionForm(TestCase):
    def test_create_and_save(self):
      data = {'const': 1, 'num': 2, 'denom': 3}
      f = FractionWithConstantForm(data)
      self.assertEquals(f.is_valid(),True)           