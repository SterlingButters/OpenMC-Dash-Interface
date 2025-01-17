import os

import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
import numpy as np
import openmc
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objs as go
from dash.dependencies import Output, State, Input
from dash.exceptions import PreventUpdate

from app import app

# Add Periodic Table Data
element = [['Hydrogen', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Helium'],
           ['Lithium', 'Beryllium', '', '', '', '', '', '', '', '', '', '', 'Boron', 'Carbon', 'Nitrogen', 'Oxygen',
            'Fluorine', 'Neon'],
           ['Sodium', 'Magnesium', '', '', '', '', '', '', '', '', '', '', 'Aluminium', 'Silicon', 'Phosphorus',
            'Sulfur', 'Chlorine', ' Argon'],
           ['Potassium', ' Calcium', ' Scandium', ' Titanium', ' Vanadium', ' Chromium', 'Manganese', 'Iron', 'Cobalt',
            'Nickel', 'Copper', 'Zinc', 'Gallium', 'Germanium', 'Arsenic', 'Selenium', 'Bromine', 'Krypton'],
           ['Rubidium', 'Strontium', 'Yttrium', 'Zirconium', 'Niobium', 'Molybdenum', 'Technetium', 'Ruthenium',
            'Rhodium', 'Palladium', 'Silver', 'Cadmium', 'Indium', 'Tin', 'Antimony', 'Tellurium', 'Iodine', 'Xenon'],
           [' Cesium', ' Barium', '', 'Hafnium', 'Tantalum', 'Tungsten', 'Rhenium', 'Osmium', 'Iridium', 'Platinum',
            'Gold', 'Mercury', 'Thallium', 'Lead', 'Bismuth', 'Polonium', 'Astatine', 'Radon'],
           [' Francium', ' Radium', '', 'Rutherfordium', 'Dubnium', 'Seaborgium', 'Bohrium', 'Hassium', 'Meitnerium',
            'Darmstadtium', 'Roentgenium', 'Copernicium', 'Ununtrium', 'Ununquadium', 'Ununpentium', 'Ununhexium',
            'Ununseptium', 'Ununoctium'],
           ['', '', 'Lanthanum', 'Cerium', 'Praseodymium', 'Neodymium', 'Promethium', 'Samarium', 'Europium',
            'Gadolinium', 'Terbium', 'Dysprosium', 'Holmium', 'Erbium', 'Thulium', 'Ytterbium', 'Lutetium', ''],
           ['', '', 'Actinium', 'Thorium', 'Protactinium', 'Uranium', 'Neptunium', 'Plutonium', 'Americium', 'Curium',
            'Berkelium', 'Californium', 'Einsteinium', 'Fermium', 'Mendelevium', 'Nobelium', 'Lawrencium', ''], ]

symbol = [['H', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'He'],
          ['Li', 'Be', '', '', '', '', '', '', '', '', '', '', 'B', 'C', 'N', 'O', 'F', 'Ne'],
          ['Na', 'Mg', '', '', '', '', '', '', '', '', '', '', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar'],
          ['K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr'],
          ['Rb ', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe'],
          ['Cs', 'Ba', '', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn'],
          ['Fr', 'Ra', '', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Uut', 'Fl', 'Uup', 'Lv', 'Uus',
           'Uuo'],
          ['', '', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', ''],
          ['', '', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', '']]

atomic_number = [['1', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '2'],
                 ['3', '4', '', '', '', '', '', '', '', '', '', '', '5', '6', '7', '8', '9', '10'],
                 ['11', '12', '', '', '', '', '', '', '', '', '', '', '13', '14', '15', '16', '17', '18'],
                 ['19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35',
                  '36'],
                 ['37 ', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53',
                  '54'],
                 ['55', '56', '', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85',
                  '86'],
                 ['87', '88', '', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115',
                  '116', '117', '118'],
                 ['', '', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', ''],
                 ['', '', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '100', '101', '102', '103',
                  '']]

atomic_mass = [[1.00794, .0, .0, .0, .0, .0, .0, .0, .0, .0, .0, .0, .0, .0, .0, .0, .0, 4.002602],
               [6.941, 9.012182, .0, .0, .0, .0, .0, .0, .0, .0, .0, .0, 10.811, 12.0107, 14.0067, 15.9994, 18.9984032,
                20.1797],
               [22.98976928, 24.3050, .0, .0, .0, .0, .0, .0, .0, .0, .0, .0, 26.9815386, 28.0855, 30.973762, 32.065,
                35.453, 39.948],
               [39.0983, 40.078, 44.955912, 47.867, 50.9415, 51.9961, 54.938045, 55.845, 58.933195, 58.6934, 63.546,
                65.38, 69.723, 72.64, 74.92160, 78.96, 79.904, 83.798],
               [85.4678, 87.62, 88.90585, 91.224, 92.90638, 95.96, 98, 101.07, 102.90550, 106.42, 107.8682, 112.411,
                114.818, 118.710, 121.760, 127.60, 126.90447, 131.293],
               [132.9054519, 137.327, .0, 178.49, 180.94788, 183.84, 186.207, 190.23, 192.217, 195.084, 196.966569,
                200.59, 204.3833, 207.2, 208.98040, 209, 210, 222],
               [223, 226, .0, 267, 268, 271, 272, 270, 276, 281, 280, 285, 284, 289, 288, 293, 'unknown', 294],
               [.0, .0, 138.90547, 140.116, 140.90765, 144.242, 145, 150.36, 151.964, 157.25, 158.92535, 162.500,
                164.93032, 167.259, 168.93421, 173.054, 174.9668, .0],
               [.0, .0, 227, 232.03806, 231.03588, 238.02891, 237, 244, 243, 247, 247, 251, 252, 257, 258, 259, 262,
                .0], ]

z = [[.8, .0, .0, .0, .0, .0, .0, .0, .0, .0, .0, .0, .0, .0, .0, .0, .0, 1.],
     [.1, .2, .0, .0, .0, .0, .0, .0, .0, .0, .0, .0, .7, .8, .8, .8, .9, 1.],
     [.1, .2, .0, .0, .0, .0, .0, .0, .0, .0, .0, .0, .6, .7, .8, .8, .9, 1],
     [.1, .2, .3, .3, .3, .3, .3, .3, .3, .3, .3, .3, .6, .7, .8, .8, .9, 1.],
     [.1, .2, .3, .3, .3, .3, .3, .3, .3, .3, .3, .3, .6, .6, .7, .7, .9, 1.],
     [.1, .2, .4, .3, .3, .3, .3, .3, .3, .3, .3, .3, .6, .6, .6, .7, .9, 1.],
     [.1, .2, .5, .3, .3, .3, .3, .3, .3, .3, .3, .3, .6, .6, .6, .6, .9, 1.],
     [.0, .0, .4, .4, .4, .4, .4, .4, .4, .4, .4, .4, .4, .4, .4, .4, .4, .0],
     [.0, .0, .5, .5, .5, .5, .5, .5, .5, .5, .5, .5, .5, .5, .5, .5, .5, .0], ]

# Display element name and atomic mass on hover
hover = []
for a in range(len(symbol)):
    hover.append(
        [i + ': ' + j + '<br>' + 'Atomic Mass: ' + str(k) for i, j, k in zip(symbol[a], element[a], atomic_mass[a])])

# Invert Matrices
symbol = symbol[::-1]
atomic_number = atomic_number[::-1]
hover = hover[::-1]
z = z[::-1]

x = np.arange(np.shape(z)[1])
y = np.arange(np.shape(z)[0])

# Set Colorscale
colorscale = [[0.0, 'rgb(255,255,255)'], [.1, 'rgb(87, 27, 103)'],
              [.2, 'rgb(65, 69, 133)'], [.3, 'rgb(55, 96, 139)'],
              [.4, 'rgb(46, 120, 141)'], [.5, 'rgb(41, 145, 139)'],
              [.6, 'rgb(45, 167, 133)'], [.7, 'rgb(74, 189, 115)'],
              [.8, 'rgb(126, 207, 89)'], [.9, 'rgb(189, 216, 88)'],
              [1.0, 'rgb(252, 229, 64)']]

annotations = []
for n in range(np.shape(z)[0]):
    for m in range(np.shape(z)[1]):
        annotations.append(go.layout.Annotation(text=str(symbol[n][m]), x=x[m], y=y[n],
                                                xref='x1', yref='y1', showarrow=False,
                                                font=dict(family='Courier New',
                                                          size=15,
                                                          color='black')))

        annotations.append(go.layout.Annotation(text=str(atomic_number[n][m]), x=x[m] + .3, y=y[n] + .3,
                                                xref='x1', yref='y1', showarrow=False,
                                                font=dict(family='Courier New',
                                                          size=10,
                                                          color='black')
                                                ))

heatmap = go.Heatmap(x=x, y=y, z=z, hoverinfo='text', text=hover, colorscale=colorscale, showscale=False, opacity=.5)

data = [heatmap]

periodic_table = go.Figure(data=data)
periodic_table['layout'].update(
    title="Periodic Table of Elements",
    annotations=annotations,
    xaxis=dict(zeroline=False, showgrid=False, showticklabels=False, ticks='', ),
    yaxis=dict(zeroline=False, showgrid=False, showticklabels=False, ticks='', ),
    width=800,
    height=500,
    autosize=False
)

#######################################################################################################################


layout = html.Div([

    # Title
    html.H2('Materials Configuration',
            style={
                'position': 'relative',
                'top': '0px',
                'left': '10px',
                'font-family': 'Dosis',
                'display': 'inline',
                'font-size': '4.0rem',
                'color': 'rgb(76, 1, 3)'
            }),

    html.Br(),

    html.Div([
        html.Div([
            html.Div([
                html.H4("Add a Material"),
                html.P("""
            First, we need to create some materials with which we plan to fill our geometry. 
            Begin by entering the desired parameters and then submit the material to memory 
            once the parameters are acceptable. If a required parameter is unfilled, the material
            will not be submitted to memory and thus will not be added to the dropdown menu.
            The dropdown menu selector allows you to select previously submitted materials to view
            or make changes to subsequent parameters.  
               """),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Label('Material Name'),
                            dcc.Input(id='material-name', placeholder='Enter Material Name', type="text"), html.Br(),

                            html.Label('Material Density'),
                            daq.NumericInput(
                                id='material-density',
                                min=0,
                                max=25,
                                value=10.1,
                                size=193, style=dict(position='absolute', left=10)
                            ), html.Br(), html.Br(),

                            html.Label('Material Temperature'),
                            daq.NumericInput(
                                id='material-temperature',
                                min=0,
                                max=4000,
                                value=250,
                                size=193, style=dict(position='absolute', left=10)
                            ), html.Br(), html.Br(), html.Br(), html.Br(),
                            html.Button('Submit Material', id='submit-material-button', n_clicks_timestamp=0),
                            html.Div(id='material-message')
                        ],
                            style=dict(
                                display='table-cell',
                                verticalAlign="top",
                                width='50%'
                            ),
                        ),
                        html.Div([
                            daq.Thermometer(
                                min=0,
                                max=4000,
                                value=250,
                                showCurrentValue=True,
                                units="F",
                                size=250
                            ),
                        ],
                            style=dict(
                                display='table-cell',
                                verticalAlign="top",
                                width='50%'
                            ),
                        )
                    ], style=dict(
                        width='100%',
                        display='table',
                    )),
                ]),
                dcc.Graph(id='material-display')
            ],
                style=dict(
                    display='table-cell',
                    verticalAlign="top",
                    width='50%'
                ),
            ),

            html.Div([
                html.H4("Add a Composition Constituent"),
                html.P("""
                        Now that a material has been submitted, it is time to define its composition. You may make a 
                        selection from the periodic table to define the element and then choose whether you would like 
                        to make the composition entry based on atomic or weight %. If these fields are left blank, the 
                        natural element will be selected from the periodic table with no alteration.
                """),
                html.H5("List of Materials"),
                dcc.Dropdown(id='material-dropdown'),
                dcc.Graph(id='periodic-table',
                          figure=periodic_table
                          ),
                html.Div(id='chosen-element'),
                html.Div([

                    html.Div([
                        html.Div([
                            html.Div(style=dict(height=30)),
                            dcc.Input(id='atomic-mass', placeholder='Enter Atomic Mass (if isotope)', type='number',
                                      size=70),
                        ],
                            style=dict(
                                display='table-cell',
                                verticalAlign="top",
                                width='30%'
                            )),
                        html.Div([

                            daq.ToggleSwitch(id='composition-option', label='Atomic Percent/Weight Percent',
                                             value=False), html.Br(),
                            html.Button('Submit Element/Isotope', id='submit-isotope-button', n_clicks_timestamp=0),
                            html.Div(id='isotope-message')
                        ],
                            style=dict(
                                display='table-cell',
                                verticalAlign="top",
                                width='30%'
                            )),
                        html.Div([
                            daq.NumericInput(
                                id='composition-percent',
                                min=0,
                                value=0,
                                label='Percent Composition',
                                labelPosition='top',
                                size=120
                            ),
                        ],
                            style=dict(
                                display='table-cell',
                                verticalAlign="top",
                                width='30%'
                            ))
                    ],
                        style=dict(
                            width='100%',
                            display='table',
                        )),
                ]),
                html.Div(id='xsection-graph')
            ],
                style=dict(
                    display='table-cell',
                    verticalAlign="top",
                    width='50%'
                ),
            ),
        ],
            style=dict(
                width='100%',
                display='table',
            ),
        ),
    ]),

])


#######################################################################################################################
# Materials Interface


# Populate Material Dropdown
@app.callback(
    Output('material-dropdown', 'options'),
    [Input('material-stores', 'data')],
)
def submit_material(material_data):
    material_options = []

    if material_data:
        for material_name in material_data.keys():
            material_options.append({'label': material_name, 'value': material_name})

    return material_options


# Inform User what element occupies selection
@app.callback(
    Output('chosen-element', 'children'),
    [Input('periodic-table', 'clickData')],
)
def choose_element(clickData):
    if clickData is not None:
        chosen_element = clickData['points'][0]['text'].split(':')[1].replace('<br>', ' ')
        element_mass = clickData['points'][0]['text'].split(':')[2]
        message = '{}, {} has been selected'.format(chosen_element, element_mass)
    else:
        message = 'Please choose element from periodic table'

    return html.P(message)


#######################################################################################################################
@app.callback(
    Output('xsection-graph', 'children'),
    [Input('periodic-table', 'clickData'),
     Input('atomic-mass', 'value')]
)
def graph_xsection(clickData, atomic_mass):
    chosen_element = clickData['points'][0]['text'].split(':')[0] if clickData else None
    element_mass = float(clickData['points'][0]['text'].split(':')[2]) if clickData else None

    if atomic_mass is None:
        atomic_mass = int(element_mass) if element_mass else None

    script_dir = os.path.dirname(__file__)
    xsection_path = os.path.join(script_dir, '../nndc_hdf5/cross_sections.xml')
    library = openmc.data.DataLibrary.from_xml(xsection_path)

    try:
        filename = library.get_by_material('{}{}'.format(chosen_element, atomic_mass))['path']
        u238_pointwise = openmc.data.IncidentNeutron.from_hdf5(filename)

        data = []
        # print(u238_pointwise.temperatures)
        for r in u238_pointwise.reactions.values():
            s = str(r)
            name = '({})'.format(s[s.find("(") + 1:s.find(")")])
            data.append(go.Scatter(x=r.xs['294K'].x,  # Can also use function data
                                   y=r.xs['294K'].y,
                                   name=name,
                                   text='Q-value: {}'.format(r.q_value)))

    except:
        data = []

    layout = go.Layout(
        xaxis=dict(
            type='log',
            autorange=True
        ),
        yaxis=dict(
            type='log',
            autorange=True
        )
    )

    figure = go.Figure(data=data, layout=layout)

    return dcc.Graph(figure=figure)


# Store Material and Isotope Data
@app.callback(
    Output('material-stores', 'data'),
    [Input('submit-material-button', 'n_clicks_timestamp'),
     Input('submit-isotope-button', 'n_clicks_timestamp')],

    [State('material-name', 'value'),
     State('material-density', 'value'),
     State('material-temperature', 'value'),

     State('material-dropdown', 'value'),
     State('periodic-table', 'clickData'),
     State('atomic-mass', 'value'),
     State('composition-option', 'value'),
     State('composition-percent', 'value'),
     State('material-stores', 'data')]
)
def submit_isotope(mat_click, iso_click, material_name, material_density, material_temperature, selected_material,
                   clickData, mass, composition_option, percent_composition, material_data):
    # material_data = material_data or {}
    material_data = material_data or {
        "Fuel": {
            "density": 10.29769,
            # "temperature": 1200,
            "elements": [
                "U",
                "U",
                "U",
                "O"
            ],
            "masses": [
                234,
                235,
                238,
                16
            ],
            "compositions": [
                .0000044843,
                .00055815,
                .022408,
                .045829
            ],
            "types": [
                "ao",
                "ao",
                "ao",
                "ao"
            ]
        },
        "Clad": {
            "density": 6.55,
            # "temperature": 900,
            "elements": [
                "Zr",
                "Zr",
                "Zr",
                "Zr",
                "Zr"
            ],
            "masses": [
                90,
                91,
                92,
                94,
                96
            ],
            "compositions": [
                .021827,
                .0047600,
                .0072758,
                .0073734,
                .0011879
            ],
            "types": [
                "ao",
                "ao",
                "ao",
                "ao",
                "ao"
            ]
        },
        "Water": {
            "density": 0.740582,
            # "temperature": 700,
            "elements": [
                "H",
                "O",
                "B",
                "B"
            ],
            "masses": [
                1,
                16,
                10,
                11
            ],
            "compositions": [
                .049457,
                .024672,
                .0000080042,
                .000032218
            ],
            "types": [
                "ao",
                "ao",
                "ao",
                "ao"
            ]
        },
    }

    trigger = dash.callback_context.triggered[0]
    if 'submit-material-button' in trigger['prop_id']:
        if None or '' in [material_name, material_density]:
            print('A Material Parameter remains Unfilled')
        else:
            material_data.update({'{}'.format(material_name):
                                      {'density': material_density,
                                       'temperature': material_temperature}
                                  })

        return material_data

    if 'submit-isotope-button' in trigger['prop_id']:
        chosen_element = clickData['points'][0]['text'].split(':')[0] if clickData else None
        element_mass = float(clickData['points'][0]['text'].split(':')[2]) if clickData else None

        mass = element_mass if mass is None else mass
        composition_type = 'wo' if composition_option is True else 'ao'

        if selected_material is None:
            print('A Material must be specified')
        elif percent_composition is None:
            print('A Composition percentage must be specified')
        else:
            print('{}-{} has been added to {} at {}% ({})'.format(mass,
                                                                      chosen_element,
                                                                      selected_material,
                                                                      percent_composition,
                                                                      composition_type))
        material = material_data[selected_material]

        try:
            elements = material_data[selected_material]['elements']
            masses = material_data[selected_material]['masses']
            compositions = material_data[selected_material]['compositions']
            types = material_data[selected_material]['types']
        except:
            elements = []
            masses = []
            compositions = []
            types = []

        elements.append(chosen_element)
        masses.append(mass)
        compositions.append(percent_composition)
        types.append(composition_type)

        material.update(
            {'elements': elements,
             'masses': masses,
             'compositions': compositions,
             'types': types}
        )

        return material_data


# Populate Table from Memory
@app.callback(
    Output('material-display', 'figure'),
    [Input('material-stores', 'modified_timestamp')],
    [State('material-stores', 'data')]
)
def tabulate_materials(timestamp, data):
    if timestamp is None:
        raise PreventUpdate

    df = pd.DataFrame.from_dict(data)
    df = df.reindex(['density', 'temperature', 'elements', 'masses', 'compositions', 'types'])
    # https://plot.ly/python/figure-factory/table/
    table = ff.create_table(df.reset_index())
    return table
