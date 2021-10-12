#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 12:12:38 2021

@author: schorb
"""

import os
import mobie
from pybdv import transformations as tf
import copy

import xml.etree.ElementTree as ET

import numpy as np

dataset = "./data/hela"

meta = mobie.metadata.read_dataset_metadata(dataset)

os.chdir(dataset)


#%%

sourcetrafos = dict()

for (sourcename,source) in meta['sources'].items():
    for xmlfile in [source['image']['imageData']['bdv.n5']['relativePath'],
                    source['image']['imageData']['bdv.n5.s3']['relativePath']]:
        
        origfile = os.path.splitext(xmlfile)[0]+'_orig.xml'
                    
        
        tree = ET.parse(xmlfile)
        
        if not os.path.exists(origfile):
            tree.write(origfile)
        else:
            tree = ET.parse(origfile)
            
        root = tree.getroot()
        
        sd = root.find('SequenceDescription')
        
        vs = sd.find('ViewSetups')
        vs_attr = vs.find('ViewSetup')        
        vxs = vs_attr.find('voxelSize')
        voxs = vxs.find('size')
        
        voxel_sz = np.array(list(map(float,voxs.text.split(' '))))
        m_vox = np.diag(voxel_sz)
        
        vr = root.find('ViewRegistrations')
        vr_el = vr.find('ViewRegistration')
        
        vr_attr = vr_el.attrib
        
        trafos = [None]*len(vr_el)
        trafo_names = []
        
        for ix,vt in enumerate(vr_el):
                
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
        
        vr_el.clear()
        
        vr_el.attrib = vr_attr
        
        vt = ET.SubElement(vr_el, 'ViewTransform')
        ET.SubElement(vt,'name').text = 'Scaling'
        ET.SubElement(vt, 'affine').text = ' '.join(map(str,voxs_mat1))
   
    # write the xml
        tf.indent_xml(root)
        tree = ET.ElementTree(root)
        tree.write(xmlfile)
        
        sourcetrafos[sourcename]={'names':trafo_names, 'trafos':trafos}
        
        
        # now deal with the views:
            
for viewname, orig_view in meta['views'].items():
    
    outview = copy.deepcopy(orig_view)
    v_sources = []
    break
    for v_transform in orig_view['sourceTransforms']:
        if 'affine' in v_transform.keys():
            v_sources.append(v_transform['affine']['sources'])
        elif 'crop' in v_transform.keys():
            v_sources.append(v_transform['crop']['sources'])
 
    for xml_source in sourcetrafos.keys():
       if [xml_source] in v_sources:   
           
           for t_idx,xml_trafo in enumerate(sourcetrafos[xml_source]['trafos']):
               
               t_view = mobie.metadata.get_affine_source_transform([xml_source],
                                                                   tf.matrix_to_transformation(np.concatenate((xml_trafo,[[0,0,0,1]]))).tolist(),
                                                                   name = sourcetrafos[xml_source]['names'][t_idx])
               
               outview['sourceTransforms'].insert(v_sources.index([xml_source]),t_view)
               
    mobie.metadata.add_view_to_dataset(dataset, viewname, outview)
           
                        
                        
                            
                            
        
        
