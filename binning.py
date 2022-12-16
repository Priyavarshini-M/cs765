import pandas as pd
import plotly.express as px

ageBins = [False]*2
numOfChildBins = [False]*3
sportsBins = [False]*2
leisureBins = [False]*2
sleepBins = [False]*3
socialBins = [False]*2

def initializeBinVars(toInit=None):
  if toInit == None:
    ageBins[0:] = [False]*2
    numOfChildBins[0:] = [False]*3
    sportsBins[0:] = [False]*2
    leisureBins[0:] = [False]*2
  elif toInit == 'ageBins':
    ageBins[0:] = [False,False]
  elif toInit == 'numOfChildBins':
    numOfChildBins[0:] = [False,False,False]
  elif toInit == 'sportBins':
    sportsBins[0:] = [False,False]
  elif toInit == 'leisureBins':
    leisureBins[0:] = [False,False]
  elif toInit == 'sleepBins':
    sleepBins[0:] = [False,False,False]
  elif toInit == 'socializeBins':
    socialBins[0:] = [False,False]

def plotBarGraph(data):
  keys = data.keys()
  key_str = []
  for k in keys:
    key_str.append(str(k))
  fig = px.bar(x=key_str,y=data)
  fig.update_xaxes(type='category')
  fig.show()

from numpy.core.fromnumeric import var
treeList = []
def creatListsAndGroup(data, varList):
  for i in range(0,len(varList)):
    newDF=data.groupby(varList[:i+1])["TUCASEID"].count()
    keys = newDF.keys()
    val = newDF.values
    key_str = []
    for k in keys:
      key_str.append(str(k))
    d = dict(zip(key_str,val))
    treeList.append(d) 
  plotBarGraph(newDF)

def createNewBins(newDf,key,step,start,end):
  bins =[*range(start,end+1,step)]
  if key not in ['t130199','t010101','t120101']:
    labels = [*range(1,int((end/step)))]
  else:
    labels = [*range(0,int((end/step)))]
  binDF=pd.cut(newDf[key], bins=bins,labels=labels,include_lowest=True)
  return binDF

def binAge(newDf,varList,i,reorder=0):
    if ageBins[0] == False:
      #Default Binning
      binDF=createNewBins(newDf,varList[i],10,15,85)
      newDf['ageBins']=binDF.copy()
      j = 1
      for k in range(15,85,10):
        newDf['ageBins']=newDf['ageBins'].replace(j,(str(k))+ '-'+str(k+10))
        j+=1
      varList[i]='ageBins'
      ageBins[0] = True
    elif ageBins[1] == False:
      #reordering
      binDF=createNewBins(newDf,varList[i],15,15,90)
      newDf['ageBins']=binDF.copy()
      j = 1
      for k in range(15,85,15):
        newDf['ageBins']=newDf['ageBins'].replace(j,(str(k))+ ' - '+str(k+15))
        j+=1
      newDf['ageBins']=newDf['ageBins'].replace(5,'75 - 85')
      varList[i]='ageBins'
      if reorder == 1:
        initializeBinVars('ageBins')

def binEmploymentType(newDF):
  #only one way of binning
  newDF['TELFS'] = newDF['TELFS'].replace([1,2],'Emp')
  newDF['TELFS'] = newDF['TELFS'].replace([3,4,5],'Unemp')

def binNumOfChild(newDF,varList,i,reorder=0):
  maxchild = newDF['TRCHILDNUM'].max()
  if numOfChildBins[0] == False:
    #default Binning 0 vs 1&More children 
    bins = [*range(1,maxchild+1)]
    newDF['childBins'] = newDF['TRCHILDNUM']
    newDF['childBins'] = newDF['childBins'].replace(0,'No children')
    newDF['childBins'] = newDF['childBins'].replace(bins,'Have Children')
    varList[i]='childBins'
    numOfChildBins[0]=True
  elif numOfChildBins[1] == False:
    #Binning 0,1,2,3 vs More than 3 children
    bins = [*range(4,maxchild+1)]
    newDF['childBins'] = newDF['TRCHILDNUM']
    for j in range(0,4):
      newDF['childBins']=newDF['childBins'].replace(j,(str(j)+' Children'))
    newDF['childBins']= newDF['childBins'].replace(bins,'More than 3 Children')
    varList[i]='childBins'
    if reorder == 1:
      numOfChildBins[1]=True
  elif numOfChildBins[2] == False:
    # drop rows having more than 5 children
    bins = [*range(6,maxchild+1)]
    dropIndex=newDF[newDF.childBins.isin(bins)].index
    newDF.drop(dropIndex, inplace=True)
    for j in range(0,6):
      newDF['childBins']=newDF['childBins'].replace(j,(str(j)+' Children'))
    varList[i]='childBins'
    if reorder == 1:
      initializeBinVars('numOfChildBins')

def binSports(newDF,varList,actKey,reorder=0):
  if sportsBins[0] == False:
    binDF=createNewBins(newDF,actKey,60,0,1440)
    newDF['sportsBin']=binDF.copy()
    bins = [*range(1,24)]
    newDF['sportsBin']=newDF['sportsBin'].replace(0,'Less than 1 Hr')
    newDF['sportsBin']=newDF['sportsBin'].replace(bins,'More than 1 Hr') #replacing rest as second bin
    varList.append('sportsBin')
    
    sportsBins[0]=True
  elif sportsBins[1]==False:
    binDF=createNewBins(newDF,actKey,10,0,1440)
    newDF['sportsBin']=binDF.copy()
    bins = [*range(6,144)]
    for i in range(0,6):
      newDF['sportsBin']=newDF['sportsBin'].replace(i,(str((i+1)*10)+' Mins'))
    newDF['sportsBin']=newDF['sportsBin'].replace(bins,'More than 1 Hrs') #everything after 6th bin
    varList.append('sportsBin') 
    if reorder==1:
      initializeBinVars('sportBins')
      
def binSleep(newDF,varList,actKey,reorder=0):
  if sleepBins[0] == False:
    binDF=createNewBins(newDF,actKey,60,0,1440)
    newDF['sleepBin']=binDF.copy()
    for i in range(24):
      newDF['sleepBin']=newDF['sleepBin'].replace(i,(str(i)+' Hrs'))
    varList.append('sleepBin')
    sleepBins[0]=True
  elif sleepBins[1]==False:
    binDF=createNewBins(newDF,actKey,60,0,1440)
    newDF['sleepBin']=binDF.copy()
    bins1 = [*range(0,6)]
    bins2 = [*range(6,13)]
    bins3 = [*range(13,24)]
    newDF['sleepBin']=newDF['sleepBin'].replace(bins1,'Less than 6hrs')
    newDF['sleepBin']=newDF['sleepBin'].replace(bins2,'6-12 Hrs')
    newDF['sleepBin']=newDF['sleepBin'].replace(bins3,'More than 12hrs')
    varList.append('sleepBin')
    if reorder==1:
      sleepBins[1]=True
  elif sleepBins[2] == False:
    binDF=createNewBins(newDF,actKey,360,0,1440)
    newDF['sleepBin']=binDF.copy()
    newDF['sleepBin']=newDF['sleepBin'].replace(0,'0-5 Hrs')
    newDF['sleepBin']=newDF['sleepBin'].replace(1,'6-12 Hrs')
    newDF['sleepBin']=newDF['sleepBin'].replace(2,'13-17 Hrs')
    newDF['sleepBin']=newDF['sleepBin'].replace(3,'18-23 Hrs')
    varList.append('sleepBin')
    if reorder==1:
      initializeBinVars('sleepBins')
    
def binSocialize(newDF,varList,actKey,reorder=0):
  if socialBins[0] == False:
    binDF=createNewBins(newDF,actKey,60,0,1440)
    newDF['socializeBin']=binDF.copy()
    bins = [*range(5,24)]
    for i in range(0,5):
      newDF['socializeBin']=newDF['socializeBin'].replace(i,(str(i)+' Hrs'))
    newDF['socializeBin']=newDF['socializeBin'].replace(bins,'More than 4Hrs') #everything after 4hrs
    varList.append('socializeBin')
    socialBins[0]=True
  elif socialBins[1]==False:
    binDF=createNewBins(newDF,actKey,60,0,1440)
    newDF['socializeBin']=binDF.copy()
    bins = [*range(1,24)]
    newDF['socializeBin']=newDF['socializeBin'].replace(0,'Less Than 1 Hr')
    newDF['socializeBin']=newDF['socializeBin'].replace(bins,'More Than 1 Hr') #replacing rest as second bin
    varList.append('socializeBin')
    if reorder==1:
      initializeBinVars('socializeBins')
      
def getTreeList():
    return treeList

def clearTreeList():
    treeList.clear()