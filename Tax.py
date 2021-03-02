import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

#Importing CSV
tax = pd.read_csv('Open Data Tax Receipts Source.csv')
live_reg = pd.read_csv('Live Register.csv')
#pd.set_option('display.max_columns',50)

#Checking Tax CSV
#print(tax.head())
#print(tax.shape)

#Insert column names
cols = ['Year', 'MonthLong', 'Actual/Projected', 'Tax Head', 'Amount (000s)']
tax_cols = pd.read_csv('Open Data Tax Receipts Source.csv', names=cols)

#Checking dataframe post column insertion / looking for one extra row
#print(tax_cols.head())
#print(tax_cols.shape)

#Creating a combined date column
date = pd.to_datetime(tax_cols['Year'].astype(str) + tax_cols['MonthLong'], format='%Y%B', errors='coerce')
tax_cols['FullDate'] = date + pd.offsets.MonthEnd()

#Checking for errors brings up 510 errors
#print(tax_cols.isna().sum())

#Checked the data set and there is some whitespace after 'December  ' which is removed by this
tax_cols['MonthLong'] = tax_cols['MonthLong'].apply(lambda x: x.strip())

#Running this again to ensure the FullDate column is filled in full. I would normally remove the date line above but keeping it as an example that I check the errors
date = pd.to_datetime(tax_cols['Year'].astype(str) + tax_cols['MonthLong'], format='%Y%B', errors='coerce')
tax_cols['FullDate'] = date + pd.offsets.MonthEnd()

#Checking for errors again to ensure none are pulled through - all is ok
#print(tax_cols.isna().sum())

#Create abbreviated column for ease of charting
tax_heads = tax_cols['Tax Head'].unique()

tax_heads_list = []

for i in tax_heads:
        tax_heads_list.append(i)

#print(tax_heads_list)

tax_dict = {'Tax Head': tax_heads_list,
        'Tax Heads Short': ['CUST','EXD','CGT','SD','IT','CORP','VAT','TEL','MOT','UNA','CAT','LPT']}

tax_dict_pd = pd.DataFrame(data=tax_dict)
#print(tax_dict_pd)

tax_cols_short = tax_cols.merge(tax_dict_pd, on='Tax Head', how='left')
print(tax_cols_short)

actual_filter = (tax_cols_short['Actual/Projected'] == 'Actual Outturn')
tax_final = tax_cols_short[actual_filter]

print(tax_final['Actual/Projected'].unique())
print(tax_final)

#Looking at live register data
#print(live_reg.head())

#Adding a full date column to the live reg info so I can match the tax table with live reg table
date_live_reg = pd.to_datetime(live_reg['Month'], format='%YM%M')
live_reg['FullDate'] = date_live_reg + pd.offsets.MonthEnd()

live_reg['NewYear'] = live_reg['FullDate'].dt.strftime('%Y')

#print(live_reg.head)

#Checking live reg table for errors

#print(live_reg.isna().sum())

#print(live_reg['VALUE'].isna().groupby(live_reg['NewYear']).sum())

live_reg_clean = live_reg.dropna(axis=0)

#print(live_reg_clean)

#Creating a maak filter that just contains all ages, both sexes, all classes
live_reg_filter = ((live_reg_clean['Age Group'] == 'All ages') & (live_reg_clean['Sex'] == 'Both sexes') & (live_reg_clean['Social Welfare Scheme'] == 'All classes'))

#Checking the mask works
live_reg_final = live_reg_clean[live_reg_filter]

#print(live_reg_final['VALUE'].isna().groupby(live_reg_final['NewYear']).sum())

print(live_reg_final)

#Merging the tables
tax_live_reg_final = pd.merge_asof(tax_final, live_reg_final, on='FullDate', direction='forward')
print(tax_live_reg_final)

#Checking there are no errors
print(tax_live_reg_final.isna().sum())

#Tables - need to adjust for profile v actual outturn in tax
#total_tax_live_reg_actual = (tax_live_reg_actual.groupby(['Year'])['Amount (000s)'].sum())
#total_tax_live_reg_actual.plot(kind='bar', color='limegreen', width=0.6)
#plt.xlabel('Year')
#plt.ylabel('Tax Revenue in €bn')
#plt.title('Tax Revenue per Year')
#plt.show()

#print(tax_live_reg_actual.columns)