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
	{ data: { id: 'multiply_elements_stream2', name:'multiply_elements_stream2 '} },
	{ data: { id: 'multiply_elements_stream3', name:'multiply_elements_stream3 '} },
	{ data: { id: 'print_value_stream1', name:'print_value_stream1 '} },
	{ data: { id: 'print_value_stream2', name:'print_value_stream2 '} },
	{ data: { id: 'multiply_elements_stream', name:'multiply_elements_stream '} },
	{ data: { id: 'print_value_stream', name:'print_value_stream '} },
	{ data: { id: 'generate_stream_of_random_integers', name:'generate_stream_of_random_integers '} }],
edges: [
	{ data: { stream: 'multiply_elements_stream1_PORT_out', source: 'multiply_elements_stream1', target: 'multiply_elements_stream2', name:'multiply_elements_stream1_PORT_out:'} },
	{ data: { stream: 'multiply_elements_stream2_PORT_out', source: 'multiply_elements_stream2', target: 'multiply_elements_stream3', name:'multiply_elements_stream2_PORT_out:'} },
	{ data: { stream: 'multiply_elements_stream2_PORT_out', source: 'multiply_elements_stream2', target: 'print_value_stream1', name:'multiply_elements_stream2_PORT_out:'} },
	{ data: { stream: 'multiply_elements_stream3_PORT_out', source: 'multiply_elements_stream3', target: 'print_value_stream2', name:'multiply_elements_stream3_PORT_out:'} },
	{ data: { stream: 'multiply_elements_stream_PORT_out', source: 'multiply_elements_stream', target: 'print_value_stream', name:'multiply_elements_stream_PORT_out:'} },
	{ data: { stream: 'generate_stream_of_random_integers_PORT_out', source: 'generate_stream_of_random_integers', target: 'multiply_elements_stream1', name:'generate_stream_of_random_integers_PORT_out:'} },
	{ data: { stream: 'generate_stream_of_random_integers_PORT_out', source: 'generate_stream_of_random_integers', target: 'multiply_elements_stream', name:'generate_stream_of_random_integers_PORT_out:'} }]
    },
  
  layout: {
    name: 'breadthfirst',
    directed: true,
    padding: 20
}
  });
  

var myVar;

var stream_names = ['generate_stream_of_random_integers_PORT_out', 'multiply_elements_stream1_PORT_out', 'multiply_elements_stream2_PORT_out', 'multiply_elements_stream2_PORT_out', 'multiply_elements_stream3_PORT_out', 'generate_stream_of_random_integers_PORT_out', 'multiply_elements_stream_PORT_out',];
var edge = ['edge[stream= "generate_stream_of_random_integers_PORT_out"]', 'edge[stream= "multiply_elements_stream1_PORT_out"]', 'edge[stream= "multiply_elements_stream2_PORT_out"]', 'edge[stream= "multiply_elements_stream2_PORT_out"]', 'edge[stream= "multiply_elements_stream3_PORT_out"]', 'edge[stream= "generate_stream_of_random_integers_PORT_out"]', 'edge[stream= "multiply_elements_stream_PORT_out"]',];
var value = ['' ,'7400.0' ,'' ,'' ,'' ,'74' ,'' ,'' ,'' ,'14800.0' ,'14800.0' ,'' ,'74' ,'' ,'' ,'' ,'' ,'14800.0' ,'14800.0' ,'74' ,'' ,'' ,'' ,'' ,'' ,'14800.0' ,'74' ,'' ,'' ,'' ,'' ,'' ,'' ,'74' ,'' ,'' ,'' ,'' ,'' ,'' ,'' ,'7400.0' ,'' ,'' ,'' ,'' ,'' ,'' ,'' ,'32' ,'' ,'' ,'' ,'' ,'32' ,'' ,'' ,'3200.0' ,'' ,'' ,'' ,'32' ,'' ,'' ,'' ,'6400.0' ,'6400.0' ,'' ,'32' ,'' ,'' ,'' ,'' ,'6400.0' ,'6400.0' ,'32' ,'' ,'' ,'' ,'' ,'' ,'6400.0' ,'32' ,'' ,'' ,'' ,'' ,'' ,'' ,'32' ,'' ,'' ,'' ,'' ,'' ,'' ,'' ,'3200.0' ,'' ,'' ,'' ,'' ,'' ,'' ,'' ,'86' ,'' ,'' ,'' ,'' ,'86' ,'' ,'' ,'8600.0' ,'' ,'' ,'' ,'86' ,'' ,'' ,'' ,'17200.0' ,'17200.0' ,'' ,'86' ,'' ,'' ,'' ,'' ,'17200.0' ,'17200.0' ,'86' ,'' ,'' ,'' ,'' ,'' ,'17200.0' ,'86' ,'' ,'' ,'' ,'' ,'' ,'' ,'86' ,'' ,'' ,'' ,'' ,'' ,'' ,'' ,'8600.0' ,'' ,'' ,'' ,'' ,'' ,'' ,'' ,'20' ,'' ,'' ,'' ,'' ,'20' ,'' ,'' ,'2000.0' ,'' ,'' ,'' ,'20' ,'' ,'' ,'' ,'4000.0' ,'4000.0' ,'' ,'20' ,'' ,'' ,'' ,'' ,'4000.0' ,'4000.0' ,'20' ,'' ,'' ,'' ,'' ,'' ,'4000.0' ,'20' ,'' ,'' ,'' ,'' ,'' ,'' ,'20' ,'' ,'' ,'' ,'' ,'' ,'' ,'' ,'2000.0' ,'' ,'' ,'' ,'' ,'' ,'' ,'' ,'84' ,'' ,'' ,'' ,'' ,'84' ,'' ,'' ,'8400.0' ,'' ,'' ,'' ,'84' ,'' ,'' ,'' ,'16800.0' ,'16800.0' ,'' ,'84' ,'' ,'' ,'' ,'' ,'16800.0' ,'16800.0' ,'84' ,'' ,'' ,'' ,'' ,'' ,'16800.0' ,'84' ,'' ,'' ,'' ,'' ,'' ,'' ,'84' ,'' ,'' ,'' ,'' ,'' ,'' ,'' ,'8400.0' ,'' ,'' ,'' ,'' ,'' ,'' ,'' ,'24' ,'' ,'' ,'' ,'' ,'24' ,'' ];
 
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