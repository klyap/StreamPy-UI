# StreamPy-UI
A visual tool for programming streaming apps using the package PStreams using Flowhub

# Documentation
http://klyap.github.io/StreamPy-UI/

# Get started with a tutorial!
http://klyap.github.io/StreamPy-UI/Getting%20Started.html

1. Download this repo and get a Flowhub account at https://app.flowhub.io
2. In Flowhub, make your own components using this template:
  
  noflo = require 'noflo'
  
  exports.getComponent = ->
    c = new noflo.Component
    
    c.inPorts.add 'func', (event, payload) ->
      return unless event is 'data'
      # Makes a field for function name
      c.outPorts.out.send payload
    
    c.inPorts.add 'type', (event, payload) ->
      return unless event is 'data'
      # Makes a field for wrapper type
      c.outPorts.out.send payload
    
    c.inPorts.add 'state', (event, payload) ->
      return unless event is 'data'
      # Makes a field for state, if any
      c.outPorts.out.send payload
    
    c.inPorts.add 'multiplier', (event, payload) ->
      return unless event is 'data'
      # Makes a field for a constant parameter, if any
      c.outPorts.out.send payload
    
    c.inPorts.add 'in', (event, payload) ->
      return unless event is 'data'
      # Makes a port where incoming stream is connected to
      c.outPorts.out.send payload
    
    c.outPorts.add 'out'
    # Makes a port where output stream comes out
  
    c

