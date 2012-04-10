#!/usr/bin/env python

from pyper import *
from numpy import array

def updateAbility(responses,grades,m_theta,s_theta):
  myR = R()
  myR['responses'] = array(responses)
  myR['grades'] = array(grades)
  myR['m.theta'] = m_theta
  myR['s.theta'] = s_theta
  myR.run('source("rasch.R")')
  mean_theta = myR['thm']
  sd_theta = myR['ths']
  grade_probs = myR['probs']
  print mean_theta
  print sd_theta
  print grade_probs 
  del myR  