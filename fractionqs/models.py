from django.db import models
from fractions import Fraction
import random, datetime

class FractionWithConstant(models.Model):
    const = models.IntegerField()
    num = models.IntegerField()
    denom = models.IntegerField()
    
    def __init__(self, *args, **kwargs):
        self.const = kwargs.get('const')
        self.num = kwargs.get('num')
        self.denom = kwargs.get('denom')
        super(FractionWithConstant, self).__init__(*args, **kwargs)    

    def __eq__(self, other):
        if self.denom != 0 and other.denom !=0:
          f1 = Fraction(self.num,self.denom) + self.const
          f2 = Fraction(other.num,other.denom) + other.const
          ret = f1 == f2 
        else:
          ret = "ZeroDivisionError"
        return ret
          
    def __ne__(self, other):
        return not self.__eq__(other)

    def __unicode__(self):
        if self.num == 0 and self.denom == 0 and self.const == 0:
          return u'No response'
        elif self.num == 0 and self.const != 0:
          return u'%s' % (self.const)         
        else:
          if self.const != 0:    
            return u'%s <sup>%s</sup>&frasl;<sub>%s</sub>' % (self.const, self.num, self.denom)
          else:
            return u'<sup>%s</sup>&frasl;<sub>%s</sub>' % (self.num, self.denom)

    def simplest_form(self):
        #take sign from constant
        if self.const < 0:
          f1 = self.const - Fraction(self.num,self.denom)
        else:
          f1 = self.const + Fraction(self.num,self.denom)
        #Find remainder          
        cnst =  abs(f1.numerator) / abs(f1.denominator)  
        if f1.numerator < 0 and cnst > 0:
        #transfer sign to constant
          cnst = - cnst
          f1 = abs(f1)
          f1 += cnst
        if f1.numerator > 0 and cnst > 0:  
          f1 -= cnst  
        self.const = cnst
        self.num = f1.numerator
        self.denom = f1.denominator
        return(self)
    
    def oper(self,other,oper):
        f1 = Fraction(self.num,self.denom) + abs(self.const)
        f2 = Fraction(other.num,other.denom) + abs(other.const)
        #take sign from constant
        if self.const < 0:
          f1 = -f1
        if other.const < 0:
          f2 = -f2
        if oper.oper_name == "+":          
          ans = f1 + f2
        elif oper.oper_name == "-":  
          ans = f1 - f2
        elif oper.oper_name == "/":  
          ans = f1 / f2
        elif oper.oper_name == "*":  
          ans = f1 * f2
        else:
          print "Unknown operation"
          return(None)          
        ansq = FractionWithConstant()
        ansq.const = 0
        ansq.num = ans.numerator
        ansq.denom = ans.denominator
        ansq = ansq.simplest_form()
        return(ansq)
        
class Oper(models.Model):
    oper_name = models.CharField(max_length=1)
    def __unicode__(self):
        return self.oper_name        
          
class FractionQuestion(models.Model):
    f1 = models.ForeignKey(FractionWithConstant,related_name='f1')
    f2 = models.ForeignKey(FractionWithConstant,related_name='f2')
    oper = models.ForeignKey(Oper)
    answer = models.ForeignKey(FractionWithConstant,related_name='answer')

    def __eq__(self, other):
      return self.f1 == other.f1 and self.f2 == other.f2 and self.oper == other.oper    

    def __ne__(self, other):
      return not self.__eq__(other)
    
    
class FractionBank(models.Model):
    name = models.CharField(max_length=30)
    date_created = models.DateField()
    
    def generate_question(self,oper):
      fbfs = FractionBankFraction.objects.filter(fraction_bank=self)
      #Choose two random fractions
      fs = random.sample(fbfs, 2) 
      #Return question
      fq = FractionQuestion()
      ans = fs[0].fraction.oper(fs[1].fraction,oper)
      #See if answer in database
      fwcs = FractionWithConstant.objects.all()
      mtch = False
      for f in fwcs:
        if ans == f:
          mtch = True
          ans = f
          break        
      if mtch == False:
        ans.save()
      fq.f1 = fs[0].fraction
      fq.f2 = fs[1].fraction
      fq.oper = oper
      fq.answer = ans   
      return(fq)
    
    def fill(self,st,en,negatives_allowed=False):
        items = 0
        for i in range(st,en):
          for j in range(st+1,en):    
            for k in range(j+1,en):      
              f = FractionWithConstant(const=i,num=j,denom=k)
              g = FractionWithConstant(const=i,num=j,denom=k)
              f.simplest_form()
              if f == g:
                f.save()
                fbf = FractionBankFraction()
                fbf.fraction_bank = self
                fbf.fraction = f
                fbf.save()
                items += 1
                if negatives_allowed:
                  neg = FractionWithConstant(const=i,num=j,denom=k) 
                  if i == 0:
                    neg.num = -j
                  else:
                    neg.const = -i
                  neg.save()                
                  fbf = FractionBankFraction()
                  fbf.fraction_bank = self
                  fbf.fraction = neg
                  fbf.save()
                  items += 1
        return(items)  
    
class FractionBankFraction(models.Model):
    fraction_bank = models.ForeignKey(FractionBank)
    fraction = models.ForeignKey(FractionWithConstant)
    
class FractionQuestionBank(models.Model):
    name = models.CharField(max_length=30)
    fraction_bank = models.ForeignKey(FractionBank)
    date_created = models.DateField()
    
    def add_question(self,q):
      #Check to see if exists
      fbqs = FractionBankQuestion.objects.filter(fraction_question_bank=self)
      mtch = False
      for fbq in fbqs:
        if fbq.question == q:
          mtch = True
          break
      if mtch == False:
        #Save question and answer
        q.save()
        fbq = FractionBankQuestion()
        fbq.fraction_question_bank = self
        fbq.question = q
        fbq.save()
        return(True)
      else:
        return(False)      
    
    def add_n_questions(self,n,oper):
      items = 0
      tries = 0
      while items < n:
        print "items:" + str(items)      
        print "tries:" + str(tries)
        tries += 1
        #Create random question from fraction bank
        q = self.fraction_bank.generate_question(oper)
        #Try to add to bank
        added = self.add_question(q)
        #Check if added
        if added:
          items +=1
      return(items)      
    
    def generate(self,name,st,en,negatives_allowed,oper,n):
      fb = FractionBank()
      fb.name = name + str(st) + " to " + str(en)
      fb.date_created = datetime.date.today()
      fb.save()
      i = fb.fill(st,en,negatives_allowed)    
      self.name = name
      self.fraction_bank = fb
      self.date_created = datetime.date.today()
      self.save()
      self.add_n_questions(n,oper)
      return(self)
      
    def fill(self,opers):
      items = 0
      fs1 = FractionBankFraction.objects.filter(fraction_bank=self.fraction_bank)
      fs2 = FractionBankFraction.objects.filter(fraction_bank=self.fraction_bank)
      for o in opers:
        for jj in fs1:
          j = jj.fraction
          for kk in fs2:
            k = kk.fraction
            if j != k:
              ans = j.oper(k,o.oper_name)
              exf = FractionWithConstant.objects.filter(const=ans.const,num=ans.num,denom=ans.denom)  
              if len(exf)>0:
                ans = exf[0]
              else:
                ans.save()
              
              fq = FractionQuestion()
              fq.f1 = j
              fq.f2 = k
              fq.oper = o
              fq.answer = ans
              fq.save()
      
              fbq = FractionBankQuestion()
              fbq.fraction_bank = self.fraction_bank
              fbq.question = fq
              fbq.save()          
              items +=1
              print str(items)      
      return(items)
    
class FractionBankQuestion(models.Model):
    fraction_question_bank = models.ForeignKey(FractionQuestionBank)
    question = models.ForeignKey(FractionQuestion)     
