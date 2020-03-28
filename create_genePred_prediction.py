# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 18:48:47 2020

@author: Aashutosh Maheshwari
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 15:01:19 2020

@author: Aashutosh Maheshwari
"""

import numpy as np
import pandas as pd
df = pd.read_excel('genePred1.xlsx')

data = df.to_numpy()

genePred = ['name','chrom','strand','txStart','txEnd','cdsStart','cdsEnd','exonCount','exonStarts','exonEnds','score','name2','cdsStartStat','cdsEndStat','exonFrames']
genePred_size = np.shape(genePred)
for i in range(np.shape(data)[0]):
    exon_count = 0
    exon_start = []
    exon_end = []
    exon_Frames = []
    CDS_s = []
    CDS_e = []
    temp = np.zeros(genePred_size).astype(np.str)
    if data[i,2] == 'gene':
        temp[0] = data[i,np.shape(data)[1]-1] #name = transcript_id
        temp[11]= temp[0]   #name2
        temp[1] = data[i,0] #chromosome/scaffold
        temp[2] = data[i,6] #strand
        temp[3] = data[i,3] #txstart
        temp[4] = data[i,4] #txend
        
        
        #cds
        for l in range(i+1,np.shape(data)[0]): #25 can be replaced by #np.shape(data)[0]
            if data[l,2] == 'gene':
                break
            elif data[l,2] == 'CDS':
                CDS_s.append(data[l,3])
                CDS_e.append(data[l,4])
                exon_Frames.append(data[l,7])
        temp[5] = np.amin(CDS_s)
        temp[6] = np.amax(CDS_e)
        temp[14] = str(exon_Frames[::-1])[1:-1]
        #exon
        for k in range(i+1,np.shape(data)[0]):
            if data[k,2] == 'gene':
                break
            elif data[k,2] == 'exon':
                exon_count = exon_count + 1
                exon_start.append(data[k,3])
                exon_end.append(data[k,4])
                #exon_Frames.append()
        temp[7] = exon_count
        temp[8] = str(exon_start)[1:-1] 
        temp[9] = str(exon_end)[1:-1] 
        
        #cds Start and End Stat [Read more] 
        temp[12]= 'cmpl'
        temp[13]= 'cmpl'
        
        genePred = np.vstack((genePred,temp))
    
final_df = pd.DataFrame(genePred)
with pd.ExcelWriter('genePred_CHOPCHOP.xlsx',
                        engine='xlsxwriter',
                        options={'strings_to_numbers': True}) as writer:
    final_df.to_excel(writer)