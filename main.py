import numpy as np
import pandas as pd
import plotly.express as px

import ipywidgets as widgets
from ipywidgets import Layout
from IPython.display import display, clear_output

from zipfile import ZipFile
from tree import drawTree
from binning import initializeBinVars, getTreeList, clearTreeList, binAge, binEmploymentType, binNumOfChild, binSports, binSocialize, binSleep, creatListsAndGroup

zip_file = ZipFile("atussum_0321.csv.zip")
df = pd.read_csv(zip_file.open('atussum_0321.csv'))


def defaultBinning(varList, actList=None):
  varList = [i for i in varList if i is not None]
  actList = [i for i in actList if i is not None]
  initializeBinVars()
  clearTreeList()
  newDF = df.copy()
  #defaultBins for each variable
  for i in range(len(varList)):
    if varList[i] == 'TESEX':
      newDF['TESEX'] = newDF['TESEX'].replace(1,'Male')
      newDF['TESEX'] = newDF['TESEX'].replace(2,'Female')
    if varList[i] == 'TEAGE':
      binAge(newDF,varList,i)
    elif varList[i] == 'TELFS':
      binEmploymentType(newDF)
    elif varList[i] == 'TRCHILDNUM':
      binNumOfChild(newDF,varList,i)

  if len(actList) != 0:
    if actList[0] == 't130199':
      #drop the biased data
      bins = [*range(0,10)]
      dropIndex=newDF[newDF.t130199.isin(bins)].index #dropping bins in range 0 to 10
      newDF.drop(dropIndex , inplace=True)
      binSports(newDF,varList,actList[0])

    elif actList[0] == 't120101':
      binSocialize(newDF,varList,actList[0])
    
    elif actList[0] == 't010101':
      binSleep(newDF,varList,actList[0])

  creatListsAndGroup(newDF,varList)
  del newDF

def reorderBins(varList, actList=None,reorderVar=None):
  varList = [i for i in varList if i is not None]
  actList = [i for i in actList if i is not None]
  clearTreeList()
  newDF = df.copy()
  #defaultBins for each variable
  for i in range(len(varList)):
    if varList[i] == 'TESEX':
      newDF['TESEX'] = newDF['TESEX'].replace(1,'Male')
      newDF['TESEX'] = newDF['TESEX'].replace(2,'Female')
    elif varList[i] == 'TEAGE':
      if reorderVar=='TEAGE':
        binAge(newDF,varList,i,1)
      else:
        binAge(newDF,varList,i)
    elif varList[i] == 'TELFS':
      if reorderVar=='TELFS':
        binEmploymentType(newDF)
      else:
        binEmploymentType(newDF)
    elif varList[i] == 'TRCHILDNUM':
      if reorderVar=='TRCHILDNUM':
        binNumOfChild(newDF,varList,i,1)
      else:
        binNumOfChild(newDF,varList,i)
      
  if len(actList) != 0:
    if actList[0] == 't130199':
      bins = [*range(0,10)]
      dropIndex=newDF[newDF.t130199.isin(bins)].index
      newDF.drop(dropIndex , inplace=True)
      if reorderVar=='t130199':
        binSports(newDF,varList,actList[0],1)
      else:
        binSports(newDF,varList,actList[0])

    elif actList[0] == 't120101':
      if reorderVar=='t120101':
        binSocialize(newDF,varList,actList[0],1)
      else:
        binSocialize(newDF,varList,actList[0])
    elif actList[0] == 't010101':
      if reorderVar == 't010101':
        binSleep(newDF,varList,actList[0],1)
      else:
        binSleep(newDF,varList,actList[0])

  creatListsAndGroup(newDF,varList)
  del newDF
# Logic for drop down
variableDropDown = []
def dropdown(variables1, variables2, showWidget, userSelectedVariables1, userSelectedVariables2):

    button = widgets.Button(description="Clear All", layout=Layout(width='99%'))
    button.style.button_color = 'lightgreen'

    if (showWidget) :
      for i in range(0,4):
        variableDropDown.append(widgets.Dropdown(options = variables1, value=None, description='Variable ' + str(i+1) + ' :', disabled=False))
        variableDropDown.append(widgets.Button(description="Reorder"))
        variableDropDown[-1].style.button_color = 'lightblue'
      for i in range(4, 5):
        variableDropDown.append(widgets.Dropdown(options = variables2, value=None, description='Variable ' + str(i+1) + ' :', disabled=False))
        variableDropDown.append(widgets.Button(description="Reorder"))
        variableDropDown[-1].style.button_color = 'lightblue'

    def addToUserSelectedVariables(choice, i, flag):
      if flag :
        if choice not in userSelectedVariables1:
          userSelectedVariables1[i] = choice
      else:
        if choice not in userSelectedVariables2:
          userSelectedVariables2[i] = choice
      defaultBinning(userSelectedVariables1, userSelectedVariables2)
      drawTree(getTreeList())
      
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

    def button1_eventhandler(b): 
      reorderBins(userSelectedVariables1, userSelectedVariables2, userSelectedVariables1[0])
      drawTree(getTreeList())

    def button2_eventhandler(b): 
      reorderBins(userSelectedVariables1, userSelectedVariables2, userSelectedVariables1[1])
      drawTree(getTreeList())

    def button3_eventhandler(b): 
      reorderBins(userSelectedVariables1, userSelectedVariables2, userSelectedVariables1[2])
      drawTree(getTreeList())

    def button4_eventhandler(b): 
      reorderBins(userSelectedVariables1, userSelectedVariables2, userSelectedVariables1[3])
      drawTree(getTreeList())

    def button5_eventhandler(b): 
      reorderBins(userSelectedVariables1, userSelectedVariables2, userSelectedVariables1[4])
      drawTree(getTreeList())

    def on_button_clicked(b):
        clear_output()
        # global userSelectedVariables
        userSelectedVariables1 = [None] * 4
        userSelectedVariables2 = [None] * 2
        variableDropDown.clear()
        dropdown(variables1, variables2, True, userSelectedVariables1, userSelectedVariables2)  
       
    # dropDown event handlers
    variableDropDown[0].observe(variable1_eventhandler, names=['value'])
    variableDropDown[2].observe(variable2_eventhandler, names=['value'])
    variableDropDown[4].observe(variable3_eventhandler, names=['value'])
    variableDropDown[6].observe(variable4_eventhandler, names=['value'])
    variableDropDown[8].observe(variable5_eventhandler, names=['value'])

    # reorder button event handlers
    variableDropDown[1].on_click(button1_eventhandler)
    variableDropDown[3].on_click(button2_eventhandler)
    variableDropDown[5].on_click(button3_eventhandler)
    variableDropDown[7].on_click(button4_eventhandler)
    variableDropDown[9].on_click(button5_eventhandler)

    widget1 = widgets.HBox([variableDropDown[0], variableDropDown[1]])
    widget2 = widgets.HBox([variableDropDown[2], variableDropDown[3]])
    widget3 = widgets.HBox([variableDropDown[4], variableDropDown[5]])
    widget4 = widgets.HBox([variableDropDown[6], variableDropDown[7]])
    widget5 = widgets.HBox([variableDropDown[8], variableDropDown[9]])

    input_widgets = widgets.VBox([widget1, widget2, widget3, widget4, widget5])

    display(input_widgets)
    display(button)
    button.on_click(on_button_clicked)


variables_list1 = [('', ''), ('age', 'TEAGE'), ('gender', 'TESEX'), ('emp_type', 'TELFS'), ('child_num', 'TRCHILDNUM')]
variables_list2 = [('', ''), ('sports', 't130199'), ('socialize', 't120101'), ('sleep', 't010101')]
userSelectedVariables1 = [None] * 4
userSelectedVariables2 = [None] * 2
dropdown(variables_list1, variables_list2,  True, userSelectedVariables1, userSelectedVariables2)
