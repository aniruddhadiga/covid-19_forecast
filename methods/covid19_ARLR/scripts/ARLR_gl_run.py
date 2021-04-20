import sys, os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import pdb
from joblib import Parallel, delayed
import multiprocessing
from scipy.stats import entropy
from datetime import datetime, timedelta
import epiweeks as epi
from scipy.stats import pearsonr
from scipy.signal import correlate
import matplotlib
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.fftpack import fft, ifft
from scipy.optimize import nnls
import scipy.stats as stats
from scipy.optimize import leastsq
from scipy.signal import savgol_filter
from collections import defaultdict
import statsmodels.api as sm
from models import predictor_spatial_mob, predictor_spatial, predictor_ar, predictor_mob, predictor_exog

def conv_col_time(tempdf):
    for col in tempdf.columns:
        tempdf=tempdf.rename(columns={col:datetime.strptime(col,'%Y-%m-%d').date()})
    return tempdf


glcode=sys.argv[1]
hrzn_date_file=sys.argv[2]
#hrzn_date_str=[sys.argv[3]]
hrzn_date_str=[]
with open(hrzn_date_file,'r') as f:
    for line in f:
        hrzn_date_str.append(line.strip())


datadf=pd.read_csv('../input/gl_data.csv',dtype={'Province_State':str})
datadf=datadf.set_index('Country/Region')
mobdf=pd.read_csv('../input/mobility_data.csv',dtype={'scnty':str})
mobdf=mobdf.set_index('scnty')
for col in mobdf.columns:
    mobdf=mobdf.rename(columns={col:datetime.strptime(col,'%Y-%m-%d').date()})

for col in datadf.columns:
    datadf=datadf.rename(columns={col:datetime.strptime(col,'%Y-%m-%d').date()})

sdidf=pd.read_csv('../input/sdi_data.csv').rename(columns={'Unnamed: 0':'FIPS'})
sdidf['FIPS']=sdidf.FIPS.apply(lambda x: '{:05}'.format(x))
sdidf=sdidf.set_index('FIPS')
sdidf=conv_col_time(sdidf)

rsdidf=pd.read_csv('../input/rate_sdi_data.csv').rename(columns={'Unnamed: 0':'FIPS'})
rsdidf['FIPS']=rsdidf.FIPS.apply(lambda x: '{:05}'.format(x))
rsdidf=rsdidf.set_index('FIPS')
rsdidf=conv_col_time(rsdidf)

docdf=pd.read_csv('../input/doc_visit_data.csv').rename(columns={'Unnamed: 0':'FIPS'})
docdf['FIPS']=docdf.FIPS.apply(lambda x: '{:05}'.format(x))
docdf=docdf.set_index('FIPS')
docdf=conv_col_time(docdf)

dictdf={'cases':datadf, 'mob':mobdf, 'sdi':sdidf, 'doc':docdf}
step_ahead=4
#hrzn_date_str=['2020-05-17','2020-05-24','2020-05-31','2020-06-07','2020-06-14','2020-06-21','2020-06-28','2020-07-05','2020-07-12','2020-07-19']
#cntyresdf=pd.DataFrame(columns=['method','cnty','horizon','fct_date','fct','true'],index=None)
#for hrzn_date_str in [hrzn_list]:#hrzn_dates:

#tempresdf1=predictor_spatial_mob(datadf,mobdf,[cnty_list],hrzn_date_str,step_ahead)
#cntyresdf=cntyresdf.append(tempresdf,ignore_index=True)
AR_sp_outdir='../output/AR_global/AR_spatial/'
AR_sp_pkldir='../pkl/AR_spatial_global/'
tempresdf2=predictor_spatial(datadf,[glcode],hrzn_date_str,step_ahead,AR_sp_outdir, AR_sp_pkldir)
#cntyresdf=cntyresdf.append(tempresdf,ignore_index=True)
AR_outdir='../output/AR_global/'
AR_pkldir='../pkl/AR_global/'
tempresdf3=predictor_ar(datadf,mobdf,[glcode],hrzn_date_str,step_ahead, AR_outdir, AR_pkldir)
#cntyresdf=cntyresdf.append(tempresdf,ignore_index=True)
#tempresdf4=predictor_mob(datadf,mobdf,[cnty_list],hrzn_date_str,step_ahead)
#tempresdf5=predictor_exog(dictdf,[cnty_list],hrzn_date_str,step_ahead)
### exog prep dict of dataframes

print('{},{}\n'.format(glcode,hrzn_date_str))
