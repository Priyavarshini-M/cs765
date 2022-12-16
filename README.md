#Tree Graph - Interactive Population Distribution Visualizer


## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This tool helps visualize the distribution of the samples across groupings formed by 
different variables. It lets the user see different possible subgroups and helps them 
figure out a good way to divide the data population.

## Technologies

* Python 3.9.9

## Setup

* Pre requisites:
	* Python version 3.9.9 and above
	* VS Code
		* Extensions:
			Jupyter v2022.8.1002431955 (Microsoft)
			
	* To run the code locally, once the pre requisite are downloaded run the Makefile
	'''
	$make
	'''
	This installs the required python Packages:
		* Numpy
		* Pandas
		* plotly
		* ete3
		* Pillow
		* PyQt5
		* ipywidgets
		
*Steps to perform after downloading all packages

1. Open VS code on the repository directory
2. Right click on main.py and select 'Run Current File in interactive Window'
3. After each interaction the tree will be rendered in tree.png