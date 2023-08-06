# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 16:37:59 2020

@author: pierr
"""
import os
import backtest.webapp
def run():
    exec(open("backtest/webapp.py").read())
def run2():
    return backtest.webapp
def run3():
    os.system("python webapp.py")