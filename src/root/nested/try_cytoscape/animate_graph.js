$(function(){ // on dom ready

var cy = cytoscape({
  container: document.getElementById('cy'),

  style: cytoscape.stylesheet()
    .selector('node')
      .css({
        'content': 'data(name)',
        'text-valign': 'bottom',
        'color': 'black',
        'font-size': '15',
    'shape': 'rectangle',
    'background-color': 'orange',
    'width': 30,
    'height': 30,
    
      })
    .selector('edge')
      .css({
    'content': 'data(val)',
    'target-arrow-shape': 'triangle',
        'width': '10',
    'font-size': '12',
    'target-arrow-color': '#D3D3D3',
    'line-color': '#D3D3D3'
      })
    .selector(':selected')
      .css({
        'background-color': 'orange',
        'line-color': '#D3D3D3',
        'target-arrow-color': '#D3D3D3',
        'source-arrow-color': '#D3D3D3',
        'content': 'data(name)'
      })
    
    .selector('.faded')
      .css({
        'opacity': 0.25,
        'text-opacity': 0
      }),
  
  elements: {
    nodes: [
	{ data: { id: 'multiply_elements_stream1', name:'multiply_elements_stream1 '} },
	{ data: { id: 'split_into_even_odd_stream', name:'split_into_even_odd_stream '} },
	{ data: { id: 'print_value_stream1', name:'print_value_stream1 '} },
	{ data: { id: 'multiply_elements_stream', name:'multiply_elements_stream '} },
	{ data: { id: 'print_value_stream', name:'print_value_stream '} },
	{ data: { id: 'generate_stream_of_random_integers', name:'generate_stream_of_random_integers '} }],
edges: [
	{ data: { stream: 'multiply_elements_stream1_PORT_product', source: 'multiply_elements_stream1', target: 'print_value_stream', name:'multiply_elements_stream1_PORT_product:'} },
	{ data: { stream: 'split_into_even_odd_stream_PORT_even', source: 'split_into_even_odd_stream', target: 'multiply_elements_stream1', name:'split_into_even_odd_stream_PORT_even:'} },
	{ data: { stream: 'split_into_even_odd_stream_PORT_odd', source: 'split_into_even_odd_stream', target: 'multiply_elements_stream', name:'split_into_even_odd_stream_PORT_odd:'} },
	{ data: { stream: 'multiply_elements_stream_PORT_product', source: 'multiply_elements_stream', target: 'print_value_stream1', name:'multiply_elements_stream_PORT_product:'} },
	{ data: { stream: 'generate_stream_of_random_integers_PORT_out', source: 'generate_stream_of_random_integers', target: 'split_into_even_odd_stream', name:'generate_stream_of_random_integers_PORT_out:'} }]
    },
  
  layout: {
    name: 'breadthfirst',
    directed: true,
    padding: 20
}
  });
  

var myVar;

var stream_names = ['split_into_even_odd_stream_PORT_even', 'generate_stream_of_random_integers_PORT_out', 'multiply_elements_stream_PORT_product', 'split_into_even_odd_stream_PORT_odd', 'multiply_elements_stream1_PORT_product',];
var edge = ['edge[stream= "split_into_even_odd_stream_PORT_even"]', 'edge[stream= "generate_stream_of_random_integers_PORT_out"]', 'edge[stream= "multiply_elements_stream_PORT_product"]', 'edge[stream= "split_into_even_odd_stream_PORT_odd"]', 'edge[stream= "multiply_elements_stream1_PORT_product"]',];
var value = ['' ,'22' ,'' ,'' ,'' ,'22' ,'' ,'' ,'' ,'' ,'22' ,'' ,'' ,'' ,'' ,'22' ,'' ,'' ,'' ,'' ,'22' ,'' ,'' ,'' ,'' ,'22' ,'49' ,'' ,'' ,'' ];
 
var n = 0;
function myFunction() {
   myVar = setTimeout(myFunction, 200);
   var edge_index = n % edge.length;
   var sname = stream_names[edge_index];
   //var sname = cy.elements(edge[edge_index]).data('stream');
   //cy.elements(edge[n]).data('name', sname + ': ' + value[n]);
   cy.elements(edge[edge_index]).data('name', sname + ': ' + value[n]);
   cy.elements(edge[edge_index]).data('val', value[n]);
   //setTimeout(function(){
   //     cy.elements(edge[edge_index]).data('name', sname);
   //     cy.elements(edge[edge_index]).data('val', '');
   //     }, 500);
   if (n < value.length - 1){
       n = n + 1;
   } else{
       cy.elements(edge[edge_index]).data('name', sname );
       cy.elements(edge[edge_index]).data('val', '');
   }
}

var i = 0;
function myFunction2() {
   myVar = setTimeout(myFunction2, 1000);
   var seq_keys = Object.keys(seq);
   for (var stream in seq_keys){
      window.alert(stream);
      var val = seq[stream][i];
      
      window.alert(val);
      //var sname = cy.elements(edge[edge_index]).data('stream');
      cy.elements(edge['source =' + stream]).data('name', stream + ': ' + val);
      setTimeout(function(){cy.elements(edge['source =' + stream]).data('name', stream + ': ');}, 500);
   
   if (i < seq_keys[0].length - 1){
       i = i + 1;
    }
   }
}

myFunction();
    
}); // on dom ready