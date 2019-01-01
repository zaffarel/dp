# Fading Suns
# Fusion Interlock Custom System v7
# This file contains the core business function of the app
import math
from random import randint
import os
from collector.models.skillrefs import SkillRef
from collector.utils.fics_references import *
from collector.utils.basic import debug_print

def check_secondary_attributes(ch):
  """ Compute all secondary attributes (we check nothing in fact)
  """
  ch.SA_REC = ch.PA_STR + ch.PA_CON
  ch.SA_STA = math.ceil(ch.PA_BOD / 2) - 1
  ch.SA_END = (ch.PA_BOD + ch.PA_STR) * 5
  ch.SA_STU = ch.PA_CON + ch.PA_BOD
  ch.SA_RES = ch.PA_WIL + ch.PA_PRE
  ch.SA_DMG = math.ceil(ch.PA_STR / 2) - 2
  ch.SA_TOL = ch.PA_TEM + ch.PA_WIL
  ch.SA_HUM = (ch.PA_TEM + ch.PA_WIL) * 5
  ch.SA_PAS = ch.PA_TEM + ch.PA_AWA
  ch.SA_WYR = ch.PA_INT + ch.PA_REF
  ch.SA_SPD = math.ceil(ch.PA_REF / 2)
  ch.SA_RUN = ch.PA_MOV *2


def check_everyman_skills(ch):
  """ Check and fix everyman values for the skills"""
  from collector.models.skills import Skill
  skills = ch.skill_set.all()
  for every in EVERYMAN[ch.species]:
    every_found = False
    for s in skills:
      if s.skill_ref.reference == every:
        every_found = True
        val = int(EVERYMAN[ch.species][every])
        if s.value < val:          
          debug_print('Value fixed for %s (%s)'%(s.skill_ref.reference,val))
          this_skill = Skill.objects.get(id=s.id)
          this_skill.value = val
          this_skill.save()
        break
    if not every_found:
      debug_print('Not found: %s... Added!'%every)
      val = int(EVERYMAN[ch.species][every])
      this_skill_ref = SkillRef.objects.get(reference=every)
      this_skill = Skill()
      this_skill.character=ch
      this_skill.skill_ref=this_skill_ref
      this_skill.value = val
      this_skill.save()


def check_gm_shortcuts(ch,sk):
  """ Check for Gamemaster shortcuts for the character """
  if sk.skill_ref.reference in SHORTCUTS:
    score = sk.value + getattr(ch,SHORTCUTS[sk.skill_ref.reference]['attribute'])
    newshortcut = '%s: <b>%d</b>'%(SHORTCUTS[sk.skill_ref.reference]['label'],score)
    return newshortcut  
  else:
    return ''


def check_nameless_attributes(ch):
  res = ''
  PA_PHY = (ch.PA_STR + ch.PA_CON + ch.PA_BOD + ch.PA_MOV) // 4
  PA_SPI = (ch.PA_INT + ch.PA_WIL + ch.PA_TEM + ch.PA_PRE) // 4
  PA_COM = (ch.PA_TEC + ch.PA_REF + ch.PA_AGI + ch.PA_AWA) // 4
  res = '<h2>Nameless</h2>Physical:<b>%s</b> Spirit:<b>%s</b> Combat:<b>%s</b>' % (PA_PHY,PA_SPI,PA_COM)
  return res

def check_attacks(ch):
  """ Attacks shortcuts depending on the avatar and his/her weapons and skills """
  ranged_attack = '<h2>Attacks</h2>'
  for w in ch.weapon_set.all():
    if w.weapon_ref.category in {'P','RIF','SMG'}:      
      sk = ch.skill_set.filter(skill_ref__reference='Shoot').first()
      if sk is None:
        sval = 0
      else:
        sval = sk.value
      score = ch.PA_REF + sval + w.weapon_ref.weapon_accuracy
      dmg = w.weapon_ref.damage_class
      x = minmax_from_dc(dmg)
      ranged_attack += '%s: Roll:<b>%d+1D12</b> Dmg:<b>%d-%d</b></br>'%(w.weapon_ref.reference,score,x[0],x[1])
    if w.weapon_ref.category in {'HVY'}:      
      sk = ch.skill_set.filter(skill_ref__reference='Heavy Weapons').first()
      if sk is None:
        sval = 0
      else:
        sval = sk.value
      score = ch.PA_REF + sval + w.weapon_ref.weapon_accuracy
      dmg = w.weapon_ref.damage_class
      x = minmax_from_dc(dmg)
      ranged_attack += '%s: Roll:<b>%d+1D12</b> Dmg:<b>%d-%d</b></br>'%(w.weapon_ref.reference,score,x[0],x[1])
    if w.weapon_ref.category in {'MELEE'}:      
      sk = ch.skill_set.filter(skill_ref__reference='Melee').first()
      if sk is None:
        sval = 0
      else:
        sval = sk.value
      score = ch.PA_REF + sval + w.weapon_ref.weapon_accuracy
      dmg = w.weapon_ref.damage_class
      x = minmax_from_dc(dmg) 
      ranged_attack += '%s: Roll:<b>%d+1D12</b> Dmg:<b>%d-%d (+str:%d)</b></br>'%(w.weapon_ref.reference,score,x[0],x[1], ch.SA_DMG)
  tmpstr = filter(None,ranged_attack.split('</br>'))
  ranged_attack = '<br/>'.join(tmpstr) 
  return ranged_attack

def get_rid(s):
  x = s.replace(' ','_').replace("'",'').replace('é','e').replace('è','e').replace('ë','e').replace('â','a').replace('ô','o').replace('"','').replace('ï','i').replace('à','a').replace('-','')
  return x.lower()

def minmax_from_dc(sdc):
  if sdc == '':
    return (0,0)
  s = sdc.lower()
  dmin,dmax,dbonus = 0,0,0
  split_bonus = s.split('+')
  split_scope = split_bonus[0].split('d')
  if split_bonus.count == 2:
    dbonus = int(split_bonus[1])
  dmin = int(split_scope[0])+dbonus
  dmax = dmin*int(split_scope[1])+dbonus
  return (dmin,dmax)

def sanitize(character,f):
  sane_f = {}
  for key, value in f.items():
    rkey,rvalue = character.update_field(key, value)
    if rkey != False:
      sane_f[rkey] = rvalue
  return sane_f


def check_root_skills(ch):
  """ Checking Root skills and their specialties
  """
  exportable = True
  skills = ch.skill_set.all()
  for root in skills:
    if root.skill_ref.is_root:
      cnt = 0
      for spec in skills:
        if spec.skill_ref.is_speciality:
          if spec.skill_ref.linked_to == root.skill_ref:
            cnt += 1
      if cnt >= root.value:
        if cnt > root.value:
          root.value = cnt
          debug_print('Fixing root value for %s...'%root.skill_ref.reference)
        #else:         
          #print('OK for %s'%root.skill_ref.reference)
      else:
        debug_print('Warning: Missing %d specialties for %s\n'% (root.value-cnt,root.skill_ref.reference))
        exportable = False
  return exportable

def roll(maxi):
  """ A more random '1 to maxi' dice roller  """
  randbyte = int.from_bytes(os.urandom(1),byteorder='big',signed=False)
  x = int(randbyte / 256 * (maxi)) +1
  debug_print('x=%d/%d)'%(x,maxi))
  return x

def choose_pa(weights):
  #x = randint(1,sum(weights))
  x = roll(sum(weights))
  cum = 0
  idx = 0
  while idx < 12:
    cum += weights[idx]
    if x <= cum:
      return idx
    idx += 1
  return -1

def check_primary_attributes(ch):
  """ Fixing primary attributes """
  pool = ROLES[ch.role]['primaries']
  maxi = ROLES[ch.role]['maxi']
  weights = PROFILES[ch.profile]['weights']
  ch.challenge = '(<i class="fas fa-th-large"></i>%02d <i class="fas fa-th-list"></i>%02d <i class="fas fa-th"></i>%02d <i class="fas fa-outdent"></i>%02d)'%(ROLES[ch.role]['primaries'],ROLES[ch.role]['skills'], ROLES[ch.role]['talents'],ROLES[ch.role]['bc'])
  debug_print('%s: %s [ %d / %d ]'%(ch.full_name,ch.role,pool,maxi))  
  pas = [2,2,2,2,2,2,2,2,2,2,2,2]
  #pas = [0,0,0,0,0,0,0,0,0,0,0,0]
  current =  ch.PA_STR+ch.PA_CON+ch.PA_BOD+ch.PA_MOV+ch.PA_INT+ch.PA_WIL+ch.PA_TEM+ch.PA_PRE+ch.PA_TEC+ch.PA_REF+ch.PA_AGI+ch.PA_AWA
  debug_print('Current PA TOTAL: %d'%(current))
  if (current < pool or ch.keyword.startswith('rebuild')) and ch.player == '':
    pool = pool-24
    debug_print('Error: Primary Attributes invalid. Fixing that\n')
    while pool>0:      
      chosen_pa = choose_pa(weights)
      idx = chosen_pa
      if pas[idx] < maxi:
        pas[idx] += 1
        pool -= 1
      else:
        debug_print('Invalid : already too high: pa[idx]:%d idx:%d maxi:%d pool:%d chosen_pa:%d'%(pas[idx],idx,maxi,pool,chosen_pa))
    debug_print(pas)
    ch.PA_STR = pas[0]
    ch.PA_CON = pas[1]
    ch.PA_BOD = pas[2]
    ch.PA_MOV = pas[3]
    
    ch.PA_INT = pas[4]
    ch.PA_WIL = pas[5]
    ch.PA_TEM = pas[6]
    ch.PA_PRE = pas[7]
    
    ch.PA_TEC = pas[8]
    ch.PA_REF = pas[9]
    ch.PA_AGI = pas[10]
    ch.PA_AWA = pas[11]
    if ch.keyword == 'rebuild' or ch.keyword == 'rebuild_pa':
      ch.keyword = 'rebuilt'

def get_skills_list(ch,groups):
  """ Prepare the list of skills without specialties """
  skills = SkillRef.objects.all().filter(is_speciality=False)
  master_skills = []
  for s in skills:
    weight = 1
    for g in groups:
      if s.group == g:
        weight = 5
    master_skills.append({'skill':s.reference, 'data':s, 'weight':weight})
  msl = []
  for ms in master_skills:
    debug_print('%s: %d'%(ms['skill'],ms['weight']))
  return master_skills

def choose_sk(alist,maxweight):
  x = roll(maxweight)
  cum = 0
  idx = 0
  while idx < len(alist):
    cum += alist[idx]['weight']
    if x <= cum:
      return alist[idx]['data']
    idx += 1
  return None

def check_skills(ch):
  """ Fixing skills """
  pool = ROLES[ch.role]['skills']
  maxi = ROLES[ch.role]['maxi']
  groups = PROFILES[ch.profile]['groups']
  current = ch.SK_TOTAL
  print('Current SK TOTAL: %d (pool is %d)'%(current,pool))
  master_list = get_skills_list(ch,groups)
  debug_print(master_list)
  master_weight = 0
  for s in master_list:
    master_weight += s['weight']
  debug_print(master_weight)
  print('Keyword : %s'%(ch.keyword))
  if ch.keyword == 'rebuild_skills':
    for s in ch.skill_set.all():
      s.delete()
    check_everyman_skills(ch)
    pool -= 16
    ch.SK_TOTAL = 16
    print('>>> ch.sk_total: %d'%(ch.SK_TOTAL))
  if (current < pool or ch.keyword.startswith('rebuild')) and ch.player == '':
    pool -= ch.SK_TOTAL
    print('Error: Skills total too weak. Fixing that\n')    
    while pool>0:
      chosen_sk = choose_sk(master_list,master_weight)
      debug_print('%d: %s'%(pool,chosen_sk.reference))
      ch.add_or_update_skill(chosen_sk)
      pool -= 1
  #ch.add_missing_root_skills()
  if ch.keyword.startswith('rebuild'):
    ch.keyword = 'rebuilt'
    
  

def check_role(ch):
  pa_pool = ROLES[ch.role]['primaries']
  sk_pool = ROLES[ch.role]['skills']
  ta_pool = ROLES[ch.role]['talents']
  bc_pool = ROLES[ch.role]['bc']
  ba_pool = ROLES[ch.role]['ba']
  status = True
  if ch.PA_TOTAL < pa_pool:
    print('Not enough PA: %d < %d'%(ch.PA_TOTAL,pa_pool))
    status = False 
  elif ch.SK_TOTAL < sk_pool:
    print('Not enough SK: %d < %d'%(ch.SK_TOTAL,sk_pool))
    status = False 
  elif ch.BA_TOTAL < ba_pool:
    print('Not enough BA: %d < %d'%(ch.BA_TOTAL,ba_pool))
    status = False 
  elif ch.BC_TOTAL < bc_pool:
    print('Not enough BC: %d < %d'%(ch.BC_TOTAL,bc_pool))
    status = False 
  elif ch.TA_TOTAL < ta_pool:
    print('Not enough TA: %d < %d'%(ch.TA_TOTAL,ta_pool))
    status = False 
  return status

def update_challenge(ch):
  res = ''
  res += '<i class="fas fa-th-large" title="primary attributes"></i>%d '%(ch.AP)
  res += '<i class="fas fa-th-list" title="skills"></i> %d '%(ch.SK_TOTAL)
  res += '<i class="fas fa-th" title="talents"></i> %d '%(ch.TA_TOTAL)
  res += '<i class="fas fa-outdent" title="blessing curses"></i> %d '%(ch.BC_TOTAL)
  res += '<i class="fas fa-outdent" title="benefice afflictions"></i> %d '%(ch.BA_TOTAL)
  res += '<i class="fas fa-newspaper" title="OP challenge"></i> %d '%(ch.OP)
  return res

def get_keywords():
  from collector.models.characters import Character
  everybody = Character.objects.all()
  keywords = []
  for someone in everybody:
    if someone.keyword != '':
      keywords.append(someone.keyword)
  return sorted(list(set(keywords)))
