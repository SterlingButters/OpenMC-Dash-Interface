import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, State, Input

import openmc
import openmc.model
import openmc.mgxs

import numpy as np
import time
import io
from glob import glob
import os
from shutil import copyfile
from contextlib import redirect_stdout

from app import app

layout = html.Div([

    # Title
    html.H2('Runtime Verification & Model Generation',
            style={
                'position': 'relative',
                'top': '0px',
                'left': '10px',
                'font-family': 'Dosis',
                'display': 'inline',
                'font-size': '4.0rem',
                'color': '#4D637F'
            }), html.Br(),

    #############################################################################
    # Loading/Writing XML Files
    html.Div([
        dcc.ConfirmDialog(
            id='confirm',
            message='Are you sure you want to write these contents to the file?',
        ),
        html.Div([
            html.Label('Geometry XML File Contents'),
            html.Br(),
            dcc.Textarea(id='geometry-xml', rows=20, cols=50, placeholder='Write XML contents here and Load to File'
                                                                          'or leave blank and Load from File'),
            html.Br(),
            html.Button('Load Geometry XML File', n_clicks=0, id='load-geometry'),
            html.Button('Write Geometry XML File', n_clicks=0, id='write-geometry'),
            html.P(id='geometry-placeholder'),  # Used as dummy for mandatory Output in decorator

            html.Label('Plots XML File Contents'),
            html.Br(),
            dcc.Textarea(id='plots-xml', rows=20, cols=50, placeholder='Write XML contents here and Load to File'
                                                                       'or leave blank and Load from File'),
            html.Br(),
            html.Button('Load Plot XML File', n_clicks=0, id='load-plots'),
            html.Button('Write Plot XML File', n_clicks=0, id='write-plots'),
            html.P(id='plots-placeholder'),  # Used as dummy for mandatory Output in decorator
        ],
            style=dict(
                display='table-cell',
                verticalAlign="top",
                width='30%'
            ),
        ),

        html.Div([
            html.Label('Materials XML File Contents'),
            html.Br(),
            dcc.Textarea(id='materials-xml', rows=20, cols=50, placeholder='Write XML contents here and Load to File'
                                                                           'or leave blank and Load from File'),
            html.Br(),
            html.Button('Load Material XML File', n_clicks=0, id='load-materials'),
            html.Button('Write Material XML File', n_clicks=0, id='write-materials'),
            html.P(id='material-placeholder'),  # Used as dummy for mandatory Output in decorator
        ],
            style=dict(
                width='30%',
                display='table-cell',
                verticalAlign="top",
            ),
        ),

        html.Div([
            html.Label('Tallies XML File Contents'),
            html.Br(),
            dcc.Textarea(id='tallies-xml', rows=20, cols=50, placeholder='Write XML contents here and Load to File'
                                                                         'or leave blank and Load from File'),
            html.Br(),
            html.Button('Load Tallies XML File', n_clicks=0, id='load-tallies'),
            html.Button('Write Tallies XML File', n_clicks=0, id='write-tallies'),
            html.P(id='tallies-placeholder'),  # Used as dummy for mandatory Output in decorator

            html.Label('Settings XML File Contents'),
            html.Br(),
            dcc.Textarea(id='settings-xml', rows=20, cols=50, placeholder='Write XML contents here and Load to File'
                                                                          'or leave blank and Load from File'),
            html.Br(),
            html.Button('Load Settings XML File', n_clicks=0, id='load-settings'),
            html.Button('Write Material XML File', n_clicks=0, id='write-settings'),
            html.P(id='settings-placeholder'),  # Used as dummy for mandatory Output in decorator
        ],
            style=dict(
                width='30%',
                display='table-cell',
                verticalAlign="top",
            ),
        ),
    ], style=dict(
        width='100%',
        display='table',
    ),
    ),
    #############################################################################
    # Simulation
    html.Button('Generate XML Files', id='xml-button', n_clicks=0),
    html.Div(id='memory-display'),
    html.Button('Run Simulation', id='run-button', n_clicks=0),
    html.Br(),
    dcc.Textarea(id='console-output', rows=40, cols=75, placeholder='Console Output will appear here...',
                 readOnly=True),

])


############################################################################################################
# Load XML from File
@app.callback(
    Output('materials-xml', 'value'),
    [Input('load-materials', 'n_clicks')],
)
def show_material_xml_contents(run_click):
    if run_click > 0:
        script_dir = os.path.dirname(__file__)
        filename = os.path.join(script_dir, '../xml-files/materials.xml')
        contents = open(filename).read()
        return contents


@app.callback(
    Output('geometry-xml', 'value'),
    [Input('load-geometry', 'n_clicks')],
)
def show_material_xml_contents(run_click):
    if run_click > 0:
        script_dir = os.path.dirname(__file__)
        filename = os.path.join(script_dir, '../xml-files/geometry.xml')
        contents = open(filename).read()
        return contents


@app.callback(
    Output('tallies-xml', 'value'),
    [Input('load-tallies', 'n_clicks')],
)
def show_material_xml_contents(run_click):
    if run_click > 0:
        script_dir = os.path.dirname(__file__)
        filename = os.path.join(script_dir, '../xml-files/tallies.xml')
        contents = open(filename).read()
        return contents


@app.callback(
    Output('settings-xml', 'value'),
    [Input('load-settings', 'n_clicks')],
)
def show_material_xml_contents(run_click):
    if run_click > 0:
        script_dir = os.path.dirname(__file__)
        filename = os.path.join(script_dir, '../xml-files/settings.xml')
        contents = open(filename).read()
        return contents


@app.callback(
    Output('plots-xml', 'value'),
    [Input('load-plots', 'n_clicks')],
)
def show_material_xml_contents(run_click):
    if run_click > 0:
        script_dir = os.path.dirname(__file__)
        filename = os.path.join(script_dir, '../xml-files/plots.xml')
        contents = open(filename).read()
        return contents


#######################################################################################################################
# Write XML to File

@app.callback(Output('confirm', 'displayed'),
              [Input('write-materials', 'n_clicks'),
               Input('write-geometry', 'n_clicks'),
               Input('write-tallies', 'n_clicks'),
               Input('write-settings', 'n_clicks'),
               Input('write-plots', 'n_clicks')])
def display_confirm(mat_click, geo_click, tal_click, set_click, plot_click):
    if mat_click or geo_click or tal_click or set_click or plot_click:
        return True
    return False


@app.callback(
    Output('material-placeholder', 'children'),
    [Input('confirm', 'submit_n_clicks')],
    [State('materials-xml', 'value')],
)
def write_material_xml_contents(write_click, contents):
    if write_click:
        script_dir = os.path.dirname(__file__)
        filename = os.path.join(script_dir, '../xml-files/materials.xml')
        file = open(filename, "w+")
        file.write(contents)
        file.close()


@app.callback(
    Output('geometry-placeholder', 'children'),
    [Input('confirm', 'submit_n_clicks')],
    [State('geometry-xml', 'value')],
)
def write_material_xml_contents(write_click, contents):
    if write_click:
        script_dir = os.path.dirname(__file__)
        filename = os.path.join(script_dir, '../xml-files/geometry.xml')
        file = open(filename, "w+")
        file.write(contents)
        file.close()


@app.callback(
    Output('tallies-placeholder', 'children'),
    [Input('confirm', 'submit_n_clicks')],
    [State('tallies-xml', 'value')],
)
def write_material_xml_contents(write_click, contents):
    if write_click:
        script_dir = os.path.dirname(__file__)
        filename = os.path.join(script_dir, '../xml-files/tallies.xml')
        file = open(filename, "w+")
        file.write(contents)
        file.close()


@app.callback(
    Output('settings-placeholder', 'children'),
    [Input('confirm', 'submit_n_clicks')],
    [State('settings-xml', 'value')],
)
def write_material_xml_contents(write_click, contents):
    if write_click:
        script_dir = os.path.dirname(__file__)
        filename = os.path.join(script_dir, '../xml-files/settings.xml')
        file = open(filename, "w+")
        file.write(contents)
        file.close()


@app.callback(
    Output('plots-placeholder', 'children'),
    [Input('confirm', 'submit_n_clicks')],
    [State('plots-xml', 'value')],
)
def write_material_xml_contents(write_click, contents):
    if write_click:
        script_dir = os.path.dirname(__file__)
        filename = os.path.join(script_dir, '../xml-files/plots.xml')
        file = open(filename, "w+")
        file.write(contents)
        file.close()


#######################################################################################################################

@app.callback(
    Output('memory-display', 'children'),
    [Input('xml-button', 'n_clicks')],

    [State('material-stores', 'data'),

     State('cell-stores', 'data'),
     State('assembly-stores', 'data'),
     State('boundary-stores', 'data'),

     State('mesh-stores', 'data'),

     State('mesh-score-stores', 'data')]
)
def build_model(click, material_data, cell_data, assembly_data, boundary_data, mesh_data, score_data):
    if click:
        model = openmc.model.Model()

        print(material_data)

        print(cell_data)
        print(assembly_data)
        print(boundary_data)

        print(score_data)

        #######################################
        # Materials

        materials = openmc.Materials([])
        for material in material_data.keys():
            density = material_data[material]['density']
            temperature = material_data[material]['temperature']

            mat_object = openmc.Material(name=material)
            mat_object.set_density('g/cm3', density)
            mat_object.temperature = temperature
            mat_object.depletable = False

            elements = material_data[material]['elements']
            masses = material_data[material]['masses']
            compositions = material_data[material]['compositions']
            types = material_data[material]['types']

            for i in range(len(elements)):
                if float(masses[i]).is_integer() or masses[i] == 0:
                    mat_object.add_element(element=elements[i],
                                           percent=compositions[i],
                                           percent_type=types[i],
                                           enrichment=None)
                else:
                    mat_object.add_nuclide(nuclide=str(masses[i])+elements[i],
                                           percent=compositions[i],
                                           percent_type=types[i])

            materials.append(mat_object)

        model.materials = materials

        #######################################
        # Mesh

        mesh = openmc.Mesh()
        mesh.type = 'regular'
        dim_x = mesh_data['x-resolution']
        dim_y = mesh_data['y-resolution']
        dim_z = mesh_data['z-resolution']
        width = mesh_data['width']
        depth = mesh_data['depth']
        height = mesh_data['height']
        mesh.dimension = [dim_x, dim_y, dim_z]
        mesh.lower_left = [-width / 2, -depth / 2, -height / 2]
        mesh.width = [width / dim_x, depth / dim_y, height / dim_z]

        # Create a mesh filter
        mesh_filter = openmc.MeshFilter(mesh)

        #######################################
        # Cross-sections

        #######################################
        # Tallies/Scores

        model.tallies = openmc.Tallies()
        # mgxs_lib.add_to_tallies_file(model.tallies, merge=True)

        # Instantiate a flux tally; Other valid options: 'current', 'fission', etc
        mesh_tally = openmc.Tally(name='Mesh')
        mesh_tally.filters = [mesh_filter]
        mesh_tally.scores = score_data['scores']

        energy_tally = openmc.Tally(name='Energy')
        # energy_tally.filters = [energy_filter]
        energy_tally.scores = score_data['scores']

        # Add tallies to the tallies file
        model.tallies.append(mesh_tally)
        model.tallies.append(energy_tally)

        #######################################
        # Settings

        return html.P('Success')

#######################################################################################################################


@app.callback(
    Output('console-output', 'value'),
    [Input('run-button', 'n_clicks')], )
def run_model(click):
    if int(click) > 0:

        script_dir = os.path.dirname(__file__)
        xml_path_src = os.path.join(script_dir, '../xml-files/')
        xml_files_src = glob('{}*.xml'.format(xml_path_src))

        for file in xml_files_src:
            xml_file_name = os.path.basename(file)
            copyfile(os.path.join(xml_path_src, xml_file_name), os.path.join(script_dir, xml_file_name))

        xml_files_dst = glob('{}*.xml'.format(script_dir))
        print(xml_files_dst)

        pass_test = False
        while not pass_test:
            bool_array = []
            for file in range(len(xml_files_dst)):
                exists = os.path.exists(xml_files_dst[file])
                if exists:
                    bool_array.append(exists)

            if np.array(bool_array).all():
                pass_test = True
                print('All files exist')

            time.sleep(1)

        output = io.StringIO()
        with redirect_stdout(output):
            openmc.run()

        for file in xml_files_dst:
            os.remove(file)

        return output.getvalue()
