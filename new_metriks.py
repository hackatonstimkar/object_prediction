# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 13:28:32 2019

@author: pitonhik
"""
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 16:20:29 2019

@author: pitonhik
"""
import os
import pandas as pd
import math
import statistics as st
r ={}
mark_mas=[]
svodka = {}
w1 = 1
w2 = 1
w3 =1
w4 =1
w5 =1
w6 =1
w7 =1
def per(xm1,ym1,xmax1,ymax1,xm2,ym2,xmax2,ymax2):
    left = max(xm1,xm2)
    top = min(ymax1,ymax2)
    right= min(xmax1,xmax2)
    bot = max(ym1,ym2)
    wight = right - left
    h = top - bot
    #print(wight<0)
    #print(h<0)
    if wight < 0 or h < 0 :
        #print(wight < 0 or h < 0)
        return 'false'
    return wight * h
def mark(xm1,ym1,xmax1,ymax1,xm2,ym2,xmax2,ymax2):
    p = per(xm1,ym1,xmax1,ymax1,xm2,ym2,xmax2,ymax2)
    if p == 'false':
        return 0
    elif p == 5:
        return 1
    s2 = (max(xmax2,xm2) - min(xmax2,xm2))*(max(ymax2,ym2) - min(ymax2,ym2))
    s1 = (max(xmax1,xm1) - min(xmax1,xm1))*(max(ymax1,ym1) - min(ymax1,ym1))
    s = s1+s2 - p
    if s ==0:
        return 1
    mark = p / s
    return mark
tr_data =pd.read_csv('train_data.csv',sep=',')
tr_ans = pd.read_csv('train_answers.csv',sep=',')
id_ob = [] #объект уникальных id обьектов 
for i in range(len(tr_data)):
    if not (tr_data['itemId'][i] in id_ob):
        id_ob.append(tr_data['itemId'][i])
id_p =[] #объект уникальных id людей из тестовых выборок
for j in range(len(tr_data)):
    if not (tr_data['userId'][j] in id_p):
        id_p.append(tr_data['userId'][j])
ts = pd.read_csv('test_data.csv',sep=',')
#loc[] обращение по индексу
dp ={}
cl_p =[]
def sred_rast(mas):
    #med = st.median(mas)
    mas.sort()
    rast = []
    sr = 0
    if len(mas)==1:
        return 0
    for i in range(len(mas)-1):
        
        rast.append(mas[i+1]-mas[i])
        
    
    sr =  sred(rast)
    #print(sr)
    med = st.median(mas)
    #print(med)
    return 1 - (sr / med)
def dlina(mas):
    d =  len(mas)
    d = 1 / d
    return 1 - d
def sred(a):
    s =0 
    for i in range(len(a)):
        s = s+ a[i]
    res = s/ len(a)
    return(res)
def newrad(mas):
    nm =[]
    res = []
    mas.sort()
    if len(mas)==1:
        res.append(mas)
        return res
    for i in range(len(mas)-1):
        nm.append(mas[i+1]-mas[i])
    
    m = sred(nm)
    q=0
    for i in range(len(nm)):
        if nm[i]> m :
            
            newm = []
            newm = mas[q:i+1]
            q = i+1
            res.append(newm)
            del(newm)
    res.append(mas[q:len(mas)])
    return res
def naib_v(mas):
    m = newrad(mas)
    r = 0
    l = 0
    le = []
    s = 0
    for i in range(len(m)): 
       le.append(len(m[i]))
    ma = max(le)
    if len(mas)==1:
        return mas[0]
    elif le.count(ma)==1:
        return sred(m[le.index(ma)])
    else:
        kol = le.count(ma)
        for i in range(kol):
            s = s + sred(m[le.index(ma)])
            m.remove(m[le.index(ma)])
            le.remove(ma)
        return s / kol
def srez(df,name):
    cl = []
    for i in range(len(df)):
     idf = df.index[i]
     
     cl.append(df[name].loc[idf])
    return cl
def my_print(ids):
  print('/-/-/-/-/-/-/-/-/')
  data = tr_data[tr_data['itemId']==ids]
  print(data)
  print('--------')
  data = tr_ans[tr_ans['itemId']==ids]
  print(data)
        
def new_pipl_filt():
 #print('/--/')
 c =[]
 for i in range(len(id_p)):
    
    pipl = id_p[i]
    pa = tr_data[tr_data['userId']==pipl]
    m = []
    for j in range(len(pa)):
      ind = pa.index[j]
      xm1 = pa['Xmin'].loc[ind]
      ym1 = pa['Ymin'].loc[ind]
      xmax1 = pa['Xmax'].loc[ind]
      ymax1 = pa['Ymax'].loc[ind]
      otv = tr_ans[tr_ans['itemId']==pa['itemId'].loc[ind]]
      #print(otv)
      ind2 = otv['Xmin_true'].index[0]
      xm2=otv['Xmin_true'].loc[ind2]
      ym2=otv['Ymin_true'].loc[ind2]
      xmax2=otv['Xmax_true'].loc[ind2]
      ymax2=otv['Ymax_true'].loc[ind2]
      mar = mark(xm1,ym1,xmax1,ymax1,xm2,ym2,xmax2,ymax2)
      m.append(mar)
    rez = {}
    rez['id']=pipl
    rez['mas']=m
    rez['sred']=sred(m)
    rez['med']=st.median(m)
    rez['min']= min(m)
    rez['max']= max(m)
    c.append(rez)
    del(rez)
    
 return c
def pipl_metrik():
    global pip
    global w1
    global w2
    global w3
    global w4
    w1= 0
    for i in range(len(pip)):
        dlin = dlina(pip[i]['mas'])
        mi = pip[i]['min']
        #print(pip[i]['mas'])
        ver = naib_v(pip[i]['mas'])
        med = pip[i]['med']
        metrika = w1*dlin + 1*mi + 2*ver + 1 * med
        pip[i]['metr']=metrika / 3
pip = new_pipl_filt()
pipl_metrik()
def new_sr_sr():
 if True:
  global svodka
  global mark_mas
  global r
  global id_ob
  global tr_ans
  global id_p
  global pip
  for i in range(len(id_ob)):
   ot = [0,0,0,0]
   ob = id_ob[i]
   t = tr_data[tr_data['itemId']==ob]
   work = []
   work.append(srez(t,'userId'))
   work.append([ob])
   work.append(srez(t,'Xmin'))
   work.append(srez(t,'Ymin'))
   work.append(srez(t,'Xmax'))
   work.append(srez(t,'Ymax'))
   work_test = []
   work_test.append(srez(t,'Xmin'))
   work_test.append(srez(t,'Ymin'))
   work_test.append(srez(t,'Xmax'))
   work_test.append(srez(t,'Ymax'))
   w8=1
   obl_x = newrad(work[2])
   obl_y = newrad(work[3])
   obl_xm = newrad(work[4])
   obl_ym = newrad(work[5])
   mas_o_x = obl(obl_x,work[2],work[0])
   mas_o_y = obl(obl_y,work[3],work[0])
   mas_o_xm = obl(obl_xm,work[4],work[0])
   mas_o_ym = obl(obl_ym,work[5],work[0])
   
   #for j in range(len(best_x)):
       
   onvet1 = []
   onvet1.append(oblast(mas_o_x,obl_x))
   onvet1.append(oblast(mas_o_y,obl_y))
   onvet1.append(oblast(mas_o_xm,obl_xm))
   onvet1.append(oblast(mas_o_ym,obl_ym))
   onvet2=[]
   onvet2.append(st.median(work_test[0]))
   onvet2.append(st.median(work_test[1]))
   onvet2.append(st.median(work_test[2]))
   onvet2.append(st.median(work_test[3]))
   masp =[]
   for j in range(len(work[0])):
       if work[0][j] in id_p:
         masp.append(ret_pm(work[0][j]))
   if len(masp)==0:
       for i in range(len(work[0])):
           p ={}
           p['id']=work[0][i]
           p['metr']=0
           pip.append(p)
           del(p)
   elif len(masp)>0:
        for i in range(len(work[0])):
            if not(work[0][i] in id_ob):
                p ={}
                p['id']=work[0][i]
                p['metr']=sred(masp)
                pip.append(p)
                del(p)
   bp = max(masp)
   #print(masp)
   pind = masp.index(bp)
   bpx = work_test[0][pind]
   #print(bpx)
   bpy = work_test[1][pind]
   #print(bpy)
   bpxm = work_test[2][pind]
   bpym = work_test[3][pind]
   onvet3 =[]
   onvet3.append(bpx)
   onvet3.append(bpy)
   onvet3.append(bpxm)
   onvet3.append(bpym)
   mark12 = mark(onvet1[0],onvet1[1],onvet1[2],onvet1[3],onvet2[0],onvet2[1],onvet2[2],onvet2[3])
   mark23= mark(onvet2[0],onvet2[1],onvet2[2],onvet2[3],onvet3[0],onvet3[1],onvet3[2],onvet3[3])
   mark31= mark(onvet3[0],onvet3[1],onvet3[2],onvet3[3],onvet1[0],onvet1[1],onvet1[2],onvet1[3])
   mai = max([mark12,mark23,mark31])
   if mark12 == mai:
       ot[0] = int((onvet1[0] + onvet2[0]) / 2)
       ot[1] = int((onvet1[1] + onvet2[1]) / 2)
       ot[2] = int((onvet1[2] + onvet2[2]) / 2)
       ot[3] = int((onvet1[3] + onvet2[3]) / 2)
   elif mark23 == mai:
       ot[0] = int((onvet3[0] + onvet2[0]) / 2)
       ot[1] = int((onvet3[1] + onvet2[1]) / 2)
       ot[2] = int((onvet3[2] + onvet2[2]) / 2)
       ot[3] = int((onvet3[3] + onvet2[3]) / 2)
   else :
       ot[0] = int((onvet3[0] + onvet1[0]) / 2)
       ot[1] = int((onvet3[1] + onvet1[1]) / 2)
       ot[2] = int((onvet3[2] + onvet1[2]) / 2)
       ot[3] = int((onvet3[3] + onvet1[3]) / 2)
   #print(mark1)
   '''if mark1 > 0.68:
    ot[0]= xe
    ot[1]= ye
    ot[2]= xme
    ot[3]= yme
   
       
   else:
    ot[0]= bpx + xe
    ot[0] = int(ot[0]/2)
    ot[1]= bpy + ye
    ot[1] = int(ot[1]/2)
    ot[2]= bpxm + xme
    ot[2] = int(ot[2]/2)
    ot[3]= bpym + yme
    ot[3] = int(ot[3]/2)
   if len(work[0])< 4:
       ot[0]= xe
       ot[1]= ye
       ot[2]= xme
       ot[3]= yme'''
   ans = tr_ans[tr_ans['itemId']==ob]
   
   io = ans.index[0]
   
   x = ans['Xmin_true'].loc[io]
   
   y = ans['Ymin_true'].loc[io]
   xm = ans['Xmax_true'].loc[io]
   ym = ans['Ymax_true'].loc[io]
   mg = mark(ot[0],ot[1],ot[2],ot[3],x,y,xm,ym)
   
   """if mg < 0.5:
      r[str(ob)]=mg"""
   mark_mas.append(mg)
   svodka[str(ob)]= {}
   svodka[str(ob)]['piple']=[work[0]]
   svodka[str(ob)]['xmin']=work_test[0]
   svodka[str(ob)]['ymin']=work_test[1]
   svodka[str(ob)]['xmax']=work_test[2]
   svodka[str(ob)]['ymax']=work_test[3]
   svodka[str(ob)]['X_grup']= obl_x
   svodka[str(ob)]['Y_grup']= obl_y
   svodka[str(ob)]['Xm_grup']= obl_xm
   svodka[str(ob)]['Ym_grup']= obl_ym
   svodka[str(ob)]['xmin_v']=ot[0]
   svodka[str(ob)]['ymin_v']=ot[1]
   svodka[str(ob)]['xmax_v']=ot[2]
   svodka[str(ob)]['ymax_v']=ot[3]
   svodka[str(ob)]['ver']=mg
   svodka[str(ob)]['xmin_v_TRUE']=x
   svodka[str(ob)]['ymin_v_TRUE']=y
   svodka[str(ob)]['xmax_v_TRUE']=xm
   svodka[str(ob)]['ymax_v_TRUE']=ym
   pi_m =[]
   for j in range(len(work[0])):
       pi_m.append(ret_pm_inf(work[0][j]))
   #svodka[str(ob)]['piple_ym']=pi_m
   del(pi_m)
   if mg < 0.4 and mg > 0.3:
    r[str(ob)] = mg
   
   del(work)
   del(work_test)
def oblast(mas_o_x,obl_x):
    best_x = newrad_2(mas_o_x)
    sre = 0
    sre_i = 0
    for j in range(len(best_x)):
       if sred(best_x[j]) > sre:
           sre = sred(best_x[j])
           sre_i = j
    if len(best_x) == 1:
        mac = max(best_x[0])
        mas_in = mas_o_x.index(mac)
        obx = obl_x[mas_in]
        return sred(obx)
    if len(best_x[sre_i])==1:
     mas_in = mas_o_x.index(best_x[sre_i])
     obx = obl_x[mas_in]
    else:
       
       obx = []
       for j in range(len(best_x[sre_i])):
             mas_in = mas_o_x.index(best_x[sre_i][j])
             for g in range(len(obl_x[mas_in])):
                 
                 obx.append(obl_x[mas_in][g])
       #print('---')     
    return sred(obx)
    
def obl(mas_obl,mas,mas_p):
    global pip
    global w5
    global w6
    global w7
    
    rez =[]
    j = 0
    for i in range(len(mas_obl)):
        dlin = dlina(mas_obl[i])
        #print(mas_obl[i])
        sr_r = sred_rast(mas_obl[i])
        sum_p = 0
        
        for j in range(len(mas_obl[i])):
            ind = mas.index(mas_obl[i][j])
            piple = mas_p[ind]
            #print(piple)
            sum_p = sum_p + ret_pm(piple)
        sum_p = sum_p / len(mas_obl[i])
        metrika = 1*dlin + 2*sr_r + 0.5*sum_p
        rez.append(metrika)
    return rez
            
        
def ret_pm(a):
   global pip
   for i in range(len(pip)):
       if pip[i]['id']==a:
           return pip[i]['metr']
def ret_pm_inf(a):
   global pip
   for i in range(len(pip)):
       if pip[i]['id']==a:
           return pip[i]
'''trem = [0,0,0,0,0,0,0,0]
for i1 in range(10):
    #w1=1 * (i1+1)
    for i2 in range(10):
        #w2=0.6 * (i2+1)
        for i3 in range(10):
           #w3=5 * (i3 +1)
           for i4 in range(10):
              #w4=0.4 * (i4+1)
              for i5 in range(10):
                 #w5=0.5 * (i5 +1)
                 for i6 in range(10):
                     
                     for i7 in range(10):
                         
                         w4=w4 +0.1
                         pip = new_pipl_filt()
                         pipl_metrik()
                         new_sr_sr()
                         print(sred(mark_mas))
                         print(w4)
                         if sred(mark_mas)>trem[0]:
                             trem[0]=sred(mark_mas)
                             trem[1]=w1
                             trem[2]=w2
                             trem[3]=w3
                             trem[4]=w4
                             trem[5]=w5
                             trem[6]=w6
                             trem[7]=w7
                         
                         #print(trem)
                     print(trem)
                 print(trem)
        
        print(trem)
    
print(trem)  ''' 
def newrad_2(mas):
    nm =[]
    res = []
    mase = []
    for i in range(len(mas)):
        mase.append(mas[i])
    mase.sort()
    if len(mase)==1:
        res.append(mase)
        return res
    for i in range(len(mase)-1):
        nm.append(mase[i+1]-mase[i])
    
    m = sred(nm)
    q=0
    for i in range(len(nm)):
        if nm[i]> m :
            
            newm = []
            newm = mase[q:i+1]
            q = i+1
            res.append(newm)
            del(newm)
    res.append(mase[q:len(mase)])
    return res
new_sr_sr()
print(sred(mark_mas))                    