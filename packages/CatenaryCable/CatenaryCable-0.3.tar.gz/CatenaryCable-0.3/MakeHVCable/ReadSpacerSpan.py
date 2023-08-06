#
#
#
#
#   Phisan.Chula@gmail.com
#
#
import math,sys,os
import pandas as pd
import geopandas as gpd
import fiona
from pathlib import Path
from shapely.geometry import Point, LineString
import matplotlib.pyplot as plt

gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'


#############################################################
def convert_wgs_to_utm(lon, lat):
    utm_band = str((math.floor((lon + 180) / 6 ) % 60) + 1)
    if len(utm_band) == 1:
        utm_band = '0'+utm_band
    if lat >= 0:
        epsg_code = 'epsg:326' + utm_band
    else:
        epsg_code = 'epsg:327' + utm_band
    return epsg_code

#############################################################
def GenTowerSpan( df_TW, df_SPC , X_BUFF ):
    df_span = gpd.GeoDataFrame(columns=['Name','length','geometry'])
    for i in range( len(df_TW)-1 ):
        tw0 = df_TW.iloc[i ]
        tw1 = df_TW.iloc[i+1]
        name = '{}-{}'.format( tw0.Name, tw1.Name ) 
        line = LineString( [tw0.geometry, tw1.geometry] )
        df_span = df_span.append( { 'Name': name ,'length': line.length,
                          'geometry':line } , ignore_index=True )
    df_span = df_span.set_crs( df_TW.crs )
    #import pdb; pdb.set_trace()
    buf = df_span.buffer( X_BUFF )
    df_Buf = gpd.GeoDataFrame({'Name':df_span.Name}, crs= df_TW.crs,
                              geometry= buf  )
    df_SpacSpan = gpd.sjoin( df_SPC, df_Buf, how='inner', op='intersects',
                          lsuffix='Spacer', rsuffix='Span' )
    return df_Buf, df_SpacSpan

##############################################################
def ReadTowerSpaceFile( TowerFile, SpacerFile):
    df_tw = gpd.read_file( TowerFile, driver='KML')
    df_sp = gpd.read_file( SpacerFile, driver='KML')

    lng_m, lat_m, _ = df_tw.iloc[ len(df_tw)//2 ].geometry.coords[0]
    UTM_PROJ = convert_wgs_to_utm(lng_m, lat_m)
    df_tw = df_tw.to_crs( UTM_PROJ )
    df_sp = df_sp.to_crs( UTM_PROJ )
    return UTM_PROJ, df_tw, df_sp

#####################################################################
def PREPARE_CACHEDIR( CACHEDIR = './CACHE' ):
    if not os.path.isdir(CACHEDIR):
        os.makedirs(CACHEDIR)
        print('created folder "{}" ... '.format( CACHEDIR) )
    else:
        print('folder "{}"already exists.'.format( CACHEDIR ))

#####################################################################
def WriteSpanCSV( df_SPAN ,CACHE_DIR, CABLE_NAME ):
    grp_span = df_SPAN.groupby('Name_Span')
    print( f'Total spans : {len(grp_span)}' )
    print( df_SPAN['Name_Span'].value_counts() )
    df_SPAN['E'] = df_SPAN.geometry.x
    df_SPAN['N'] = df_SPAN.geometry.y
    df_SPAN['H'] = df_SPAN.geometry.z
    cmds = list()
    #import pdb; pdb.set_trace()
    for i,grp in grp_span:
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        grp.index += 1
        #for col in ( 'E', 'N', 'H' ):
        #    grp[col]= grp[col].map('{:.3f}'.format )
        #print ( i, grp )
        FileCSV = '{}/{}_{}.csv'.format( CACHE_DIR,
                CABLE_NAME, grp.iloc[0].Name_Span )
        print(f'Writing CSV for each span : {FileCSV}...')
        grp.rename(columns={'Name_Spacer':'Name'}, inplace=True)
        grp[['Name_Span','Name','E','N','H']].to_csv( FileCSV,
                 index=True, index_label='Seq')
        os.system( f'python3 1_Make_CateLine.py {FileCSV}\n' )

#####################################################################
def CalcCoordUV( df ):
    df['V'] = df.geometry.z
    df['U'] = 0.0
    for i in range(len(df)):
        if i==0:
            df.at[i,'U'] = 0.0
        else:
            t0 = df.loc[0].geometry
            t1 = df.loc[i].geometry
            df.at[i,'U'] = t0.distance(t1) 
    return df 

#####################################################################
def Plot_Longitudinal(df_Tower, df_Spacer, PLOT_FILE):
    df_Tower  = CalcCoordUV( df_Tower )
    df_Spacer = CalcCoordUV( df_Spacer )
    #import pdb; pdb.set_trace()
    fig,ax = plt.subplots( 1, figsize=(20,10) )
    for i,row in df_Spacer.iterrows():
        ax.annotate( row.Name, xy=(row.U,row.V), fontsize=14, 
                     rotation=90, color='grey' )
    for i,row in df_Tower.iterrows():
        ax.annotate( row.Name, xy=(row.U,row.V), fontsize=24, color='red' )
        ax.axvline( row['U'] , color='red', linestyle='--'  )
    df_Tower.plot.scatter( x='U', y='V' , marker='1', s=500,
                           c='red',  alpha=0.5 ,  ax=ax )
    df_Spacer.plot.scatter( x='U', y='V' , marker='X', s=100,
                     alpha=0.5 ,  ax=ax )
    ax.grid()
    plt.suptitle( PLOT_FILE )
    plt.savefig( PLOT_FILE )
    #plt.show()
    return
#####################################################################
#####################################################################
#####################################################################
if __name__ == "__main__":
    CACHE = './CACHE' 
    PREPARE_CACHEDIR( CACHE )

    X_BUFF = 12   # m 2x of cross-arm
    TowerFile  = Path( 'Krabin_Demo/KBR_Trans_8.kml' )
    #SpacerFile = Path('Krabin_Demo/KBR_C_R.kml')
    SpacerFile = Path('Krabin_Demo/KBR_C_L.kml' )

    print(f'Reading Tower Data ...{TowerFile}')
    print(f'Reading Spacer Data ...{SpacerFile}')
    print(f'Cross-arm buffering ...{X_BUFF} meter')

    if len(sys.argv)==4:
        TowerFile  = Path( sys.argv[1] )
        SpacerFile = Path( sys.argv[2] )
        X_BUFF = float( sys.argv[3] )

    UTM_PROJ , df_tw, df_sp = ReadTowerSpaceFile( TowerFile, SpacerFile )
    
    PLOT_FILE = '{}/{}_{}.pdf'.format(CACHE, TowerFile.stem, SpacerFile.stem)  
    Plot_Longitudinal(df_tw, df_sp, PLOT_FILE)
    df_buf, df_SPAN = GenTowerSpan( df_tw, df_sp, X_BUFF )
    WriteSpanCSV( df_SPAN ,CACHE, SpacerFile.stem )
    #############################################################
    if 1:
        df_buf = df_buf.to_crs('epsg:4326')
        with fiona.Env():
            df_buf.to_file(f'CACHE/{TowerFile.stem}_df_buf.kml', driver='KML')
