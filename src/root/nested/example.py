'''
Functions that handle renaming

'''
import json
from pprint import pprint
import webbrowser
import os
#from root.nested.instances import instance_dict

def make_conn_dict(conn):
    conn_dict = {}
    for i in conn:
        if 'src' in i.keys():
            name = str(i['src']['process'])[x:]
            conn_dict[name] = []
        
    for i in conn:
        if 'src' in i.keys():
            #src_name, src_id = clean_id(str(i['src']['process']))
            #tgt_name, tgt_id = clean_id(str(i['tgt']['process']))
            src_name = str(i['src']['process'])[x:]
            tgt_name = str(i['tgt']['process'])[x:]
            port_name = str(i['src']['port'])
            conn_dict[src_name].append({'tgt': tgt_name , 'port': port_name})
     
    return conn_dict

## Dictionary of each component with it's input and output ports
## Ex. {process: {'in':[input_ports], 'out':[output_ports]}
def make_comps(data):
    # con_dict has the keys: src & tgt, vals: dict of process & port
    conn_list = data["connections"]
    
    ## Get list of unique output ports {port, process}
    out_ports = []
    for con_dict in conn_list:
        if 'src' in con_dict.keys() and con_dict['src'] not in out_ports:
            out_ports.append(con_dict['src'])

    
    ## Get list of unique input ports {port, process}
    in_ports = []
    for con_dict in conn_list:
        if con_dict['tgt'] not in in_ports:
            in_ports.append(con_dict['tgt'])

    
    ## Start constructing comps:
    ## {process: {'in':[input_ports], 'out':[output_ports]}
    comps = {}
    comp_list = data["processes"]
    for comp_dict in comp_list:
        if comp_list[comp_dict]['component'] not in comps:
            comps[comp_list[comp_dict]['component']] = {"in":[], "out":[]}

    ## Assign output and input ports to each component in comps
    for comp in comps:
        for op in out_ports:
            instance_name = op["process"].encode('ascii','ignore')    #name of module with ID
            name = comp.encode('ascii','ignore')                      #name of module
    
            if instance_name.find(name) == 0 and (op["port"] not in comps[comp]["out"]):
                comps[comp]["out"].append(op["port"])
                
        for ip in in_ports:
            instance_name = ip["process"].encode('ascii','ignore')    #name of module with ID
            name = comp.encode('ascii','ignore')                      #name of module

            if instance_name.find(name) == 0 and (ip["port"] not in comps[comp]["in"]):
                comps[comp]["in"].append(ip["port"])
    return comps


## Makes dict of each instance and its in and out ports
def make_instance_dict(data, instances):
    instance_dict= {}
    for i in instances:
        i = i.encode('ascii','ignore')
        instance_dict[i] = {'in':[], 'out':[]}
        
    
    for conn in data['connections']:
        if 'src' in conn.keys():
            sp = conn['src']['process'].encode('ascii','ignore')
            spp = conn['src']['port'].encode('ascii','ignore')
        else:
            # for constant parameters because they have no 'src'
            sp = 'none'
            spp = conn['tgt']['port'].encode('ascii','ignore') + '=' + conn['data']
        
        tp = conn['tgt']['process'].encode('ascii','ignore')
        tpp = conn['tgt']['port'].encode('ascii','ignore')
        
        if sp == 'none':
            instance_dict[tp]['in'].append(spp)
        else:
            if sp + '_' + spp not in instance_dict[sp]['out']:
                instance_dict[sp]['out'].append(sp +'_' + spp)
            '''
            if sp + '_'+ spp not in instance_dict[tp]['in']:
                instance_dict[tp]['in'].append(sp +'_'+spp)
            '''
            instance_dict[tp]['in'].append(sp +'_'+spp)
    return instance_dict


## Convert string to the correct object type (int, float, string)
def cast(s):
    try:
        int(s)
        return float(s)
    except ValueError:
        try:
            float(s)
            return int(s)
        except ValueError:
            return str(s)
        
# Helper function to delete 'browser...'
def delete_startswith_substring(s, substring):
    if s.startswith(substring):
        return s[len(substring):]
    else:
        return s
    
# Removes the random id at the end of the component name
# Returns the clean name of the component and the id
def clean_id(component):
    
    if '_' not in component:
        return component, ''
    
    l_array = component.split('_')
    l = len(l_array) - 1
    cid = l_array[l]
    label = str()
    for i in range(0, l ):
        label = label+ l_array[i] + '_'
    label = label[:-1]
    #label = component.replace(cid, '')[:-1]
    
    return label, cid

def rename_stream(original_arr, comp_list):
    renamed_arr = []
    for i in original_arr:
        #print('\n this is original arr: \n')
        #pprint(original_arr)
        #print('\n this is comp_list: \n')
        #pprint(comp_list)
        if '=' in i:
            renamed_arr.append(i)
        else:
            label_with_id, portname = clean_id(i.split('/')[1])
            #pprint(label_with_id)
            #pprint(portname)
            label, id = clean_id(label_with_id)
            #pprint(comp_list)
            #pprint(label)
            #pprint(id)
            if comp_list[label].index(id) == 0:
                new_id = ''
            else:
                new_id = '_' + str(comp_list[label].index(id))
            renamed_arr.\
            append(label + new_id + '_PORT_' + portname)
    return renamed_arr

# comp_list will be a dictionary of each
# module/function name and the id's
# associated with each
# The index of the id's will determine
# which number 1, 2, 3... it will be
# replaced by
def make_comp_list(instance_dict):
    comp_list = dict()
    for component, connections in instance_dict.items():
        # populating comp_list
        label, cid = clean_id(component)
        label = label.split('/')[1]
        if label in comp_list.keys():
            comp_list[label].append(cid)
        else:
            comp_list[label] = [cid]

    return comp_list


## Replace id with 0, 1, 2...
def new_name(comp_list, i, id):
    name = i
    if name not in comp_list.keys():
        return name
    elif comp_list[i].index(id) > 0:
        
        name = i + str(comp_list[i].index(id))
        return name
    return name



