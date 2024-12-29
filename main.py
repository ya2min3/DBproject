#import sys
#import math
#import random
#import os
#from PyQt5 import (QtGui, QtCore, QtWidgets)
#import psycopg2
#from PyQt5.QtCore import QSortFilterProxyModel, Qt
#from PyQt5.QtWidgets import QComboBox, QApplication, QCompleter
import jobs_search

#-------------------------------------------SEARCH BAR------------------------------------------------
reserch_params= jobs_search.search_bar()
research_results = jobs_search.search_results(reserch_params)
print(research_results)