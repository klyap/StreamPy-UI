import json
from pprint import pprint
from graph_to_program1 import *
from example import *
from MakeNetwork import *
#from MakeNetworkParallel import *
import MakeParallelNetworkParallel
#import components_test


import webbrowser
import os
#from root.nested.instances import instance_dict

## From MakeNetwork
from Stream import Stream
from Stream import _no_value, _multivalue
from Agent import Agent
#from OperatorsTest import stream_agent
from OperatorsTestParallel import stream_agent


import components_test
from components_test import *
import re
from array import array
from copy import deepcopy

## From MakeParallelNetwork
from multiprocessing import Process, Queue
import MakeParallelNetwork
### UNCOMMENT FOR PARALLELLLL and get bakc MakeParallelNet2
#from MakeParallelNetwork import *

# Checks initial input file for whether it has groups, etc.
# and sends file to appropriate process



def make_my_JSON(instance_dict, comp_list, json_data):

    stream_names_tuple = make_stream_names_tuple(instance_dict, comp_list)
    agent_descriptor_dict = make_agent_descriptor_dict(instance_dict, comp_list)    
    
    if json_data['groups']: # for graphs with groups
        groups = {}
        for group in json_data['groups']:
            
            group_name = group['name']
            nodes = []
            for node in group['nodes']:
                # Rename node
                label, id = clean_id(node.split('/')[1])

                if comp_list[label].index(id) == 0:
                    new_id = ''
                else:
                    new_id = str(comp_list[label].index(id))
                
                new_name = label + new_id
                nodes.append(new_name)
            # Add group data to the dict 'groups'
            groups[group_name] = nodes
            
        groups = str(groups)
        groups = groups.replace('\'', '\"').replace('u\"', '\"')
        pprint(groups)
    else:
        groups = None



    #in_ports, out_ports = get_exported_ports(json_data) # for graphs with subgraphs
    inports = 'inports'
    outports = 'outports'
    # if there are exposed inports
    def get_exposed_ports(in_ports):
        str_name = str(in_ports)
        if len(json_data[str_name].keys()) > 0:
            ports = json_data[str_name]
            ## Start renaming
            # Make new dict
            output = {}
            # Rename node
            for s in ports:
                node = ports[s]['process']
                label, id = clean_id(node.split('/')[1])
                #pprint(comp_list)
                #pprint(label)
                #pprint(id)
                if comp_list[label].index(id) == 0:
                    new_id = ''
                else:
                    new_id = str(comp_list[label].index(id))
                
                new_sname = label + new_id + '_PORT_' + ports[s]['port']
                
                # Save cleaned name to dict
                output[s] = new_sname
            
            in_ports = str(output)
            #pprint(in_ports)
            in_ports = in_ports.replace('\'', '\"').replace('u\"', '\"')
            #print '----cleaned exposed ports-----'
            #pprint(in_ports)
        else:
            in_ports = '{}'
        return in_ports
    
    inports = get_exposed_ports(inports)
    outports = get_exposed_ports(outports)
    
    output_file_name = 'agent_descriptor.json'
    f = open(output_file_name, 'w')
    f.write('{\n')
    
    f.write('\"agent_descriptor_dict\":\n')
    f.write(agent_descriptor_dict)
    f.write(',\n')
    
    f.write('\"stream_names_tuple\":\n')
    f.write(stream_names_tuple)

    
    if groups:
        f.write(',\n')
        f.write('\"groups\":\n')
        f.write(groups)
    
    if inports:
        f.write(',\n')
        f.write('\"inports\":\n')
        f.write(inports)
    
    if outports:
        f.write(',\n')
        f.write('\"outports\":\n')
        f.write(outports)

    
    f.write('\n}')
    f.close()
    
    
    return output_file_name

# Returns the 2 strings whose values are the edge and node arrays for the JS
# file
def make_graph(agent_descriptor_dict, stream_names_tuple):
    nodes = 'nodes: [\n'
    edges = 'edges: [\n'
    
    # Construct nodes string
    for name in agent_descriptor_dict.keys():
        node_line = '\t{ data: { id: \''+ name + '\', name:\'' + name +\
                        ' ''\'} },\n'
        nodes = nodes + node_line
    
    # Construct edges string
    for process in agent_descriptor_dict:
        for output_stream in agent_descriptor_dict[process][1]: 
            # each output stream is unique because streams are named after
            # the module instance and port name
            stream_name = output_stream
            # the source of this stream is this process
            output_process = output_stream.split('_PORT_')[0]
            
            for input_process in agent_descriptor_dict.keys():
                # if a process takes this stream as an input...
                # then we have found this stream's target
                if output_stream in agent_descriptor_dict[input_process][0]:
                    src_name = output_process
                    tgt_name = input_process
                    edge_line = '\t{ data: { stream: \'' + stream_name + '\', source: \'' + src_name + '\', target: \'' +\
                                tgt_name +'\', name:\'' + stream_name + ':' + '\'} },\n'
                    edges = edges + edge_line
            
    nodes = nodes[:-2] + ']'
    edges = edges[:-2] + ']'
    return nodes, edges
'''
# Returns the 2 strings whose values are the edge and node arrays for the JS
# file
def make_graph(agent_descriptor_dict, stream_names_tuple):
    nodes = 'nodes: [\n'
    edges = 'edges: [\n'
    
    # Construct nodes string
    for name in agent_descriptor_dict.keys():
        node_line = '\t{ data: { id: \''+ name + '\', name:\'' + name +\
                        ' ''\'} },\n'
        nodes = nodes + node_line
    
    print('--------stream names tuple-------------')
    pprint(stream_names_tuple)
    # Construct edges string
    for s in stream_names_tuple:
        # src_name is the name of the component that the stream s is from
        src_name = s.split('_PORT_')[0]
        # tgt_name is found from the list of input streams of the components
        tgt_name = str()
        for i in agent_descriptor_dict.keys():
            if s in agent_descriptor_dict[i][0]:
                tgt_name = i
                break
            
        edge_line = '\t{ data: { stream: \'' + s + '\', source: \'' + src_name + '\', target: \'' +\
                    tgt_name +'\', name:\'' + s + ':' + '\'} },\n'
        edges = edges + edge_line
        
            
    nodes = nodes[:-2] + ']'
    edges = edges[:-2] + ']'
    return nodes, edges
'''

def make_seq(agent_descriptor_dict, stream_names_tuple):
    print('---------agent_descriptor_dict-------')
    pprint(agent_descriptor_dict)
    
    # STEP 3: MAKE THE NETWORK
    stream_dict, agent_dict, t_dict = make_network(
        stream_names_tuple, agent_descriptor_dict)
    
    #print('------agent_dict_-------')
    #pprint(agent_dict)
    '''    
    # Only for debugging
    ## for key, value in s_dict.items():
    ##     print 'stream name', key
    ##     print 'stream', value

    ## for key, value in a_dict.items():
    ##     print 'agent name', key
    ##     print 'agent', value

    ## for key, value in t_dict.items():
    ##     print 'timer name is', key
    ##     print 'timer', value

    # STEP 4: DRIVE THE NETWORK BY APPENDING
    #      VALUES TO TIMER STREAMS
    
    ## AND ALSO MAKE STRINGS TO BE WRITTEN TO OUTPUT FILE
    '''   
    
    # val_str is a list of values of each time step,
    # concatnated in one long, comma separated string
    val_str = str()
    
    # list of the streams in order
    streams_list = []
    streams_list_done = False
    
    # Time_step tells you how many times it should fire all components at
    # (roughly how many values you want to go through)
    time_step = 1
    for t in range(time_step):
        print '--------- time step: ', t
        # Append t to each of the timer streams
        for stream in t_dict.values():
            print '-------', stream.name
            stream.append(t)
            ## for stream in stream_dict.values():
            ##     stream.print_recent()

            # Print messages in transit to the input port
            # of each agent.
            for agent_name, agent in agent_dict.iteritems():
                descriptor = agent_descriptor_dict[agent_name]
                input_stream_list = descriptor[0]
                for stream_name in input_stream_list:
                    #print '--------input_stream_list: ', input_stream_list
                    # Create list of all streams at each time step
                    if streams_list_done == False:
                        streams_list.append(stream_name)
                    
                    # Get the correct stream object
                    stream = stream_dict[stream_name]
                    
                    # value is a string of this form:
                    # [4]
                    value = str(stream.recent[stream.start[agent]:stream.stop])
                    #print '----value------'
                    #print value[1:-1]
                    val_str = val_str + '\'' + value[1:-1] + '\' ,'
                    #val_str = val_str + index_and_value.split(' = ')[1] + ','
                    
                    print "messages in ", stream_name, "to", agent.name
                    print stream.recent[stream.start[agent]:stream.stop]
            streams_list_done = True

    val_str = 'var value = [' + val_str[:-1] + '];'
    
    # stream_str is a list of all streams, 
    # selector_str is the list of streams, but formatted 
    # to be used as selectors in JS
    stream_str = str()
    selector_str = str()
    for s in streams_list:
        selector_str = selector_str + '\'edge[stream= "' + s + '"]\', '
        stream_str = stream_str + '\'' + s + '\', '
    selector_str = 'var edge = [' + selector_str[:-1] + '];'
    stream_str = 'var stream_names = [' + stream_str[:-1] + '];'
    
    
    #pprint(stream_str + '\n' +  selector_str + '\n' + val_str)
    return stream_str + '\n' +  selector_str + '\n' + val_str
## t_dict['generate_random'].append(0)
## s_dict['random_stream'].print_recent()
## s_dict['multiples_stream'].print_recent()
## s_dict['non_multiples_stream'].print_recent()

## t_dict['split'].append(1)


# MAKE_JSON
# Using a JSON file of my format, generate Javascript text
# the fills in a template .js file with:
# graph configuration (draws the graph)
# & animation sequence (animates graph)
def make_js(json_file):
    ## Make agent_descriptor_dict, stream_names_tuple
    agent_descriptor_dict, stream_names_tuple = JSON_to_descriptor_dict_and_stream_names(json_file)
    nodes, edges = make_graph(agent_descriptor_dict, stream_names_tuple)
    seq = make_seq(agent_descriptor_dict, stream_names_tuple)
    
    # Write my graph and seq to a JS file
    write_to_js(nodes, edges, seq)

# Writes new things to JS file and opens browser to show animation
def write_to_js(nodes, edges, seq):
    ## Open new file to write to
    output_file_name = 'try_cytoscape/animate_graph.js'
    f = open(output_file_name, 'w')
    # Open template file to copy from and fill out
    template_file_name = 'try_cytoscape/animate_code.js'
    t = open(template_file_name, 'r')

    for line in t:
        line = line.replace('ELEMENTS', nodes + ',\n' + edges)
        line = line.replace('SEQUENCE', seq)
        f.write(line)

    new = 2
    # Hardcoded local file path (currently for Windows)
    # TODO: Rename to renamed cytoscape html folder
    url = os.path.abspath("try_cytoscape/main.html")
    webbrowser.open(url,new=new)


   
    
    
    
    
    
    
    
    
    
    
    
    