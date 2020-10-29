# executor-diagrams
This is an executor for generating solution level digrams from hamlet. 
It can convert a JSON file in a predefined structure into PNG diagram directly and in the meanwhile generate a template.py file that records the codes used to produce the diagram.

A JSON format file generated from hamlet with specific data format is read into the executor(by specifying the path of the JSON file) and the deployment diagram(PNG format) will be automatically generated. You can also construct a JSON file and generate your own graph, for more information on the structure of the JSON file, you can take a look at the generated_graph-2.json file in testCases folder.

The file diagrams_demo.py is the one that's doing the converting and the output graph will be stored in the same path with it.
During the process, a template.py file with readable Python codes for Diagrams to turn to graphs will be generated and stored in the same path as the JSON file used for converting.

# installation requirement
This tool will require pre installation of Graphviz, Diagrams, Jinja2 and Click.
Diagrams is a code to graph tool that allows user to write Python codes and generate graphs in different format. It uses Graphviz to render the graphs.
Jinja2 is used in the script to record the Python codes for the graph being generated (template.py).

# future improvement
In folder sampleDiagrams you can find the "upgrade - future work" folder where some more complex styling of the Python codes for Diagrams are there for reference as a future upgrade. More information could also be found on the Diagrams documentation page: https://diagrams.mingrammer.com/docs/getting-started/installation.
