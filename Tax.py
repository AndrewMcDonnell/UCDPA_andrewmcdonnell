import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Importing CSV
tax = pd.read_csv('Open Data Tax Receipts Source.csv')

#Checking CSV
print(tax.head())
print(tax.shape)

#After checking data we need to insert column names
cols = ['Year', 'MonthLong', 'Actual/Projected', 'Tax Head', 'Amount (000s)']
tax_cols = pd.read_csv('Open Data Tax Receipts Source.csv', names=cols)

#Checking dataframe post column insertion / looking for one extra row
print(tax_cols.head())
print(tax_cols.shape)

#Adding the last day of each month
date = pd.to_datetime(tax_cols['Year'].astype(str) + tax_cols['MonthLong'], format='%Y%B', errors='coerce')
tax_cols['FullDate'] = date + pd.offsets.MonthEnd()

#Checking for errors
print(tax_cols.isna().sum())

#Checked date set and there is some shitespace after 'December' which is removed by this
tax_cols['MonthLong'] = tax_cols['MonthLong'].apply(lambda x: x.strip())

#Running this again to ensure the FullDate column is filled in full
date = pd.to_datetime(tax_cols['Year'].astype(str) + tax_cols['MonthLong'], format='%Y%B', errors='coerce')
tax_cols['FullDate'] = date + pd.offsets.MonthEnd()

#After looking at file it turns out December has a few blank spaces after it.
print(tax_cols.isna().sum())
print(tax_cols.head())