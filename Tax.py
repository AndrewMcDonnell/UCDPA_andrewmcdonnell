import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

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

#Looking at live register data
live_reg = pd.read_csv('Live Register.csv')

#Reformatting the Month column so I can match it with the tax info
date_live_reg = pd.to_datetime(live_reg['Month'], format='%YM%M')
live_reg['FullDate'] = date_live_reg + pd.offsets.MonthEnd()

print(live_reg.head())

#Creating a maak filter that just contains all ages, both sexes, all classes
filt = ((live_reg['Age Group'] == 'All ages') & (live_reg['Sex'] == 'Both sexes') & (live_reg['Social Welfare Scheme'] == 'All classes'))

#Checking the mask works
live_reg_merge = live_reg[filt]
print(live_reg_merge)

#Merging the tables
tax_live_reg_merge = pd.merge_asof(tax_cols, live_reg_merge, on='FullDate', direction='forward')
print(tax_live_reg_merge)

actual_filt = (tax_live_reg_merge['Actual/Projected'] == 'Actual Outturn')
tax_live_reg_actual = tax_live_reg_merge[actual_filt]


#Tables - need to adjust for profile v actual outturn in tax
total_tax_live_reg_actual = (tax_live_reg_actual.groupby(['Year'])['Amount (000s)'].sum())
total_tax_live_reg_actual.plot(kind='bar', color='limegreen', width=0.6)
plt.xlabel('Year')
plt.ylabel('Tax Revenue in €bn')
plt.title('Tax Revenue per Year')
plt.show()