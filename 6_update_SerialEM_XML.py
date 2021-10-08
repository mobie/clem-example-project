#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 12:12:38 2021

@author: schorb
"""

import os
import mobie
from pybdv import transformations as tf


import xml.etree.ElementTree as ET

import numpy as np

dataset = "./data/hela"

meta = mobie.metadata.read_dataset_metadata(dataset)

os.chdir(dataset)

sourcetrafos = dict()

for (sourcename,source) in meta['sources'].items():
    for xmlfile in [source['image']['imageData']['bdv.n5']['relativePath'],
                    source['image']['imageData']['bdv.n5.s3']['relativePath']]:
        
        tree = ET.parse(xmlfile)
        root = tree.getroot()
        
        sd = root.find('SequenceDescription')
        
        vs = sd.find('ViewSetups')
        vs_attr = vs.find('ViewSetup')        
        vxs = vs_attr.find('voxelSize')
        voxs = vxs.find('size')
        
        voxel_sz = np.array(list(map(float,voxs.text.split(' '))))
        m_vox = np.diag(voxel_sz)
        
        vr = root.find('ViewRegistrations')
        vr_attr = vr.find('ViewRegistration')
        
        trafos = [None]*len(vr_attr)
        trafo_names = []
        
        for ix,vt in enumerate(vr_attr):
                
            aff = vt.find('affine')
            t_name = vt.find('name').text
                        
            trafo1 = aff.text
            t = np.array(list(map(float,trafo1.split(' ')))).reshape([3,4])
            
            trafos[-ix-1] = t
            trafo_names.append(t_name)
           
        
        # update transformation to be written into XML
        
        trafos[0][:3,:3] = trafos[0][:3,:3] @ np.linalg.inv(m_vox)
        
        voxs_mat = np.concatenate((m_vox,[[0],[0],[0]]),axis=1)
        voxs_mat = np.concatenate((voxs_mat,[[0,0,0,1]]))
        voxs_mat1 = tf.matrix_to_transformation(voxs_mat).tolist()
        
        vr_attr.clear()
        vt = ET.SubElement(vr, 'ViewTransform')
        ET.SubElement(vt,'name').text = 'Scaling'
        ET.SubElement(vt, 'affine').text = ' '.join(map(str,voxs_mat1))
   
    # write the xml
        tf.indent_xml(root)
        tree = ET.ElementTree(root)
        tree.write(xmlfile+'new')
        
        sourcetrafos[sourcename]={'names':trafo_names, 'trafos':trafos}
        
        
        # now deal with the views:
            
    for viewname, orig_view in meta['views'].items():
        
        for v_transform in orig_view['sourceTransforms']:
            if 'affine' in v_transform.keys():
                v_sources = v_transform['affine']['sources']
                
                for v_source in v_sources:
                
                    if v_source in sourcetrafos.keys():
                        for ix,t_name in enumerate(sourcetrafos[v_source]['names']):
                            print(t_name)
        
        
