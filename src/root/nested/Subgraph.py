__author__ = 'klyap_000'
import json
from pprint import pprint
from graph_to_program1 import *
from example import *
from MakeNetwork import *
#from MakeNetworkParallel import *
import MakeParallelNetworkParallel
#import components_test

from Animation import *

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

# Convert input JSON file to a JSON file of my format if needed
def make_json(json_file_name):
    ## Import json file
    with open(json_file_name) as data_file:
        json_data = json.load(data_file)

    ## Check if the input JSON is from Flowhub or already in my format
    if 'agent_descriptor_dict' not in json_data.keys():
        ## Make required data structs from Flowhub JSON

        # comps is dict of processes with the names of their
        # input and output ports as array values with keys 'inputs', 'outputs'
        comps = make_comps(json_data)
        #pprint(comps)

        # x is the length of the file name (aka the part we need to cut off)
        x = len(comps.keys()[0].encode('ascii','ignore').split('/')[0]) + 1
        #print x

        instances = json_data["processes"].keys()
        instance_dict = make_instance_dict(json_data, instances)
        #pprint(instance_dict)

        comp_list = make_comp_list(instance_dict, x)
        #pprint(comp_list)

        # Make a JSON file in the format I want from Flowhub's JSON
        my_json_file_name = make_my_JSON(instance_dict, comp_list, json_data, x)

        # DEBUG
        #with open(my_json_file_name) as data_file:
        #    json_data = json.load(data_file)
        #print 'in make_json: this is final json'
        #pprint(json_data)

    else:
        # The input JSON is already in the format I want
        my_json_file_name = json_file_name

    return my_json_file_name


## DEALING WITH SUBGRAPHS
'''
# Iterative version
def unwrap_subgraph(my_json_file_name):

    ## Go through all functions/modules in json file and make sure they're in
    ## components_test.py. Otherwise, there might be a subgraph.
    # Open new file to put the fully exposed graph JSON in
    # by copying over current json file

    iteration_count = 0
    with open(my_json_file_name) as json_file_original:
            j = json.load(json_file_original)

    print '---------J = current agent dic------'
    pprint(j)

    #### GET SUBGRAPH NAMES #####
    unfound_comps = []
    # Make array of functions in components_test.py
    # (also includes random elements like '__builtins__', '__doc__', '__file__'
    comps_funcs = dir(components_test)

    # Make array of functions in JSON
    JSON_funcs = []
    for i in j['agent_descriptor_dict'].keys():
        JSON_funcs.append(j['agent_descriptor_dict'][i][2])
    #print '---------funcs in JSON----------'
    #pprint(JSON_funcs)

    # If there are functions not in components_test.py...
    # collect them (they are prlly subgraphs)
    #unfound_comps = []
    for f in JSON_funcs:
        if (f not in comps_funcs) and (f not in unfound_comps):
            unfound_comps.append(f)

    while len(unfound_comps) > 0:
        print 'iteration: ', str(iteration_count)
        print 'unfound comps: ', unfound_comps
        new_dict = {}
        new_dict['agent_descriptor_dict'] = deepcopy(j['agent_descriptor_dict'])
        new_dict['stream_names_tuple'] = deepcopy(j['stream_names_tuple'])
        print '============== new_dict = j ================='
        pprint(new_dict)

        ##### EXPOSE SUBGRAPHS ########
        for unfound in unfound_comps:
            print 'unfound: ', unfound
            try:
                # Look for .json for corresponding subgraph
                #path = '/home/klyap/Downloads/'
                path = 'JSON/'
                new_json = unfound + '.json'

            except NameError:
                print 'No such function or subgraph JSON file: ' + f
                return 'No such function or subgraph JSON file: ' + f

            # Grab the exposed in and out ports from original JSON:
            with open(path + new_json) as new_json_file:
                subgraph_json = json.load(new_json_file)

            # Look for new JSON file for the subgraph
            new_json = make_json(path + new_json)

            with open(new_json) as new_json_file:
                subgraph_dict = json.load(new_json_file)

            unfound_entry = deepcopy(new_dict['agent_descriptor_dict'][unfound])
            print '------unfound entry------'
            pprint(unfound_entry)
            # Now that it's stored as unfound_entry, delete it from the dict
            del new_dict['agent_descriptor_dict'][unfound]

            # Add new unwrapped components
            for comp in subgraph_dict['agent_descriptor_dict'].keys():
                new_dict['agent_descriptor_dict'][comp] = subgraph_dict['agent_descriptor_dict'][comp]

            # Get exposed outports and inports of subgraph
            inports = subgraph_dict['inports']
            outports = subgraph_dict['outports']

            for comp in new_dict['agent_descriptor_dict']:
                new_inputs = []

                for s in new_dict['agent_descriptor_dict'][comp][0]:
                    # if exposed output streams come from a comp in
                    # this subgraph, add this to comp's input streams
                    renamed_stream = s
                    if unfound in s:
                        # Replace s with correctly named stream in exposed outports
                        # by matching the s.split('_PORT_')[1] with a key in dict
                        # and extracting the value as my new s
                        print 'loooking for:'
                        pprint(s.split('_PORT_')[1])
                        pprint(outports)
                        renamed_stream = outports[s.split('_PORT_')[1]]
                        #print 'renaming:'
                        #print renamed_stream
                    new_inputs.append(renamed_stream)

                new_dict['agent_descriptor_dict'][comp][0] = new_inputs
                #print '---------just added new inputs to ' + comp
                #pprint(new_dict['agent_descriptor_dict'][comp])

            # Now check components outside subgraphs for those
            # that connect to the inputs in our list
            # (These streams in new_inputs are currently named after
            # the in port. We want it to be the out port of the prev component)

            for i in range(len(inports.values())):
                # Get component name from inport stream (ie. compname_PORT_in)
                comp_name = inports.values()[i].split('_PORT_')[0]
                print 'at index: ' + str(i)
                print inports.values()[i]

                # Match it with a input stream of the same index
                new_dict['agent_descriptor_dict'][comp_name][0].\
                append(unfound_entry[0][i])


            # Now that the input streams inside each component are fixed
            # fix corresponding streams in inports of subgraph
            new_inports = {}
            for c in subgraph_dict['agent_descriptor_dict']:
                if len(subgraph_dict['agent_descriptor_dict'][c][0]) > 0:
                    for s in subgraph_dict['agent_descriptor_dict'][c][0]:
                        new_inports[s] = s
            subgraph_dict['inports'] = new_inports
            #print '--------subgraph dict after inports-----'
            #pprint(subgraph_dict)


            # for out ports:
            for o in outports.values():
                # Assign o to comp_name in agent_desc_dict
                comp_name = o.split('_PORT_')[0]
                new_dict['agent_descriptor_dict'][comp_name][1].append(o)

            # ALL STREAMS TUPLE
            # Add in internal/hidden streams
            for s in subgraph_dict['stream_names_tuple']:
                new_dict['stream_names_tuple'].append(s)
                #print 'added s from internal subgraph streams:'
                #pprint(new_dict['stream_names_tuple'])

            # Add in inport streams
            for s in subgraph_dict['inports'].values():
                if s not in new_dict['stream_names_tuple']:
                    new_dict['stream_names_tuple'].append(s)
                    #print 'added s from inports:'
                    #pprint(new_dict['stream_names_tuple'])

            # Add in outport streams
            for s in subgraph_dict['outports'].values():
                if s not in new_dict['stream_names_tuple']:
                    new_dict['stream_names_tuple'].append(s)
                #print 'added s from outports:'
                #pprint(new_dict['stream_names_tuple'])

            # Remove wrongly named streams (ie. subgraph_PORT_stream -> component_PORT_stream)
            for s in new_dict['stream_names_tuple']:
                if unfound in s:
                    temp_dict = deepcopy(new_dict['stream_names_tuple'])
                    temp_dict.remove(s)
                    new_dict['stream_names_tuple'] = temp_dict

            print '-----new dict with stream names tuple--------'
            pprint(new_dict)

            # Remove from list because this unfound comp is done
            unfound_comps.remove(unfound)



        # Done with one iteration. Prep for next one.
        print 'final dict is: '
        pprint(new_dict)
        iteration_count += 1
        json_file_name = 'json_file' + str(iteration_count) + '.json'
        json_file = open(json_file_name, 'w')
        json.dump(new_dict, json_file)
        json_file.close()

        # new dict is now in json_file_name.json
        with open(json_file_name) as json_file_original:
            j = json.load(json_file_original)

        #### GET SUBGRAPH NAMES #####
        # Make array of functions in components_test.py
        # (also includes random elements like '__builtins__', '__doc__', '__file__'
        comps_funcs = dir(components_test)
        #print '-------components I know------------'
        #pprint(comps_funcs)

        # Make array of functions in JSON
        JSON_funcs = []
        for i in j['agent_descriptor_dict'].keys():
            JSON_funcs.append(j['agent_descriptor_dict'][i][2])
        #print '---------funcs in JSON----------'
        #pprint(JSON_funcs)

        # If there are functions not in components_test.py...
        # collect them (they are prlly subgraphs)
        #unfound_comps = []
        for f in JSON_funcs:
            if f not in comps_funcs:
                unfound_comps.append(f)


        print 'done with iteration ' + str(iteration_count)
        #return unwrap_subgraph('json_file.json')

    print json_file_name
    return json_file_name

'''
def unwrap_subgraph(my_json_file_name):
    print 'input arg: ', my_json_file_name
    ## Go through all functions/modules in json file and make sure they're in
    ## components_test.py. Otherwise, there might be a subgraph.
    # Open new file to put the fully exposed graph JSON in
    # by copying over current json file
    with open(my_json_file_name) as json_file_original:
        j = json.load(json_file_original)

    #json_file = open('json_file.json', 'w')
    #json.dump(j, json_file)

    print '---------J = current agent dic------'
    pprint(j)

    #### GET SUBGRAPH NAMES #####
    # Make array of functions in components_test.py
    # (also includes random elements like '__builtins__', '__doc__', '__file__'
    comps_funcs = dir(components_test)
    #print '-------components I know------------'
    #pprint(comps_funcs)

    # Make array of functions in JSON
    JSON_funcs = []
    for i in j['agent_descriptor_dict'].keys():
        JSON_funcs.append(j['agent_descriptor_dict'][i][2])
    #print '---------funcs in JSON----------'
    #pprint(JSON_funcs)

    # If there are functions not in components_test.py...
    # collect them (they are prlly subgraphs)
    unfound_comps = []
    for f in JSON_funcs:
        if f not in comps_funcs:
            unfound_comps.append(f)

    new_dict = {}
    new_dict['agent_descriptor_dict'] = deepcopy(j['agent_descriptor_dict'])
    new_dict['stream_names_tuple'] = deepcopy(j['stream_names_tuple'])
    print '==============new_dict initialize:'
    pprint(new_dict)
    ##### EXPOSE SUBGRAPHS ########
    pprint(unfound_comps)
    if len(unfound_comps) > 0:
        for unfound in unfound_comps:
            print 'unfound: ', unfound
            try:
                # Look for .json for corresponding subgraph
                #path = '/home/klyap/Downloads/'
                path = 'JSON/'
                new_json = unfound + '.json'

                # Grab the exposed in and out ports from original JSON:
                with open(path + new_json) as new_json_file:
                    subgraph_json = json.load(new_json_file)
                #exposed_in = subgraph_json['inports']
                #exposed_out = rename_exposed_port(my_json_file_name, subgraph_json['outports'])

                # Look for new JSON file for the subgraph
                new_json = make_json(path + new_json)

                with open(new_json) as new_json_file:
                    subgraph_dict = json.load(new_json_file)

                #print '------subgraph_dict--------'
                #pprint
                #                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       (subgraph_dict)
                # Pick out needed parts
                # then pick out the parts that need to be replaced HERE

                # AGENT DICT
                # Replace unfound component entry with subgraph dict
                # For each component:
                # replace in/out stream with unfound's name
                # with correct component name
                unfound_entry = deepcopy(new_dict['agent_descriptor_dict'][unfound])
                print '------unfound entry------'
                pprint(unfound_entry)
                # Now that it's stored as unfound_entry, delete it from the dict
                del new_dict['agent_descriptor_dict'][unfound]


                # Add new unwrapped components
                for comp in subgraph_dict['agent_descriptor_dict'].keys():
                    new_dict['agent_descriptor_dict'][comp] = subgraph_dict['agent_descriptor_dict'][comp]

                #print '---new_dict with unwrapped comps---'
                #pprint(new_dict)

                # Get exposed outports and inports of subgraph
                inports = subgraph_dict['inports']
                outports = subgraph_dict['outports']
                #print '-----inports and outports------'
                #pprint(inports)
                #pprint(outports)
                #print '-------subgraph_dict ready for fixed in/out streams------'
                #pprint(subgraph_dict)

                # For in ports:
                #print '----------new dict ready for inports ----------'
                #pprint(new_dict)
                for comp in new_dict['agent_descriptor_dict']:
                    #print 'replacing input streams in ' + comp
                    #pprint(new_dict['agent_descriptor_dict'])

                    new_inputs = []
                    # DEBUG
                    #print 'debug: '
                    #pprint(new_dict['agent_descriptor_dict'][comp][0])
                    for s in new_dict['agent_descriptor_dict'][comp][0]:
                        #print 'should I replace ' + s
                        # if exposed output streams come from a comp in
                        # this subgraph, add this to comp's input streams
                        renamed_stream = s
                        if unfound in s:
                            # Replace s with correctly named stream in exposed outports
                            # by matching the s.split('_PORT_')[1] with a key in dict
                            # and extracting the value as my new s
                            print 'loooking for:'
                            pprint(s.split('_PORT_')[1])
                            pprint(outports)
                            renamed_stream = outports[s.split('_PORT_')[1]]
                            #print 'renaming:'
                            #print renamed_stream
                        new_inputs.append(renamed_stream)

                    new_dict['agent_descriptor_dict'][comp][0] = new_inputs
                    #print '---------just added new inputs to ' + comp
                    #pprint(new_dict['agent_descriptor_dict'][comp])

                # Now check components outside subgraphs for those
                # that connect to the inputs in our list
                # (These streams in new_inputs are currently named after
                # the in port. We want it to be the out port of the prev component)
                print '------------unfound entry----------------'
                pprint(unfound_entry)
                for i in range(len(inports.values())):
                    # Get component name from inport stream (ie. compname_PORT_in)
                    comp_name = inports.values()[i].split('_PORT_')[0]
                    print 'at index: ' + str(i)
                    print inports.values()[i]

                    print 'debug: '
                    pprint(new_dict['agent_descriptor_dict'])
                    print comp_name
                    print 'debug: '
                    pprint(unfound_entry[0][i])
                    # Match it with a input stream of the same index
                    new_dict['agent_descriptor_dict'][comp_name][0].append(unfound_entry[0][i])
                    #print 'just added an input stream:'
                    #pprint(new_dict['agent_descriptor_dict'])
                    #pprint(unfound_entry[0][i])
                    #pprint(new_dict['agent_descriptor_dict'][comp_name][0])

                # Now that the input streams inside each component are fixed
                # fix corresponding streams in inports of subgraph
                new_inports = {}
                for c in subgraph_dict['agent_descriptor_dict']:
                    if len(subgraph_dict['agent_descriptor_dict'][c][0]) > 0:
                        for s in subgraph_dict['agent_descriptor_dict'][c][0]:
                            new_inports[s] = s
                subgraph_dict['inports'] = new_inports
                #print '--------subgraph dict after inports-----'
                #pprint(subgraph_dict)


                # for out ports:
                for o in outports.values():
                    # Assign o to comp_name in agent_desc_dict
                    comp_name = o.split('_PORT_')[0]
                    new_dict['agent_descriptor_dict'][comp_name][1].append(o)

                #print '----- new_dict with all input & output streams fixed-----'
                #pprint(new_dict)



                # ALL STREAMS TUPLE

                #print '-------subgraph_dict ready for stream name tup------'
                #pprint(subgraph_dict)
                # Add in internal/hidden streams
                for s in subgraph_dict['stream_names_tuple']:
                    new_dict['stream_names_tuple'].append(s)
                    #print 'added s from internal subgraph streams:'
                    #pprint(new_dict['stream_names_tuple'])

                # Add in inport streams
                for s in subgraph_dict['inports'].values():
                    if s not in new_dict['stream_names_tuple']:
                        new_dict['stream_names_tuple'].append(s)
                        #print 'added s from inports:'
                        #pprint(new_dict['stream_names_tuple'])

                # Add in outport streams
                for s in subgraph_dict['outports'].values():
                    if s not in new_dict['stream_names_tuple']:
                        new_dict['stream_names_tuple'].append(s)
                    #print 'added s from outports:'
                    #pprint(new_dict['stream_names_tuple'])

                # Remove wrongly named streams (ie. subgraph_PORT_stream -> component_PORT_stream)
                for s in new_dict['stream_names_tuple']:
                    if unfound in s:
                        temp_dict = deepcopy(new_dict['stream_names_tuple'])
                        temp_dict.remove(s)
                        new_dict['stream_names_tuple'] = temp_dict

                print '-----new dict with stream names tuple--------'
                pprint(new_dict)



            except NameError:
                print 'No such function or subgraph JSON file: ' + f
                return 'No such function or subgraph JSON file: ' + f
    # RECURSE
        json_file = open('json_file.json', 'w')
        json.dump(new_dict, json_file)
        json_file.close()
        print 'going for the recursion'
        return unwrap_subgraph('json_file.json')
    else:
        print 'all functions found!'
        json_file = open('json_file.json', 'w')
        json.dump(new_dict, json_file)
        json_file.close()
        return 'json_file.json'



