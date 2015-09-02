import os
from pprint import pprint
import sys
import example
#import animation
import Animation
from Animation import *
from Subgraph import *
from Multiprocessing import *

###################################################
def dispatch(json_file_name):
    # Convert JSON to my format
    print 'json file name: ', json_file_name
    agent_dict_json = make_json(json_file_name)

    # DEBUG
    print 'in dispatch'

    # Extract dict/tup from it
    with open(agent_dict_json) as data_file:
        json_data = json.load(data_file)

    # Case 1: No groups -> unwrap subgraphs -> animate
    if 'groups' not in json_data.keys():
        print 'no groups!'

        agent_dict_json = unwrap_subgraph(agent_dict_json)
        print agent_dict_json
        make_js(agent_dict_json)

    # Case 2: Has groups -> unwrap subgraphs -> parallel process
    else:
        print 'has groups!'

        big_dict = parallel_dict(json_data)
        run_parallel(big_dict)

###################################################
## If you're running from an IDE, use this:
#var = raw_input("Please enter name of JSON: ")
#var = str(var)

#var = 'components_test.json'
## WORKING CASE:
#var = 'JSON/SplitEvenOdd.json'
#execfile(example.ex(var))
#animation.animate(var)

## ERROR CASE 1
## Error in: components_test.py split_stream() component
var1 = 'JSON/makenetwork.json'
#execfile(example.ex(var1))    ## IF YOU COMMENT THIS LINE OUT, VAR WORKS
#animation.animate(var1)

## ERROR CASE 2: both example.py (running the output Py file) and 
## running the animation don't work
## Error in: components_test.py multiples_stream() component
var2 = 'JSON/animation.json'
#execfile(example.ex(var2))
#animation.animate(var2)


## CURRENT TESTING PARAMS PARSING:
#var3 = '/home/klyap/Downloads/main.json' #new 3-input components for split
var3 = 'JSON/splitparams.json' #equivalent non-3-input components

#var3 = '/home/klyap/Downloads/multiplyparam.json' #new 3-input components for multiply
#var3 = '/home/klyap/Downloads/evenodd.json' #new 3-input components for evenodd

var4 = 'agent_descriptor.json'
#execfile(example.ex(var3))
#animation.animate(var3)

## Experiment with running from Animation
## Should work for both Flowhub and my JSON files (ie var 3 and var 4)
var5 = '/home/klyap/Downloads/multiplyparam.json' #subgraphs with same components that criss cross
#var6 = '/home/klyap/Downloads/simplesubgraph.json'
var6 = 'JSON/simplesubgraph.json' # for Windows
#var6 = '/home/klyap/Downloads/subgraph_demo.json'
var7 = '/home/klyap/Downloads/simplegroups.json'
#Animation.make_json(var7)

# for groups..
#Animation.dispatch(var6)
    
var8 = '/home/klyap/Downloads/TwitterSentiment.json'

var9 = 'JSON/doublenested.json'
#dispatch(var9)
    
###################################################
## This works if you're on terminal.
## Usage: navigate into the directory with this file
##        type: python run.py NAME_OF_JSON_FILE
var = sys.argv
#fullpath = '/home/klyap/Downloads/' + var[1]
fullpath = 'JSON/' + var[1]
#execfile(example.ex(fullpath))
#Animation.dispatch(fullpath)
dispatch(fullpath)


