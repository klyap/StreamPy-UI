from operator import indexOf
if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from Stream import Stream
from OperatorsTest import stream_func
from components import *
from pprint import pprint

# Helper function to delete 'browser...'
def delete_startswith_substring(s, substring):
    if s.startswith(substring):
        return s[len(substring):]
    else:
        return s
    
#def clean_string(s, x):
#    return s[x:]

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

def rename_stream(original_arr, comp_list, x):
    renamed_arr = []
    for i in original_arr:
        #print('\n this is original arr: \n')
        #pprint(original_arr)
        #print('\n this is comp_list: \n')
        #pprint(comp_list)
        if '=' in i:
            renamed_arr.append(i)
        else:
            label_with_id, portname = clean_id(i[x:])
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
def make_comp_list(instance_dict, x):
    comp_list = dict()
    for component, connections in instance_dict.items():
        # populating comp_list
        label, cid = clean_id(component)
        label = label[x:]
        if label in comp_list.keys():
            comp_list[label].append(cid)
        else:
            comp_list[label] = [cid]

    return comp_list


# (Not used when running Animation.py
# in favor of instant-execution/animation)
# Helps populate a .py output file.
# Returns 2 values:
# a sorted instance dict & a str of the function calls in order
def function_calls(instance_dict, x):

    function_string = str()
    
    # Make comp_list, a dictionary of each module and it's instance id's
    comp_list = make_comp_list(instance_dict, x)
    
    # Make a copy of instance_dict and call it
    # instance_dict_copy.
    # instance_dict_copy remains unchanged throughout
    # this program, while instance_dict changes as
    # nodes are deleted from the graph.
    instance_dict_copy = dict()
    
    
    for component, connections in instance_dict.items():        
        # populating instance_dict_copy with correctly formatted stream names
        connections_copy = dict()
        connections_copy['in'] = rename_stream(connections['in'], comp_list, x)
        connections_copy['out'] = rename_stream(connections['out'], comp_list, x)
        instance_dict_copy[component] = connections_copy

    # sorted_components will be the topological sort of
    # the graph
    sorted_components = list()

    # While nodes remain in the graph, do:
    while instance_dict:
        # sources is a list of sources (no inputs) in
        # the graph.
        sources = []
        # Go through instance_dict and append components
        # that have no inputs
        for component, connections in instance_dict.items():
            if not connections['in'] or \
            (len(connections['in']) == 1 and '=' in str(connections['in'])):
                sources.append(component)

        if not sources:
            print 'ERROR: GRAPH HAS CYCLES!'
            return

        for component_1 in sources:
            connections_1 = instance_dict[component_1]
            # outputs_1 is the list of outputs of component_1
            outputs_1 = connections_1['out']

            # for each output port, output_1, of
            # the source, component_1, do:
            for output_1 in outputs_1:
                # Inspect remaining graph and
                # delete output_1 from the inputs of each
                # node in the graph.
                for component_2, connections_2 in instance_dict.items():
                    inputs_2 = connections_2['in']
                    # If the output port, output_1, is an input then
                    # delete it from the input list of this component,
                    # i.e., component_2
                    if output_1 in inputs_2:
                        connections_2['in'] = \
                          [input_2 for input_2 in inputs_2 if input_2 != output_1]
                        instance_dict[component_2] = {
                            'in':connections_2['in'],
                            'out':connections_2['out']}

            # Add a 3-element list with the name of the component, its
            # inputs and its outputs to sorted_components.
            sorted_components.append([component_1,
                                      instance_dict_copy[component_1]['in'],
                                      instance_dict_copy[component_1]['out']]
                                      )
            # Deleted the source itself.
            del(instance_dict[component_1])

    # The graph is empty, and all the nodes have been sorted.

    # Cleaning the names of components and ports.
    for c in sorted_components:
        c[0] = c[0][x:]

        # output_string is something like:
        # 'output_1, output_2, output_3 = ' if there is at least one
        # output, and is the empty string if there is no output.
        output_string = str()
        # streams_string are the strings that name the streams
        # ie. stream_name.set_name('stream_name')
        streams_string = str()
        
        for o in c[2]:
            output_string = output_string + o + ', '
            streams_string = streams_string + o + '.set_name(\'' + o + '\')\n'
        # Delete the very last comma
        output_string = output_string[:-2]
        if output_string:
            output_string += ' = '

        # input_string is '()' if there are no inputs.
        # and otherwise it is like: (input_1, input_2, input_3)
        if not c[1]:
            input_string = ''
        else:
            input_string = str()
            
            for i in c[1]:
                input_string = input_string + i + ', '
            input_string = input_string[:-2]

        label, id = clean_id(c[0])
        ## statement is a function call in this format: 
        ## output_stream = component(input stream)
        statement = output_string + label + '(' + input_string + ')'

        ## Visualization data is the stream values at each component,
        ## so I'm adding a "write to file" line after each function call

        if '' == input_string:
            viz_call = ''
        else:
            viz_call = 'write_stream' + '(' + input_string.split(',')[0] + ')\n'
        
        function_string += statement +  '\n'
        function_string += streams_string

    return instance_dict_copy, function_string

