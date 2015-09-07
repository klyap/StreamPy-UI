import json
from pprint import pprint
import os
import webbrowser
from Stream import Stream
from Stream import _no_value, _multivalue
from Agent import Agent

from example import *
from MakeNetwork import *
import components_test
from components_test import *

### UNCOMMENT FOR PARALLELLLL and get bakc MakeParallelNet2
#from MakeParallelNetwork import *


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


def make_seq(agent_descriptor_dict, stream_names_tuple):
    print('---------agent_descriptor_dict-------')
    pprint(agent_descriptor_dict)
    
    # MAKE THE NETWORK
    stream_dict, agent_dict, t_dict = make_network(
        stream_names_tuple, agent_descriptor_dict)
        
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
            
            # Print messages in transit to the input port
            # of each agent.
            for agent_name, agent in agent_dict.iteritems():
                descriptor = agent_descriptor_dict[agent_name]
                input_stream_list = descriptor[0]
                for stream_name in input_stream_list:
                    
                    # Create list of all streams at each time step
                    if streams_list_done == False:
                        streams_list.append(stream_name)
                    
                    # Get the correct stream object
                    stream = stream_dict[stream_name]
                    
                    value = str(stream.recent[stream.start[agent]:stream.stop])
                
                    val_str = val_str + '\'' + value[1:-1] + '\' ,'
                    
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
    
    return stream_str + '\n' +  selector_str + '\n' + val_str



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
    
    # TODO: Rename to renamed cytoscape html folder
    url = os.path.abspath("try_cytoscape/main.html")
    print 'got url: ' + url
    webbrowser.open(url,new=new)
    print 'opened'


   
    
    
    
    
    
    
    
    
    
    
    
    