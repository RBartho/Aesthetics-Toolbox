import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



def drop_low_correlations(df, threshold):
    
    np.fill_diagonal(df.values, 0)
    
    drop_list = []
    
    for k, row in df.iterrows():
        drop_row = True
        for entry in row:
            #print(entry)
            if np.abs(entry) > threshold:
                drop_row = False
        if drop_row:
            drop_list.append(k)
            
    df.drop(drop_list, inplace=True, axis=0)
    
    df.drop(drop_list, inplace=True, axis=1)
    
    return df
    
    
                
    

file = 'AVA_1000.csv'
#file = 'Branka_Clouds.csv'
#file = 'JA_QIPs.csv'

file_root = '/home/ralf/Documents/18_SIP_Machine/Correlation_measure/'

df = pd.read_csv(  file_root + file , sep=',')


# print(df)


if file != 'Branka_Clouds.csv':
    df = df[df['mean G channel'] != 'grayscale']


# print(df)


if file == 'Branka_Clouds.csv':
    df.drop( ['Image size (pixels)','img_file', 'Aspect ratio', 'Color entropy',
    'mean R channel', 'mean G channel', 'mean B channel (RGB)',
    'mean L channel', 'mean a channel', 'mean b channel (Lab)',
    'mean H channel', 'mean S channel', 'mean V channel', 'std R channel',
    'std G channel', 'std B channel', 'std L channel', 'std a channel',
    'std b channel (Lab)', 'std H channel', 'std S channel',
    'std V channel'] , inplace=True, axis=1)
else:
    df.drop('img_file' , inplace=True, axis=1)


# print(df.columns)


# print(df)

cmap = sns.color_palette("coolwarm", as_cmap=True)

threshold = 0.8

## Person
plt.figure(figsize=(24, 20), dpi=300)
sns.heatmap(df.corr(),vmin=-1, vmax=1, cmap =cmap)
df_cor = np.round(df.corr('pearson'), 2)
plt.title('Person correlation ALL QIPs  ' + file[:-4] )
plt.savefig(file_root + file[:-4] +  '_corr_pearson.jpg' , dpi=300)
df_cor.to_csv(file_root + file[:-4] +  '_corr_pearson.csv', sep=',')

## reduced
df_dropped = drop_low_correlations(df_cor, threshold=threshold)
plt.figure(figsize=(24, 20), dpi=300)
sns.heatmap(df_dropped,vmin=-1, vmax=1, cmap =cmap)
plt.title('Pearson correlation QIPs with correlation > ' + str(threshold) + '  ' + file[:-4] )
plt.savefig(file_root + file[:-4] +  '_corr_pearson_high_correaltion.jpg' , dpi=300)
df_dropped.to_csv(file_root + file[:-4] +  '_corr_pearson_high_correaltion.csv', sep=',')


## Spearman
plt.figure(figsize=(24, 20), dpi=300)
sns.heatmap(df.corr(),vmin=-1, vmax=1, cmap =cmap)
df_cor = np.round(df.corr(method='spearman'), 2)
plt.title('Spearman correlation ALL QIPs  ' + file[:-4] )
plt.savefig(file_root + file[:-4] +  '_corr_spearman.jpg' , dpi=300)
df_cor.to_csv(file_root + file[:-4] +  '_corr_spearman.csv', sep=',')


## reduced
df_dropped = drop_low_correlations(df_cor, threshold=threshold)
plt.figure(figsize=(24, 20), dpi=300)
sns.heatmap(df_dropped,vmin=-1, vmax=1, cmap =cmap)
plt.title('Spearman correlation QIPs with correlation > ' + str(threshold) + '  ' + file[:-4] )
plt.savefig(file_root + file[:-4] +  '_corr_spearman_high_correaltion.jpg' , dpi=300)
df_dropped.to_csv(file_root + file[:-4] +  '_corr_spearman_high_correlation.csv', sep=',')





