import numpy as np
import pandas as pd
import plotly.express as px


import os
import ipywidgets as widgets
from ipywidgets import interact, interact_manual
import IPython.display
from IPython.display import display, clear_output

from zipfile import ZipFile

zip_file = ZipFile("atussum_0321.csv.zip")

df = pd.read_csv(zip_file.open('atussum_0321.csv'))

def plotBarGraph(data):
  groups = [*range(1,data.shape[0] + 1)]
  fig = px.bar(x=groups,y=data)
  #plt.bar(groups, data, color ='maroon',width = 0.4)
  fig.show()

def createBins(varList, actList=None):
  varList = [i for i in varList if i is not None]
  actList = [i for i in actList if i is not None]
  if len(actList) != 0:
    bins =[*range(0,1441,10)]
    s = df.groupby(pd.cut(df[actList[0]], bins=bins)).size()
    df['binned']=s
    varList.append('binned')
  tempDF = df.groupby(varList)["TUCASEID"].count()
  plotBarGraph(tempDF)

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
      createBins(userSelectedVariables1, userSelectedVariables2)

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
