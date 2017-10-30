# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 20:16:03 2017

@author: Xiaojun
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dfall = pd.DataFrame()
for yr in range(1977,2018):
#    folder = 'C:\\Users\\Agnes\\Documents\\DS\\1977-2017_csv\\'
    folder = 'C:\\Users\\Xiaojun\\Documents\\PYTHON\\NSF\\1977-2017_csv\\'
    fname = folder+str(yr)+'.csv'
    '''
    all columns:
    ['ARRAAmount', 'AbstractNarration', 'AwardAmount', 'AwardEffectiveDate',
       'AwardExpirationDate', 'AwardID', 'AwardInstrument_Value', 'AwardTitle',
       'Directorate_LongName', 'Division_LongName', 'Institution_CityName',
       'Institution_CountryName', 'Institution_Name', 'Institution_StateCode',
       'Institution_StateName', 'Institution_ZipCode', 'Investigator_EndDate',
       'Investigator_FirstName', 'Investigator_LastName',
       'Investigator_RoleCode', 'Investigator_StartDate', 'Organization_Code',
       'ProgramElement_Code', 'ProgramElement_Text', 'ProgramReference_Code',
       'ProgramReference_Text']
    '''
    selected_columns = ['ARRAAmount','AwardAmount','AwardEffectiveDate',
       'AwardExpirationDate', 'AwardID','AwardInstrument_Value',
       'Directorate_LongName', 'Division_LongName', 'Institution_CityName',
       'Institution_CountryName', 'Institution_Name', 'Institution_StateName',
       'Institution_StateCode']
    df = pd.read_csv(fname, usecols=selected_columns, encoding = "ISO-8859-1")
    df['FY'] = yr
    dfall = pd.concat([dfall, df],ignore_index=True)
dfall = dfall.drop_duplicates()
    
# Summarize award by year
#award_by_year = dfall.AwardAmount.groupby(dfall.FY).sum()
eff_yr = dfall.AwardEffectiveDate.apply(lambda x: x[-4:]).astype(int)
eff_yr[eff_yr<1977]=np.nan
award_by_year = dfall.AwardAmount.groupby(eff_yr).sum()
arra_by_year = dfall.ARRAAmount.groupby(eff_yr).sum()
arra_by_year = arra_by_year.fillna(0)
plt.bar(award_by_year.index,award_by_year.values/1e9,color='m')
plt.bar(arra_by_year.index,award_by_year.values/1e9-arra_by_year.values/1e9,color='g')
plt.ylabel('Award amount (billion)')
plt.legend(['ARRA'])
    
# Summarize award by states
award_by_state = dfall.groupby([eff_yr,'Institution_StateCode','Institution_StateName']).AwardAmount

# Summarize award by research areas
award_dur = (pd.to_datetime(dfall.AwardExpirationDate)-pd.to_datetime(dfall.AwardEffectiveDate)).dt.days
award_dur[award_dur<=0] = np.nan
dfall['amount_per_year']=dfall.AwardAmount/(award_dur/365)
award_by_directorate = dfall[eff_yr==2017].groupby(['Directorate_LongName']).AwardAmount
award_by_directorate_sum = award_by_directorate.sum().sort_values(ascending=False)
direct = award_by_directorate_sum.index.unique()
# Choose the main research areas
areas = direct[direct.str.contains('Direct For |Directorate')]
plt.pie(award_by_directorate[areas], labels=award_by_directorate[areas].index, autopct='%1.1f%%')
plt.title('2017 NSF award by research areas')
# Normalize amount by duration
award_by_directorate_per_year = dfall[eff_yr==2017].groupby(['Directorate_LongName']).amount_per_year
per_year_mean = award_by_directorate_per_year.mean()
per_year_std = award_by_directorate_per_year.std()
plt.barh(range(len(per_year_mean)))


