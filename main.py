"""
This is the general working file for accessing the different analysis tools.
All of the tools will be accessed from here to keep clutter down and keep the modules clean.
This also may be used for developing new tools, but they must be moved to their own modules when done.
Export or pickling may happen here for now but eventually a suite of auxiliary functions to handle spreadsheets will be created.
"""
import cairo
from FinMesh.iex import stock

# Cairo uses key stats, balance sheet, and price data

class CustomStockAnalysis:
    def __init__(self, methods):
        self.m = methods

    def print_methods(self):
        print(methods)

methods = ['Cairo', 'Berlin', 'Delhi']
ut = CustomStockAnalysis(methods)
ut.print_methods()
