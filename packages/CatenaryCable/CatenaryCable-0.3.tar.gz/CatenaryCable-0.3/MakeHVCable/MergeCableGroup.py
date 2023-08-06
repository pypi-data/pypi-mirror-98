#
#
#
#
#
import glob
import pandas as pd
import geopandas as gpd

def ReadMerge( grp ):
    df_sample = gpd.GeoDataFrame()
    for i,row in grp.iterrows():
        df = gpd.read_file( row.FileName )
        df_sample = df_sample.append( df )
    return df_sample

CATE_DIR='./CACHE'

print(f'Reading Catenary Directory : {CATE_DIR}')
files = glob.glob( f'{CATE_DIR}/*.gpkg' )
print( files )

df = pd.DataFrame( files,  columns=['FileName'] )
df['Cable'] = df['FileName'].str[:15]

for i,grp in df.groupby('Cable'):
    grp = grp.sort_values(['FileName'])
    print( i,grp )
    df = ReadMerge( grp )
    df.to_file( f'{i}.gpkg' , layer='cable', driver='GPKG' )
import pdb;pdb.set_trace()

