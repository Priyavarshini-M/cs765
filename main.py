import numpy as np
import pandas as pd
import plotly.express as px


import os
import ipywidgets as widgets
from ipywidgets import interact, interact_manual
import IPython.display
from IPython.display import display, clear_output

from zipfile import ZipFile

#zip_file = ZipFile("atussum_0321.csv.zip")

#df = pd.read_csv(zip_file.open('atussum_0321.csv'))
df = pd.read_csv('atussum_0321.csv')
ageBins = [False]*2
numOfChildBins = [False]*3
sportsBins = [False]*2
leisureBins = [False]*2

def plotBarGraph(data):
  keys = data.keys()
  key_str = []
  for k in keys:
    key_str.append(str(k))
  fig = px.bar(x=key_str,y=data)
  fig.update_xaxes(type='category')
  fig.show()

def createNewBins(newDf,key,step,start,end):
  bins =[*range(start,end+1,step)]
  if key not in ['t130199','t010101','t120199']:
    labels = [*range(1,int((end/step)))]
  else:
    labels = [*range(0,int((end/step)))]
  binDF=pd.cut(newDf[key], bins=bins,labels=labels,include_lowest=True)
  return binDF

def binAge(newDf,varList,i,reorder=0):
    if ageBins[0] == False:
      #Default Binning
      step = 10
      start = 15
      end = 85
      binDF=createNewBins(newDf,varList[i],step,start,end)
      newDf['ageBins']=binDF.copy()
      varList[i]='ageBins'
      if reorder == 1:
        ageBins[0] = True
    elif ageBins[1] == False:
      #reordering
      step = 15
      start = 15
      end = 85
      binDF=createNewBins(newDf,varList[i],step,start,end)
      newDf['ageBins']=binDF.copy()
      varList[i]='ageBins'
      if reorder == 1:
        ageBins[0:] = [False]*2

def binEmploymentType(newDF):
  #only one way of binning
  newDF['TELFS'] = newDF['TELFS'].replace([1,2],1)
  newDF['TELFS'] = newDF['TELFS'].replace([3,4,5],2)

def binNumOfChild(newDF,varList,i,reorder=0):
  maxchild = newDF['TRCHILDNUM'].max()
  if numOfChildBins[0] == False:
    #default Binning 0 vs 1&More children 
    bins = [*range(1,maxchild+1)]
    newDF['childBins'] = newDF['TRCHILDNUM'].replace(0,'No children')
    newDF['childBins'] = newDF['TRCHILDNUM'].replace(bins,'Have Children')
    varList[i]='childBins'
    if reorder == 1:
      numOfChildBins[0]=True
  elif numOfChildBins[1] == False:
    #Binning 0,1,2,3 vs More than 3 children
    bins = [*range(4,maxchild+1)]
    newDF['childBins'] = newDF['TRCHILDNUM']
    newDF['childBins']= newDF['childBins'].replace(bins,5)
    varList[i]='childBins'
    if reorder == 1:
      numOfChildBins[1]=True
  elif numOfChildBins[2] == False:
    # drop rows having more than 5 children
    bins = [*range(6,maxchild+1)]
    dropIndex=newDF[newDF.childBins.isin(bins)].index
    newDF.drop(dropIndex, inplace=True)
    varList[i]='TRCHILDNUM'
    if reorder == 1:
      numOfChildBins[0:] = [False]*3
  return newDF

def binSports(newDF,varList,actKey,reorder=0):
  if sportsBins[0] == False:
    binDF=createNewBins(newDF,actKey,10,0,1440)
    newDF['sportsBin']=binDF.copy()
    bins = [*range(7,144)]
    newDF['sportsBin']=newDF['sportsBin'].replace(bins,7)
    varList.append('sportsBin')
    if reorder==1:
      sportsBins[0]=True
  elif sportsBins[1]==False:
    binDF=createNewBins(newDF,actKey,60,0,1440)
    newDF['sportsBin']=binDF.copy()
    bins = [*range(2,24)]
    newDF['sportsBin']=newDF['sportsBin'].replace(bins,2)
    varList.append('sportsBin')
    if reorder==1:
      sportsBins[0:] = [False]*2

def binLeisure(newDF,varList,actKey,reorder=0):
  if leisureBins[0] == False:
    binDF=createNewBins(newDF,actKey,10,0,1440)
    newDF['leisureBin']=binDF.copy()
    bins = [*range(7,144)]
    newDF['leisureBin']=newDF['leisureBin'].replace(bins,7)
    varList.append('leisureBin')
    if reorder==1:
      leisureBins[0]=True

def defaultBinning(varList, actList=None):
  varList = [i for i in varList if i is not None]
  actList = [i for i in actList if i is not None]

  newDF = df.copy()
  #defaultBins for each variable
  for i in range(len(varList)):
    if varList[i] == 'TEAGE':
      binAge(newDF,varList,i)
    elif varList[i] == 'TELFS':
      binEmploymentType(newDF)
    elif varList[i] == 'TRCHILDNUM':
      newDF=binNumOfChild(newDF,varList,i)

  if len(actList) != 0:
    if actList[0] == 't130199':
      #drop the biased data
      bins = [*range(0,10)]
      dropIndex=newDF[newDF.t130199.isin(bins)].index
      newDF.drop(dropIndex , inplace=True)
      binSports(newDF,varList,actList[0])

    elif actList[0] == 't120199':
      bins = [*range(0,10)]
      dropIndex=newDF[newDF.t120199.isin(bins)].index
      newDF.drop(dropIndex , inplace=True)
      binLeisure(newDF,varList,actList[0])

  tempDF = newDF.groupby(varList)["TUCASEID"].count()
  plotBarGraph(tempDF)
  del newDF

def reorderBins(varList, actList=None):
  varList = [i for i in varList if i is not None]
  actList = [i for i in actList if i is not None]
  newDF = df.copy()
  #defaultBins for each variable
  for i in range(len(varList)):
    if varList[i] == 'TEAGE':
      binAge(newDF,varList,i,1)
    elif varList[i] == 'TELFS':
      binEmploymentType(newDF,1)
    elif varList[i] == 'TRCHILDNUM':
      newDF=binNumOfChild(newDF,varList,i,1)
      
  if len(actList) != 0:
    if actList[0] == 't130199':
      #drop the biased data 
      bins = [*range(0,10)]
      dropIndex=newDF[newDF.t130199.isin(bins)].index
      newDF.drop(dropIndex , inplace=True)
      binSports(newDF,varList,actList[0],1)

    elif actList[0] == 't120199':
      bins = [*range(0,10)]
      dropIndex=newDF[newDF.t120199.isin(bins)].index
      newDF.drop(dropIndex , inplace=True)
      binLeisure(newDF,varList,actList[0])
  tempDF = newDF.groupby(varList)["TUCASEID"].count()
  plotBarGraph(tempDF)
  del newDF
  
# Logic for drop down
variableDropDown = []
def dropdown(variables1, variables2, showWidget, userSelectedVariables1, userSelectedVariables2):
    clear_output()
    output = widgets.Output()
    # userSelectionSize1 = len(userSelectedVariables1)
    # userSelectionSize2 = len ()
    print (userSelectedVariables1)
    print (userSelectedVariables2)

    button = widgets.Button(description="Clear All Values")

    if (showWidget) :
      for i in range(0,4):
        variableDropDown.append(widgets.Dropdown(options = variables1, value=None, description='Variable ' + str(i+1) + ' :', disabled=False))
      for i in range(4, 6):
        variableDropDown.append(widgets.Dropdown(options = variables2, value=None, description='Variable ' + str(i+1) + ' :', disabled=False))
    else:
      defaultBinning(userSelectedVariables1, userSelectedVariables2)

    def addToUserSelectedVariables(choice, i, flag):
      clear_output()
      if flag :
        if choice not in userSelectedVariables1:
          userSelectedVariables1[i] = choice
      else:
        if choice not in userSelectedVariables2:
          userSelectedVariables2[i] = choice
      dropdown(variables1, variables2, False, userSelectedVariables1, userSelectedVariables2)    

    def variable1_eventhandler(change):
        choice = change.new
        addToUserSelectedVariables(choice, 0, True) 

    def variable2_eventhandler(change):
        choice = change.new
        addToUserSelectedVariables(choice, 1, True)

    def variable3_eventhandler(change):
        choice = change.new
        addToUserSelectedVariables(choice, 2, True)

    def variable4_eventhandler(change):
        choice = change.new
        addToUserSelectedVariables(choice, 3, True)

    def variable5_eventhandler(change):
        choice = change.new
        addToUserSelectedVariables(choice, 0, False)

    def variable6_eventhandler(change):
        choice = change.new
        addToUserSelectedVariables(choice, 1, False)

    def on_button_clicked(b):
        clear_output()
        global userSelectedVariables
        userSelectedVariables1 = [None] * 4
        userSelectedVariables2 = [None] * 2
        variableDropDown.clear()
        dropdown(variables1, variables2, True, userSelectedVariables1, userSelectedVariables2)  
       
    variableDropDown[0].observe(variable1_eventhandler, names='value')
    variableDropDown[1].observe(variable2_eventhandler, names='value')
    variableDropDown[2].observe(variable3_eventhandler, names='value')
    variableDropDown[3].observe(variable4_eventhandler, names='value')
    variableDropDown[4].observe(variable5_eventhandler, names='value')
    variableDropDown[5].observe(variable6_eventhandler, names='value')
    # variableDropDown[6].on_click(on_button_clicked)
    

    input_widgets = widgets.VBox(variableDropDown)

    display(input_widgets)
    display(button)
    button.on_click(on_button_clicked)
    IPython.display.clear_output(wait=True)    


variables_list1 = [('', ''), ('age', 'TEAGE'), ('gender', 'TESEX'), ('emp_type', 'TELFS'), ('child_num', 'TRCHILDNUM')]
variables_list2 = [('', ''), ('sports', 't130199'), ('leisure', 't120199')]
userSelectedVariables1 = [None] * 4
userSelectedVariables2 = [None] * 2
dropdown(variables_list1, variables_list2,  True, userSelectedVariables1, userSelectedVariables2)