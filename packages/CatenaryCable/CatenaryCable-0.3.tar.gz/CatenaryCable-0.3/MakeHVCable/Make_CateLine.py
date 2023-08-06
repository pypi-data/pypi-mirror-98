#
#
#
import sys
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.metrics import r2_score
from CatenaryPaulC import *

#############################################################
def PlotTransmissionMap( df, df_mod,  TITLE ):
    fig, (ax1,ax2) = plt.subplots( 2, figsize=(10,15) )

    #######################
    df.plot.scatter( x='U', y='H' , marker='^', s=100,
                     alpha=0.5 ,  ax=ax1 )
    df_mod.plot.line( x='U', y='H' , color='red' , alpha=0.5 ,
                      legend=None , ax=ax1 )
    for i,row in df.iterrows():
        ax1.text( row['U'], row['H'], row['Name'], color='red', rotation=90)
    ax1.yaxis.grid()
    ax1.set_xlabel('Logitudinal (m)')
    #######################
    df.plot.scatter( x='E', y='N' , marker='^', s=100,
            alpha=0.5 , ax=ax2 )
    df.plot.line( x='E', y='N' , color='red' , legend=None,
            alpha=0.5 , ax=ax2 )
    for i,row in df.iterrows():
        ax2.text( row['E'], row['Npred'], row['Name'], color='red' )
    span = df.U.iloc[-1]
    xlim = ax2.get_xlim()
    xlim_ = (xlim[0]+xlim[1])/2.
    ax2.set_xlim( xlim_-span/2. , xlim_+span/2. )
    ax2.ticklabel_format(useOffset=False, style='plain')
    ax2.set_aspect( 'equal' )
    ax2.grid( True )
    plt.xticks( rotation=90 )
    plt.suptitle( TITLE )
    plt.savefig( TITLE )
    return

#############################################################
class CatenaryModel:
    def __init__( self, FILE ):
        self.df_obs = pd.read_csv( FILE )
        print( self.df_obs )
        self.Mapping2Catenary()

    def Mapping2Catenary( self ):
        df = self.df_obs
        model = np.polyfit( df['E'], df['N'], 1 )
        self.predict = np.poly1d( model )
        df['Npred'] = self.predict( df['E'] )
        R_SQUARE = r2_score( df['N'], self.predict( df['E'] ))
        print( f'R-squared : {R_SQUARE:.2f}' )
        for i in df.index:
            if i==0:
                df['U'] = 0.0
            elif i>0:
                df.at[i,'U'] = np.hypot( df.E[i]-df.E[0],
                                         df.Npred[i]-df.Npred[0] )
        df['V'] = df['H']-df['H'].iloc[0]
        #import pdb; pdb.set_trace()
        return df

    def Solve( self, NUM_OUT=40 ):
        df_obs = self.df_obs
        cate  = GeneralCatenary( HOR_DIS=df_obs.U.iloc[-1],
                                 HEI_DIF=df_obs.V.iloc[-1] )
        result = cate.SolveEquation( df_obs['U'], df_obs['V'],
                 APPROX_C=1600, APPROX_U0=-200, APPROX_V0=+1700 )

        df_model = cate.Resampling( NUM=NUM_OUT )
        df_model['E'] = np.linspace( df_obs['E'].iloc[0],
                df_obs['E'].iloc[-1],  num=NUM_OUT, endpoint=True )
        df_model['N'] = self.predict( df_model['E'] )
        df_model['H'] = df_model['V'] + df_obs['H'].iloc[0]

        df_model = gpd.GeoDataFrame( df_model, crs='EPSG:32647',
                geometry=gpd.points_from_xy(
                    df_model.E, df_model.N, df_model.H ))
        #import pdb; pdb.set_trace()
        return df_obs, df_model, result

#############################################################
if __name__ == "__main__":
    PC_FILE = Path('LiAir250.csv')
    if len(sys.argv)==2:
        PC_FILE = Path( sys.argv[1] )

    cate_model = CatenaryModel( PC_FILE )
    df, df_model,result = cate_model.Solve( NUM_OUT=100)

    print( result['fit_report'] )
    del result['fit_report']
    print( result )
    ###############################
    stem = PC_FILE.stem

    PLT_FILE=PC_FILE.parents[0].joinpath( stem+'.png' )
    PlotTransmissionMap( df, df_model, PLT_FILE )

    GPKG_FILE=PC_FILE.parents[0].joinpath( stem+'.gpkg' )
    df_model['Sample']=df_model.index+1
    df_model[['Sample','geometry']].to_file(
            GPKG_FILE, layer='Cable', driver='GPKG', mode='w' )

    print('------------ end of Catenary --------------')
    #import pdb; pdb.set_trace()
