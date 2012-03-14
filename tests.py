from django.test import TestCase
from maths.fractionqs.models import FractionQ

def createFraction(oper):
      fs = (1,0,1),(1,0,1)
      ans = (2,0,1),(1,0,1),(0,0,1),(1,0,1)
      q1 = FractionQ()
      q1.const = fs(0)(0)
      q1.num = fs(0)(1)
      q1.denom = fs(0)(2)
      q2 = FractionQ()
      q2.const = fs(1)(0)
      q2.num = fs(1)(1)
      q2.denom = fs(1)(2)
      ans = FractionQ()
      ans.const = ans(oper,0)
      ans.num = ans(oper,1)
      ans.denom = ans(oper,2)
      return[q1,q2,ans]

class TestCreateFraction(TestCase):
    def test_basic_creation(self):
      fq = FractionQ()
      fq.const = 1
      fq.num = 2
      fq.denom = 3
      fq.save()
      fqs = FractionQ.objects.all()
      fq = fqs[0]
      self.assertEquals(fq.const,1)      
      self.assertEquals(fq.num,2)      
      self.assertEquals(fq.denom,3)

    def test_two_fractions_equal(self):
      fq1 = FractionQ()
      fq1.const = 1
      fq1.num = 4
      fq1.denom = 2
      fq1.save()
      fq2 = FractionQ()
      fq2.const = 2
      fq2.num = 1
      fq2.denom = 1
      fq2.save()
      tst = fq1 == fq2
      self.assertEquals(tst,True)
      
    def test_two_fractions_not_equal(self):
      fq1 = FractionQ()
      fq1.const = 1
      fq1.num = 4
      fq1.denom = 2
      fq1.save()
      fq2 = FractionQ()
      fq2.const = 2
      fq2.num = 1
      fq2.denom = 2
      fq2.save()
      tst = fq1 == fq2
      self.assertEquals(tst,False)   
      
    def test_zero_division_error(self):
      fq1 = FractionQ()
      fq1.const = 1
      fq1.num = 4
      fq1.denom = 2
      fq1.save()
      fq2 = FractionQ()
      fq2.const = 2
      fq2.num = 0
      fq2.denom = 0
      fq2.save()
      tst = fq1 == fq2
      self.assertEquals(tst,'ZeroDivisionError')  
      
    def test_simplest_form(self):
      fq1 = FractionQ()
      fq1.const = -2
      fq1.num = 3
      fq1.denom = 2
      fq1.save()
      fq2 = fq1.simplest_form()
      self.assertEquals(fq2.const, -3)
      self.assertEquals(fq2.num, 1)      
      self.assertEquals(fq2.denom, 2)

    def test_addition(self):
      fs = createFraction(0)
      fq1 = fs(0)
      fq2 = fs(1)
      my_ans = fs(2)
      ans = fq1.add(fq2)
      self.assertEquals(ans.const, my_ans.const)
      self.assertEquals(ans.num, my_ans.const)
      self.assertEquals(ans.denom, my_ans.const)

    def test_multiplication(self):
      fq1 = FractionQ()
      fq1.const = 0
      fq1.num = -1
      fq1.denom = 2
      fq1.save()
      fq2 = FractionQ()
      fq2.const = 0
      fq2.num = 1
      fq2.denom = 4
      fq2.save()
      ans = fq1.multiply(fq2)
      self.assertEquals(ans.const, 0)
      self.assertEquals(ans.num, -1)
      self.assertEquals(ans.denom, 8)      