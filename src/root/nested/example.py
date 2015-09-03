'''
Created on Jul 21, 2015

@author: klyap
'''
import json
from pprint import pprint
from graph_to_program1 import *
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

## Replace id with 0, 1, 2...
def new_name(comp_list, i, id):
    name = i
    if name not in comp_list.keys():
        return name
    elif comp_list[i].index(id) > 0:
        
        name = i + str(comp_list[i].index(id))
        return name
    return name

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


## (Not used anymore in favor of automatic execution/animation)
def ex(json_file_name):
    ## Open new file to write to
    output_file_name = 'pstreams_output.py'
    f = open(output_file_name, 'w')
    
    ## Import json file
    with open(json_file_name) as data_file:    
        data = json.load(data_file)

    ## Get list of unique components
    comps = make_comps(data)

    
    ## x is the length of the file name (aka the part we need to cut off)
    #x = len(comps.keys()[0].encode('ascii','ignore').split('/')[0]) + 1

    setup_template_file = open('setup_template_simple.txt', 'r')
    setup_template = [line.rstrip('\n') for line in setup_template_file] # convert file to array of lines
    
    ## Write setup imports, etc to file
    for line in setup_template:
            f.write(line + '\n')
            
    ## Create a Python function for each module and write it to file
    ## This is not used if we are importing functions that we already have
    
    #for c in comps:
    #    func_name = c.encode('ascii','ignore')[x:]
    #    
    #    in_streams = ''
    #    for ip in comps[c]['in']:
    #        in_streams = ip.encode('ascii','ignore') + ', ' + in_streams
    #    in_streams = in_streams[:-2]
    #    
    #    out_streams = ''
    #    for op in comps[c]['out']:
    #        out_streams = op.encode('ascii','ignore') + ', ' + out_streams
    #    out_streams = out_streams[:-2]
    #    
        
    #    for line in func_template:
    #        if len(in_streams) == 0:
    #            line = line.replace("IN_STREAM, OUT_STREAM", 'OUT_STREAM')
    #        if len(out_streams) == 0:
    #            line = line.replace("IN_STREAM, OUT_STREAM", 'IN_STREAM')
    #        line = line.replace("MODULE_NAME", func_name)
    #        line = line.replace("IN_STREAM", in_streams).replace("OUT_STREAM", out_streams)
    #        line = line.replace("NUM_OUT", str(len(comps[c]['out'])))
    #        f.write(line + '\n')
            
    ## For the "new_stream = func(input_stream, output_stream) set up
    ## Not used in the "output_stream = func(input_stream)" set up
    ## Create a PStreams Stream object from the names of each stream/edge in the graph
    #for op in out_ports:
    #    instance = op["process"].encode('ascii','ignore')[x:]
    #    port = op["port"].encode('ascii','ignore')
    #    stream_name = instance + '_' + port
    #    f.write( stream_name + ' = Stream(\''+ stream_name + '\')\n')
    
    ## Create a PStreams Stream object from outputs of modules with no input (source module)
    #for c in comps:
    #    if len(comps[c]['in']) == 0:
    #        for op in out_ports:
    #            if op['process'].encode('ascii','ignore')[:-6] == c:
    #                instance = op["process"].encode('ascii','ignore')[x:]
    #                port = op["port"].encode('ascii','ignore')
    #                stream_name = instance + '_' + port
    #                f.write( stream_name + ' = Stream(\''+ stream_name + '\')\n')
    
    ## Call modules with names of their input and output ports
    #for c in comps:
    #    func_name = c.encode('ascii','ignore')[x:]
    #    in_streams = ''
    #    for ip in comps[c]['in']:
    #        in_streams = '\'' + ip.encode('ascii','ignore') + '\', ' + in_streams
    #    
    #    out_streams = ''
    #    for op in comps[c]['out']:
    #        out_streams = '\'' + op.encode('ascii','ignore') + '\', ' + out_streams
    #
        #f.write(func_name + '_in_stream([' + in_streams + '],[' + out_streams + '])\n')
    #    f.write(func_name + '([' + in_streams[:-2] + '],[' + out_streams[:-2] + '])\n')
        
    ## Make connections by calling modules with input and output streams
    instances = data["processes"].keys()
    #pprint(instances)
    
    #for i in instances:
    #    func_name = i.encode('ascii','ignore')[x:-6]
    #    in_streams = ''
    #    out_streams = ''
    #    for conn in data['connections']:
    #        sp = conn['src']['process'].encode('ascii','ignore')
    #        if sp == i:
    #            out_streams = sp[x:] + '_' + conn['src']['port'].encode('ascii','ignore')+ ', ' +  out_streams 
    #            
    #        tp = conn['tgt']['process'].encode('ascii','ignore')
    #        if tp == i:
    #            in_streams = tp[x:] + '_' + conn['tgt']['port'].encode('ascii','ignore')+ ', ' +  in_streams
                
                
    #    f.write(func_name + '_in_stream([' + in_streams[:-2] + '],[' + out_streams[:-2] + '])\n')
    

    ## Create dict of each module instance with it's in and out streams

    
    ## Write instance dict contents to file as a function call
    #for i in instance_dict:
    #    in_streams = ''
    #    out_streams = ''
    #    for each in instance_dict[i]['in']:
    #        in_streams = each[x:] + ', ' + in_streams
    #    for each in instance_dict[i]['out']:
    #        out_streams = each[x:] + ', ' + out_streams
    #    
    #    f.write(i[x:-6] + '_in_stream([' + in_streams[:-2] + '],[' + out_streams[:-2] + '])\n')
        
    
    instance_dict = make_instance_dict(data, instances)
    #pprint(instance_dict)
    instance_dict_copy, output_str = function_calls(instance_dict)
    f.write(output_str)
    
    #execfile(output_file_name)
    
    return output_file_name

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

