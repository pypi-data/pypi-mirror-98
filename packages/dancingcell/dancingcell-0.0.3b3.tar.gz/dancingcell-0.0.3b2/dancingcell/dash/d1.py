#   coding: utf-8
#   This file is part of potentialmind.

#   potentialmind is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License.

__author__ = 'Guanjie Wang'
__version__ = 1.0
__maintainer__ = 'Guanjie Wang'
__email__ = "gjwang@buaa.edu.cn"
__date__ = "2020/07/18"

import dash
import dash_html_components as html
import dash_core_components as dcc

# standard Crystal Toolkit import
import crystal_toolkit.components as ctc

# create Dash app as normal
app = dash.Dash()

# create our crystal structure using pymatgen
from pymatgen import Structure, Lattice

def hello_sci():
    # create your layout
    my_layout = html.Div(["Hello scientist!"])

    # tell Crystal Toolkit about the app and layout we want to display
    ctc.register_crystal_toolkit(app=app, layout=my_layout, cache=None)

    # allow app to be run using "python app.py"
    # in production, deploy behind gunicorn or similar
    # see Dash documentation for more information

def run():
    structure = Structure(Lattice.cubic(4.2), ["Na", "K"], [[0, 0, 0], [0.5, 0.5, 0.5]])

    # create the Crystal Toolkit component
    structure_component = ctc.StructureMoleculeComponent(structure)
    # add the component's layout to our app's layout
    my_layout = html.Div([structure_component.layout()])

    # as explained in "preamble" section in documentation
    ctc.register_crystal_toolkit(app=app, layout=my_layout, cache=None)


if __name__ == "__main__":
    run()
    app.run_server(debug=True, port=8050)