import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.figure_factory as ff
from dash.dependencies import Output, State, Input
import plotly.graph_objs as go
import dash_daq as daq
import numpy as np
import pandas as pd
import json
from dash.exceptions import PreventUpdate

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
                                                          size=20,
                                                          color='black')))

        annotations.append(go.layout.Annotation(text=str(atomic_number[n][m]), x=x[m] + .3, y=y[n] + .3,
                                                xref='x1', yref='y1', showarrow=False,
                                                font=dict(family='Courier New',
                                                          size=15,
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
    width=1250,
    height=750,
    autosize=False
)

#######################################################################################################################

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([

    # Title
    html.H2('Materials Configuration',
            style={
                'position': 'relative',
                'top': '0px',
                'left': '10px',
                'font-family': 'Dosis',
                'display': 'inline',
                'font-size': '4.0rem',
                'color': '#4D637F'
            }),

    ################################################################################
    html.Br(),

    dcc.Store(id='material-stores', storage_type='session'),
    html.Div([
        dcc.Graph(id='periodic-table',
                  figure=periodic_table
                  ),
        html.Div(id='chosen-element'),
        html.H3("List of Materials"),
        dcc.Dropdown(id='material-dropdown'),
        html.H4("Add a Material"),
        html.P("""
            First, we need to create some materials with which we plan to fill our geometry. 
            Begin by entering the desired parameters and then submit the material to memory 
            once the parameters are acceptable. If a required parameter is unfilled, the material
            will not be submitted to memory and thus will not be added to the dropdown menu.
            The dropdown menu selector allows you to select previously submitted materials to view
            or make changes to subsequent parameters.  
               """),
        html.Div([dcc.Input(id='material-name', placeholder='Enter Material Name', type="text"),
                  dcc.Input(id='material-density', placeholder='Enter Material Density', type='number'),
                  dcc.Input(id='material-temperature', placeholder='Enter Material Temperature',
                            type='number'),  # TODO: Thermometer
                  html.Button('Submit Material', id='submit-material-button', n_clicks=0),
                  html.Br()
                  ]),
        html.H4("Add a Composition Constituent"),
        html.P("""
            Now that a material has been submitted, it is time to define its composition. You may make a 
            selection from the periodic table to define the element and then choose whether you would like 
            to make the composition entry based on atomic or weight %. If these fields are left blank, the 
            natural element will be selected from the periodic table with no alteration.
               """),
        # TODO: Add Snackbar here
        html.Div([dcc.Input(id='atomic-mass', placeholder='Enter Atomic Mass (if isotope)', type='number', size=70),
                  daq.ToggleSwitch(id='composition-option', label='Atomic Percent/Weight Percent', value=False),
                  dcc.Input(id='composition-percent', placeholder='Enter Composition Percent', type='number'),
                  html.Button('Submit Element/Isotope', id='submit-isotope-button', n_clicks=0)
                  ]),

        html.Div(id='isotope-message-update'),
        html.Div(style=dict(height=50)),

        html.Div(id='debug'),
        dcc.Graph(id='material-display')
    ]),

])


#######################################################################################################################
# Materials Interface


# Populate Material Dropdown
@app.callback(
    Output('material-dropdown', 'options'),
    [Input('submit-material-button', 'n_clicks')],
    [State('material-name', 'value'),
     State('material-density', 'value'),
     State('material-temperature', 'value'),
     State('material-dropdown', 'options')])
def submit_material(n_clicks, material_name, material_density, material_temperature, material_options):
    material_options = material_options or []
    if n_clicks > 0:
        if None in [material_name, material_density, material_temperature]:
            print(material_name, material_density, material_temperature)
            print("A Material Parameter remains Unfilled")
        elif material_name in [material_options[m]['value'] for m in range(len(material_options))]:
            print("A Material with that name already exists")
        else:
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
        message = '{} Atomic Mass {} has been selected'.format(chosen_element, element_mass)
    else:
        message = 'Please choose element from periodic table'

    return html.P(message)


#######################################################################################################################


# Submit material, element/isotope into memory
@app.callback(
    Output('material-stores', 'data'),
    [Input('submit-isotope-button', 'n_clicks')],
    [State('material-dropdown', 'value'),
     State('periodic-table', 'clickData'),
     State('atomic-mass', 'value'),
     State('composition-option', 'value'),
     State('composition-percent', 'value'),
     State('material-dropdown', 'options'),
     State('material-stores', 'data')]
)
def submit_isotope(n_clicks, selected_material, clickData, mass, composition_option, percent_composition,
                   material_options, data):
    if n_clicks is None:
        raise PreventUpdate

    chosen_element = clickData['points'][0]['text'].split(':')[0] if clickData else None
    element_mass = float(clickData['points'][0]['text'].split(':')[2]) if clickData else None

    if n_clicks > 0:
        mass = element_mass if mass is None else mass
        composition_type = 'weight' if composition_option is True else 'atom'

        if selected_material is None:
            message = 'A material must be specified'
        elif percent_composition is None:
            message = 'A Composition percentage must be specified'
        else:
            message = '{}-{} has been added to {} at {}% ({})'.format(mass,
                                                                      chosen_element,
                                                                      selected_material,
                                                                      percent_composition,
                                                                      composition_type)

        print(message)

        MATERIALS = data or {}

        for m in range(len(material_options)):
            if material_options[m]['value'] not in MATERIALS.keys():
                material = material_options[m]['value']
                MATERIALS.update({'{}'.format(material): {
                    'elements': [],
                    'masses': [],
                    'compositions': [],
                    'types': []}
                })

        if len(MATERIALS[selected_material]['elements']) > 0:
            MATERIALS[selected_material]['elements'].append(chosen_element)
        else:
            MATERIALS[selected_material]['elements'] = [chosen_element]

        if len(MATERIALS[selected_material]['masses']) > 0:
            MATERIALS[selected_material]['masses'].append(mass)
        else:
            MATERIALS[selected_material]['masses'] = [mass]

        if len(MATERIALS[selected_material]['compositions']) > 0:
            MATERIALS[selected_material]['compositions'].append(percent_composition)
        else:
            MATERIALS[selected_material]['compositions'] = [percent_composition]

        if len(MATERIALS[selected_material]['types']) > 0:
            MATERIALS[selected_material]['types'].append(composition_type)
        else:
            MATERIALS[selected_material]['types'] = [composition_type]

        return MATERIALS


# Populate Table from Memory - Must be able to recall material data from memory
@app.callback(
    Output('material-display', 'figure'),
    [Input('material-stores', 'modified_timestamp')],
    [State('material-stores', 'data')]
)
def tabulate_materials(timestamp, data):
    if timestamp is None:
        raise PreventUpdate

    print(json.dumps(data, indent=2))
    df = pd.DataFrame.from_dict(data)
    table = ff.create_table(df)
    return table


if __name__ == '__main__':
    app.run_server(debug=True)