# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 00:49:19 2021

@author: rodbl
"""

# Plotly / Dash
import dash
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

# General
import numpy as np
import math
import pandas as pd
import datetime
import time
from datetime import datetime
import base64

# Sklearn
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

import os


######
# Data
######

#data = os.path.join(os.getcwd(),"1_insumos","master_data.xlsx")
#df = pd.read_excel(data, sheet_name='prev_1')

url = 'https://raw.githubusercontent.com/RBlasser/repos/master/master_data.csv'
df = pd.read_csv(url, error_bad_lines=False)
cols=["ID", "Tipo","Location","Baños", "dia","mes","año","Fecha","m2_const","$_m2","Precio","Cuartos","Titulo"]
df.columns = cols



df['m2_const'] = df['m2_const'].str.rstrip()
df['m2_const'] = df['m2_const'].str.lstrip()
df['m2_const'] = df['m2_const'].str.replace('"','')
df['m2_const'] = df['m2_const'].str.replace(',','')
df['m2_const'] = df['m2_const'].astype(float)


df['$_m2'] = df['$_m2'].str.rstrip()
df['$_m2'] = df['$_m2'].str.lstrip()
df['$_m2'] = df['$_m2'].str.replace('"','')
df['$_m2'] = df['$_m2'].str.replace(',','')
df['$_m2'] = df['$_m2'].astype(float)

df['Precio'] = df['Precio'].str.rstrip()
df['Precio'] = df['Precio'].str.lstrip()
df['Precio'] = df['Precio'].str.replace('"','')
df['Precio'] = df['Precio'].str.replace(',','')
df['Precio'] = df['Precio'].astype(float)

# Outlier
df = df[df['m2_const']<5000]


###########
# Subdata 1
###########
df1 = df.copy()
df1 = df1.groupby('Location')[['$_m2','m2_const']].median()
df1 = df1.reset_index()

# Outlier
df1 = df1[df1['m2_const']<1500]


########
# Inputs
########
input_types = ['Location','Tipo','Cuartos','Baños','Metraje']

#########
# Styles
########
#external_stylesheets = [dbc.themes.CYBORG]
#BS = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/cyborg/bootstrap.min.css"


# external CSS stylesheets
app = dash.Dash(__name__, title='Blasser Analytica')

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

# colors = {
#     'background': '#312B29',
#     'text': '#FFFFFF'
# }


####################
# Dropdown Locations
####################
ddbox = [{'label': '12 de Octubre', 'value': '12 de Octubre'},
{'label': '24 de Diciembre', 'value': '24 de Diciembre'},
{'label': 'Aguadulce', 'value': 'Aguadulce'},
{'label': 'Albrook', 'value': 'Albrook'},
{'label': 'Alcalde Diaz', 'value': 'Alcalde Diaz'},
{'label': 'Almirante', 'value': 'Almirante'},
{'label': 'Altamira', 'value': 'Altamira'},
{'label': 'Alto Boquete', 'value': 'Alto Boquete'},
{'label': 'Altos de Golf', 'value': 'Altos de Golf'},
{'label': 'Altos de Panama', 'value': 'Altos de Panama'},
{'label': 'Altos de Santa Maria', 'value': 'Altos de Santa Maria'},
{'label': 'Altos del Chase', 'value': 'Altos del Chase'},
{'label': 'Altos del Maria', 'value': 'Altos del Maria'},
{'label': 'Amador', 'value': 'Amador'},
{'label': 'Amador, Cause Way', 'value': 'Amador, Cause Way'},
{'label': 'Amelia Denis de Icaza', 'value': 'Amelia Denis de Icaza'},
{'label': 'Ancon', 'value': 'Ancon'},
{'label': 'Anton', 'value': 'Anton'},
{'label': 'Arnulfo Arias', 'value': 'Arnulfo Arias'},
{'label': 'Arosemena', 'value': 'Arosemena'},
{'label': 'Arraijan', 'value': 'Arraijan'},
{'label': 'Avenida Balboa', 'value': 'Avenida Balboa'},
{'label': 'Avenida Justo Arosemena', 'value': 'Avenida Justo Arosemena'},
{'label': 'Bajo Boquete', 'value': 'Bajo Boquete'},
{'label': 'Balboa', 'value': 'Balboa'},
{'label': 'Barrio Balboa', 'value': 'Barrio Balboa'},
{'label': 'Barrio Colon', 'value': 'Barrio Colon'},
{'label': 'Barrio Norte', 'value': 'Barrio Norte'},
{'label': 'Baru', 'value': 'Baru'},
{'label': 'Bejuco', 'value': 'Bejuco'},
{'label': 'Belisario Frias', 'value': 'Belisario Frias'},
{'label': 'Belisario Porras', 'value': 'Belisario Porras'},
{'label': 'Bella Vista', 'value': 'Bella Vista'},
{'label': 'Betania', 'value': 'Betania'},
{'label': 'Bocas del Toro Provincia', 'value': 'Bocas del Toro Provincia'},
{'label': 'Boqueron', 'value': 'Boqueron'},
{'label': 'Boquete', 'value': 'Boquete'},
{'label': 'Bosques de Cibeles', 'value': 'Bosques de Cibeles'},
{'label': 'Brisas del Golf', 'value': 'Brisas del Golf'},
{'label': 'Buena Vista', 'value': 'Buena Vista'},
{'label': 'Bugaba', 'value': 'Bugaba'},
{'label': 'Burunga', 'value': 'Burunga'},
{'label': 'Cabuya', 'value': 'Cabuya'},
{'label': 'Cacique', 'value': 'Cacique'},
{'label': 'Caldera', 'value': 'Caldera'},
{'label': 'Calidonia', 'value': 'Calidonia'},
{'label': 'Calle 50', 'value': 'Calle 50'},
{'label': 'Calobre', 'value': 'Calobre'},
{'label': 'Camino Real', 'value': 'Camino Real'},
{'label': 'Campana', 'value': 'Campana'},
{'label': 'Campo Alegre', 'value': 'Campo Alegre'},
{'label': 'Campo Limberg', 'value': 'Campo Limberg'},
{'label': 'Cañita', 'value': 'Cañita'},
{'label': 'Capira', 'value': 'Capira'},
{'label': 'Cardenas', 'value': 'Cardenas'},
{'label': 'Carrasquilla', 'value': 'Carrasquilla'},
{'label': 'Casco Viejo, San Felipe', 'value': 'Casco Viejo, San Felipe'},
{'label': 'Cativa', 'value': 'Cativa'},
{'label': 'Cermeño', 'value': 'Cermeño'},
{'label': 'Cerro Azul', 'value': 'Cerro Azul'},
{'label': 'Cerro Batea', 'value': 'Cerro Batea'},
{'label': 'Cerro Silvestre', 'value': 'Cerro Silvestre'},
{'label': 'Cerro Viento', 'value': 'Cerro Viento'},
{'label': 'Chame', 'value': 'Chame'},
{'label': 'Changuinola', 'value': 'Changuinola'},
{'label': 'Chanis', 'value': 'Chanis'},
{'label': 'Chepo', 'value': 'Chepo'},
{'label': 'Chica', 'value': 'Chica'},
{'label': 'Chilibre', 'value': 'Chilibre'},
{'label': 'Chiriqui', 'value': 'Chiriqui'},
{'label': 'Chiriqui Montañas', 'value': 'Chiriqui Montañas'},
{'label': 'Chiriqui Provincia', 'value': 'Chiriqui Provincia'},
{'label': 'Chitre', 'value': 'Chitre'},
{'label': 'Ciudad de Colon', 'value': 'Ciudad de Colon'},
{'label': 'Ciudad de Panama', 'value': 'Ciudad de Panama'},
{'label': 'Ciudad Radial', 'value': 'Ciudad Radial'},
{'label': 'Clayton', 'value': 'Clayton'},
{'label': 'Club de Golf', 'value': 'Club de Golf'},
{'label': 'Cochea', 'value': 'Cochea'},
{'label': 'Cocle', 'value': 'Cocle'},
{'label': 'Cocle Provincia', 'value': 'Cocle Provincia'},
{'label': 'Coco del Mar', 'value': 'Coco del Mar'},
{'label': 'Cocoli', 'value': 'Cocoli'},
{'label': 'Colinas del Golf', 'value': 'Colinas del Golf'},
{'label': 'Colon Provincia', 'value': 'Colon Provincia'},
{'label': 'Condado del Rey', 'value': 'Condado del Rey'},
{'label': 'Coronado', 'value': 'Coronado'},
{'label': 'Costa del Este', 'value': 'Costa del Este'},
{'label': 'Costa Sur', 'value': 'Costa Sur'},
{'label': 'Costa Verde', 'value': 'Costa Verde'},
{'label': 'Cristobal', 'value': 'Cristobal'},
{'label': 'David', 'value': 'David'},
{'label': 'Diablo', 'value': 'Diablo'},
{'label': 'Dolega', 'value': 'Dolega'},
{'label': 'Dorado Lake', 'value': 'Dorado Lake'},
{'label': 'Dorasol', 'value': 'Dorasol'},
{'label': 'Dos Mares', 'value': 'Dos Mares'},
{'label': 'Edison Park', 'value': 'Edison Park'},
{'label': 'El Arado', 'value': 'El Arado'},
{'label': 'El Bosque', 'value': 'El Bosque'},
{'label': 'El Cangrejo', 'value': 'El Cangrejo'},
{'label': 'El Carmen', 'value': 'El Carmen'},
{'label': 'El Chiru', 'value': 'El Chiru'},
{'label': 'El Cocal', 'value': 'El Cocal'},
{'label': 'El Coco', 'value': 'El Coco'},
{'label': 'El Cope', 'value': 'El Cope'},
{'label': 'El Crisol', 'value': 'El Crisol'},
{'label': 'El Dorado', 'value': 'El Dorado'},
{'label': 'El Doral', 'value': 'El Doral'},
{'label': 'El Espinal', 'value': 'El Espinal'},
{'label': 'El Espino', 'value': 'El Espino'},
{'label': 'El Farallon', 'value': 'El Farallon'},
{'label': 'El Higo', 'value': 'El Higo'},
{'label': 'El Ingenio', 'value': 'El Ingenio'},
{'label': 'El Muñoz', 'value': 'El Muñoz'},
{'label': 'El Palmar', 'value': 'El Palmar'},
{'label': 'El Roble', 'value': 'El Roble'},
{'label': 'El Valle', 'value': 'El Valle'},
{'label': 'Ernesto Cordoba Campos', 'value': 'Ernesto Cordoba Campos'},
{'label': 'Escobal', 'value': 'Escobal'},
{'label': 'Feuillet', 'value': 'Feuillet'},
{'label': 'Fuente del Fresno', 'value': 'Fuente del Fresno'},
{'label': 'Gamboa', 'value': 'Gamboa'},
{'label': 'Gatun', 'value': 'Gatun'},
{'label': 'Guadalupe', 'value': 'Guadalupe'},
{'label': 'Guarare', 'value': 'Guarare'},
{'label': 'Hato Pintado', 'value': 'Hato Pintado'},
{'label': 'Herrera', 'value': 'Herrera'},
{'label': 'Herrera Provincia', 'value': 'Herrera Provincia'},
{'label': 'Howard', 'value': 'Howard'},
{'label': 'Isla Bastimentos', 'value': 'Isla Bastimentos'},
{'label': 'Isla Boca Brava', 'value': 'Isla Boca Brava'},
{'label': 'Isla Contadora', 'value': 'Isla Contadora'},
{'label': 'Isla Cristobal', 'value': 'Isla Cristobal'},
{'label': 'Isla Grande', 'value': 'Isla Grande'},
{'label': 'Isla Pedro Gonzalez', 'value': 'Isla Pedro Gonzalez'},
{'label': 'Isla Saboga', 'value': 'Isla Saboga'},
{'label': 'Iturralde', 'value': 'Iturralde'},
{'label': 'Jaramillo', 'value': 'Jaramillo'},
{'label': 'Jose Domingo Espinar', 'value': 'Jose Domingo Espinar'},
{'label': 'Juan Demostenes', 'value': 'Juan Demostenes'},
{'label': 'Juan Diaz', 'value': 'Juan Diaz'},
{'label': 'La Alameda', 'value': 'La Alameda'},
{'label': 'La Castellana', 'value': 'La Castellana'},
{'label': 'La Chorrera', 'value': 'La Chorrera'},
{'label': 'La Colorada', 'value': 'La Colorada'},
{'label': 'La Cresta', 'value': 'La Cresta'},
{'label': 'La Ermita', 'value': 'La Ermita'},
{'label': 'La Exposicion', 'value': 'La Exposicion'},
{'label': 'La Laguna', 'value': 'La Laguna'},
{'label': 'La Lajas', 'value': 'La Lajas'},
{'label': 'La Loceria', 'value': 'La Loceria'},
{'label': 'La Loma', 'value': 'La Loma'},
{'label': 'La Pintada', 'value': 'La Pintada'},
{'label': 'La Represa', 'value': 'La Represa'},
{'label': 'La Villa de Los Santos', 'value': 'La Villa de Los Santos'},
{'label': 'Las Acacias', 'value': 'Las Acacias'},
{'label': 'Las Cruces', 'value': 'Las Cruces'},
{'label': 'Las Cumbres', 'value': 'Las Cumbres'},
{'label': 'Las Lajas', 'value': 'Las Lajas'},
{'label': 'Las Lomas', 'value': 'Las Lomas'},
{'label': 'Las Mañanitas', 'value': 'Las Mañanitas'},
{'label': 'Las Margaritas', 'value': 'Las Margaritas'},
{'label': 'Las Mercedes', 'value': 'Las Mercedes'},
{'label': 'Las Ollas Arriba', 'value': 'Las Ollas Arriba'},
{'label': 'Las Tablas', 'value': 'Las Tablas'},
{'label': 'Las Uvas', 'value': 'Las Uvas'},
{'label': 'Lidice', 'value': 'Lidice'},
{'label': 'Linda Vista', 'value': 'Linda Vista'},
{'label': 'Llano Bonito', 'value': 'Llano Bonito'},
{'label': 'Llano Grande', 'value': 'Llano Grande'},
{'label': 'Llanos de Curundu', 'value': 'Llanos de Curundu'},
{'label': 'Los Andes', 'value': 'Los Andes'},
{'label': 'Los Angeles', 'value': 'Los Angeles'},
{'label': 'Los Naranjos', 'value': 'Los Naranjos'},
{'label': 'Los Olivos', 'value': 'Los Olivos'},
{'label': 'Los Rios', 'value': 'Los Rios'},
{'label': 'Los Santos', 'value': 'Los Santos'},
{'label': 'Los Santos Provincia', 'value': 'Los Santos Provincia'},
{'label': 'Macaracas', 'value': 'Macaracas'},
{'label': 'Marbella', 'value': 'Marbella'},
{'label': 'Maria Chiquita', 'value': 'Maria Chiquita'},
{'label': 'Mariatos', 'value': 'Mariatos'},
{'label': 'Mateo Iturralde', 'value': 'Mateo Iturralde'},
{'label': 'Mendoza', 'value': 'Mendoza'},
{'label': 'Milla 8', 'value': 'Milla 8'},
{'label': 'Miraflores', 'value': 'Miraflores'},
{'label': 'Nata', 'value': 'Nata'},
{'label': 'Nueva Gorgona', 'value': 'Nueva Gorgona'},
{'label': 'Nuevo Belen', 'value': 'Nuevo Belen'},
{'label': 'Nuevo Emperador', 'value': 'Nuevo Emperador'},
{'label': 'Nuevo Tocumen', 'value': 'Nuevo Tocumen'},
{'label': 'Obarrio', 'value': 'Obarrio'},
{'label': 'Ocu', 'value': 'Ocu'},
{'label': 'Omar Torrijos', 'value': 'Omar Torrijos'},
{'label': 'Oria Arriba', 'value': 'Oria Arriba'},
{'label': 'Pacora', 'value': 'Pacora'},
{'label': 'Palmira', 'value': 'Palmira'},
{'label': 'Panama', 'value': 'Panama'},
{'label': 'Panama Oeste', 'value': 'Panama Oeste'},
{'label': 'Panama Pacifico', 'value': 'Panama Pacifico'},
{'label': 'Panama Provincia', 'value': 'Panama Provincia'},
{'label': 'Panama Viejo', 'value': 'Panama Viejo'},
{'label': 'Paraiso', 'value': 'Paraiso'},
{'label': 'Parita', 'value': 'Parita'},
{'label': 'Parque Lefevre', 'value': 'Parque Lefevre'},
{'label': 'Paseo del Valle', 'value': 'Paseo del Valle'},
{'label': 'Pedasi', 'value': 'Pedasi'},
{'label': 'Pedregal', 'value': 'Pedregal'},
{'label': 'Penonome', 'value': 'Penonome'},
{'label': 'Perejil', 'value': 'Perejil'},
{'label': 'Pese', 'value': 'Pese'},
{'label': 'Playa Barqueta', 'value': 'Playa Barqueta'},
{'label': 'Playa Coronado', 'value': 'Playa Coronado'},
{'label': 'Playa Gorgona', 'value': 'Playa Gorgona'},
{'label': 'Playa las Lajas', 'value': 'Playa las Lajas'},
{'label': 'Playa Leona', 'value': 'Playa Leona'},
{'label': 'Playa Malibu', 'value': 'Playa Malibu'},
{'label': 'Playas', 'value': 'Playas'},
{'label': 'Pocri', 'value': 'Pocri'},
{'label': 'Portobello', 'value': 'Portobello'},
{'label': 'Portobelo', 'value': 'Portobelo'},
{'label': 'Pueblo Nuevo', 'value': 'Pueblo Nuevo'},
{'label': 'Puerto Armuelles', 'value': 'Puerto Armuelles'},
{'label': 'Puerto Caimito', 'value': 'Puerto Caimito'},
{'label': 'Puerto Pilon', 'value': 'Puerto Pilon'},
{'label': 'Punta Chame', 'value': 'Punta Chame'},
{'label': 'Punta Pacifica', 'value': 'Punta Pacifica'},
{'label': 'Punta Paitilla', 'value': 'Punta Paitilla'},
{'label': 'Punto Barco', 'value': 'Punto Barco'},
{'label': 'Rancho Cafe', 'value': 'Rancho Cafe'},
{'label': 'Remedios', 'value': 'Remedios'},
{'label': 'Reparto Nuevo Panama', 'value': 'Reparto Nuevo Panama'},
{'label': 'Rio Abajo', 'value': 'Rio Abajo'},
{'label': 'Rio Grande', 'value': 'Rio Grande'},
{'label': 'Rio Hato', 'value': 'Rio Hato'},
{'label': 'Rodman', 'value': 'Rodman'},
{'label': 'Rufina Alfaro', 'value': 'Rufina Alfaro'},
{'label': 'Sabanitas', 'value': 'Sabanitas'},
{'label': 'Sajalices', 'value': 'Sajalices'},
{'label': 'San Antonio', 'value': 'San Antonio'},
{'label': 'San Carlos', 'value': 'San Carlos'},
{'label': 'San Francisco', 'value': 'San Francisco'},
{'label': 'San Gerardo de Mayela', 'value': 'San Gerardo de Mayela'},
{'label': 'San Isidro', 'value': 'San Isidro'},
{'label': 'San Jose', 'value': 'San Jose'},
{'label': 'San Juan', 'value': 'San Juan'},
{'label': 'San Martin', 'value': 'San Martin'},
{'label': 'San Miguelito', 'value': 'San Miguelito'},
{'label': 'San Pablo Nuevo', 'value': 'San Pablo Nuevo'},
{'label': 'San Pablo Viejo', 'value': 'San Pablo Viejo'},
{'label': 'Santa Ana', 'value': 'Santa Ana'},
{'label': 'Santa Clara', 'value': 'Santa Clara'},
{'label': 'Santa Librada', 'value': 'Santa Librada'},
{'label': 'Santa Maria', 'value': 'Santa Maria'},
{'label': 'Santa Rita', 'value': 'Santa Rita'},
{'label': 'Santa Rosa', 'value': 'Santa Rosa'},
{'label': 'Santiago', 'value': 'Santiago'},
{'label': 'Sona', 'value': 'Sona'},
{'label': 'Sora', 'value': 'Sora'},
{'label': 'Taboga', 'value': 'Taboga'},
{'label': 'Tocumen', 'value': 'Tocumen'},
{'label': 'Tonosi', 'value': 'Tonosi'},
{'label': 'Tulu', 'value': 'Tulu'},
{'label': 'Tumba Muerto', 'value': 'Tumba Muerto'},
{'label': 'Urbanizacion Don Bosco', 'value': 'Urbanizacion Don Bosco'},
{'label': 'Vacamonte', 'value': 'Vacamonte'},
{'label': 'Veracruz', 'value': 'Veracruz'},
{'label': 'Veraguas Provincia', 'value': 'Veraguas Provincia'},
{'label': 'Via Argentina', 'value': 'Via Argentina'},
{'label': 'Via Brasil', 'value': 'Via Brasil'},
{'label': 'Via Cincuentenario', 'value': 'Via Cincuentenario'},
{'label': 'Via España', 'value': 'Via España'},
{'label': 'Via Porras', 'value': 'Via Porras'},
{'label': 'Via Tocumen', 'value': 'Via Tocumen'},
{'label': 'Via Transistmica', 'value': 'Via Transistmica'},
{'label': 'Victoriano Lorenzo', 'value': 'Victoriano Lorenzo'},
{'label': 'Villa Belen', 'value': 'Villa Belen'},
{'label': 'Villa Caceres', 'value': 'Villa Caceres'},
{'label': 'Villa de las Fuentes', 'value': 'Villa de las Fuentes'},
{'label': 'Villa Lucre', 'value': 'Villa Lucre'},
{'label': 'Villa Rosario', 'value': 'Villa Rosario'},
{'label': 'Villa Zaita', 'value': 'Villa Zaita'},
{'label': 'Vista Alegre', 'value': 'Vista Alegre'},
{'label': 'Vista Hermosa', 'value': 'Vista Hermosa'},
{'label': 'Volcan', 'value': 'Volcan'},
{'label': '12 de Octubre', 'value': '12 de Octubre'},
{'label': '24 de Diciembre', 'value': '24 de Diciembre'},
{'label': 'Aguadulce', 'value': 'Aguadulce'},
{'label': 'Albrook', 'value': 'Albrook'},
{'label': 'Alcalde Diaz', 'value': 'Alcalde Diaz'},
{'label': 'Almirante', 'value': 'Almirante'},
{'label': 'Altamira', 'value': 'Altamira'},
{'label': 'Alto Boquete', 'value': 'Alto Boquete'},
{'label': 'Altos de Golf', 'value': 'Altos de Golf'},
{'label': 'Altos de Panama', 'value': 'Altos de Panama'},
{'label': 'Altos de Santa Maria', 'value': 'Altos de Santa Maria'},
{'label': 'Altos del Chase', 'value': 'Altos del Chase'},
{'label': 'Altos del Maria', 'value': 'Altos del Maria'},
{'label': 'Amador', 'value': 'Amador'},
{'label': 'Amador, Cause Way', 'value': 'Amador, Cause Way'},
{'label': 'Amelia Denis de Icaza', 'value': 'Amelia Denis de Icaza'},
{'label': 'Ancon', 'value': 'Ancon'},
{'label': 'Anton', 'value': 'Anton'},
{'label': 'Arnulfo Arias', 'value': 'Arnulfo Arias'},
{'label': 'Arosemena', 'value': 'Arosemena'},
{'label': 'Arraijan', 'value': 'Arraijan'},
{'label': 'Avenida Balboa', 'value': 'Avenida Balboa'},
{'label': 'Avenida Justo Arosemena', 'value': 'Avenida Justo Arosemena'},
{'label': 'Bajo Boquete', 'value': 'Bajo Boquete'},
{'label': 'Balboa', 'value': 'Balboa'},
{'label': 'Barrio Balboa', 'value': 'Barrio Balboa'},
{'label': 'Barrio Colon', 'value': 'Barrio Colon'},
{'label': 'Barrio Norte', 'value': 'Barrio Norte'},
{'label': 'Baru', 'value': 'Baru'},
{'label': 'Bejuco', 'value': 'Bejuco'},
{'label': 'Belisario Frias', 'value': 'Belisario Frias'},
{'label': 'Belisario Porras', 'value': 'Belisario Porras'},
{'label': 'Bella Vista', 'value': 'Bella Vista'},
{'label': 'Betania', 'value': 'Betania'},
{'label': 'Bocas del Toro Provincia', 'value': 'Bocas del Toro Provincia'},
{'label': 'Boqueron', 'value': 'Boqueron'},
{'label': 'Boquete', 'value': 'Boquete'},
{'label': 'Bosques de Cibeles', 'value': 'Bosques de Cibeles'},
{'label': 'Brisas del Golf', 'value': 'Brisas del Golf'},
{'label': 'Buena Vista', 'value': 'Buena Vista'},
{'label': 'Bugaba', 'value': 'Bugaba'},
{'label': 'Burunga', 'value': 'Burunga'},
{'label': 'Cabuya', 'value': 'Cabuya'},
{'label': 'Cacique', 'value': 'Cacique'},
{'label': 'Caldera', 'value': 'Caldera'},
{'label': 'Calidonia', 'value': 'Calidonia'},
{'label': 'Calle 50', 'value': 'Calle 50'},
{'label': 'Calobre', 'value': 'Calobre'},
{'label': 'Camino Real', 'value': 'Camino Real'},
{'label': 'Campana', 'value': 'Campana'},
{'label': 'Campo Alegre', 'value': 'Campo Alegre'},
{'label': 'Campo Limberg', 'value': 'Campo Limberg'},
{'label': 'Cañita', 'value': 'Cañita'},
{'label': 'Capira', 'value': 'Capira'},
{'label': 'Cardenas', 'value': 'Cardenas'},
{'label': 'Carrasquilla', 'value': 'Carrasquilla'},
{'label': 'Casco Viejo, San Felipe', 'value': 'Casco Viejo, San Felipe'},
{'label': 'Cativa', 'value': 'Cativa'},
{'label': 'Cermeño', 'value': 'Cermeño'},
{'label': 'Cerro Azul', 'value': 'Cerro Azul'},
{'label': 'Cerro Batea', 'value': 'Cerro Batea'},
{'label': 'Cerro Silvestre', 'value': 'Cerro Silvestre'},
{'label': 'Cerro Viento', 'value': 'Cerro Viento'},
{'label': 'Chame', 'value': 'Chame'},
{'label': 'Changuinola', 'value': 'Changuinola'},
{'label': 'Chanis', 'value': 'Chanis'},
{'label': 'Chepo', 'value': 'Chepo'},
{'label': 'Chica', 'value': 'Chica'},
{'label': 'Chilibre', 'value': 'Chilibre'},
{'label': 'Chiriqui', 'value': 'Chiriqui'},
{'label': 'Chiriqui Montañas', 'value': 'Chiriqui Montañas'},
{'label': 'Chiriqui Provincia', 'value': 'Chiriqui Provincia'},
{'label': 'Chitre', 'value': 'Chitre'},
{'label': 'Ciudad de Colon', 'value': 'Ciudad de Colon'},
{'label': 'Ciudad de Panama', 'value': 'Ciudad de Panama'},
{'label': 'Ciudad Radial', 'value': 'Ciudad Radial'},
{'label': 'Clayton', 'value': 'Clayton'},
{'label': 'Club de Golf', 'value': 'Club de Golf'},
{'label': 'Cochea', 'value': 'Cochea'},
{'label': 'Cocle', 'value': 'Cocle'},
{'label': 'Cocle Provincia', 'value': 'Cocle Provincia'},
{'label': 'Coco del Mar', 'value': 'Coco del Mar'},
{'label': 'Cocoli', 'value': 'Cocoli'},
{'label': 'Colinas del Golf', 'value': 'Colinas del Golf'},
{'label': 'Colon Provincia', 'value': 'Colon Provincia'},
{'label': 'Condado del Rey', 'value': 'Condado del Rey'},
{'label': 'Coronado', 'value': 'Coronado'},
{'label': 'Costa del Este', 'value': 'Costa del Este'},
{'label': 'Costa Sur', 'value': 'Costa Sur'},
{'label': 'Costa Verde', 'value': 'Costa Verde'},
{'label': 'Cristobal', 'value': 'Cristobal'},
{'label': 'David', 'value': 'David'},
{'label': 'Diablo', 'value': 'Diablo'},
{'label': 'Dolega', 'value': 'Dolega'},
{'label': 'Dorado Lake', 'value': 'Dorado Lake'},
{'label': 'Dorasol', 'value': 'Dorasol'},
{'label': 'Dos Mares', 'value': 'Dos Mares'},
{'label': 'Edison Park', 'value': 'Edison Park'},
{'label': 'El Arado', 'value': 'El Arado'},
{'label': 'El Bosque', 'value': 'El Bosque'},
{'label': 'El Cangrejo', 'value': 'El Cangrejo'},
{'label': 'El Carmen', 'value': 'El Carmen'},
{'label': 'El Chiru', 'value': 'El Chiru'},
{'label': 'El Cocal', 'value': 'El Cocal'},
{'label': 'El Coco', 'value': 'El Coco'},
{'label': 'El Cope', 'value': 'El Cope'},
{'label': 'El Crisol', 'value': 'El Crisol'},
{'label': 'El Dorado', 'value': 'El Dorado'},
{'label': 'El Doral', 'value': 'El Doral'},
{'label': 'El Espinal', 'value': 'El Espinal'},
{'label': 'El Espino', 'value': 'El Espino'},
{'label': 'El Farallon', 'value': 'El Farallon'},
{'label': 'El Higo', 'value': 'El Higo'},
{'label': 'El Ingenio', 'value': 'El Ingenio'},
{'label': 'El Muñoz', 'value': 'El Muñoz'},
{'label': 'El Palmar', 'value': 'El Palmar'},
{'label': 'El Roble', 'value': 'El Roble'},
{'label': 'El Valle', 'value': 'El Valle'},
{'label': 'Ernesto Cordoba Campos', 'value': 'Ernesto Cordoba Campos'},
{'label': 'Escobal', 'value': 'Escobal'},
{'label': 'Feuillet', 'value': 'Feuillet'},
{'label': 'Fuente del Fresno', 'value': 'Fuente del Fresno'},
{'label': 'Gamboa', 'value': 'Gamboa'},
{'label': 'Gatun', 'value': 'Gatun'},
{'label': 'Guadalupe', 'value': 'Guadalupe'},
{'label': 'Guarare', 'value': 'Guarare'},
{'label': 'Hato Pintado', 'value': 'Hato Pintado'},
{'label': 'Herrera', 'value': 'Herrera'},
{'label': 'Herrera Provincia', 'value': 'Herrera Provincia'},
{'label': 'Howard', 'value': 'Howard'},
{'label': 'Isla Bastimentos', 'value': 'Isla Bastimentos'},
{'label': 'Isla Boca Brava', 'value': 'Isla Boca Brava'},
{'label': 'Isla Contadora', 'value': 'Isla Contadora'},
{'label': 'Isla Cristobal', 'value': 'Isla Cristobal'},
{'label': 'Isla Grande', 'value': 'Isla Grande'},
{'label': 'Isla Pedro Gonzalez', 'value': 'Isla Pedro Gonzalez'},
{'label': 'Isla Saboga', 'value': 'Isla Saboga'},
{'label': 'Iturralde', 'value': 'Iturralde'},
{'label': 'Jaramillo', 'value': 'Jaramillo'},
{'label': 'Jose Domingo Espinar', 'value': 'Jose Domingo Espinar'},
{'label': 'Juan Demostenes', 'value': 'Juan Demostenes'},
{'label': 'Juan Diaz', 'value': 'Juan Diaz'},
{'label': 'La Alameda', 'value': 'La Alameda'},
{'label': 'La Castellana', 'value': 'La Castellana'},
{'label': 'La Chorrera', 'value': 'La Chorrera'},
{'label': 'La Colorada', 'value': 'La Colorada'},
{'label': 'La Cresta', 'value': 'La Cresta'},
{'label': 'La Ermita', 'value': 'La Ermita'},
{'label': 'La Exposicion', 'value': 'La Exposicion'},
{'label': 'La Laguna', 'value': 'La Laguna'},
{'label': 'La Lajas', 'value': 'La Lajas'},
{'label': 'La Loceria', 'value': 'La Loceria'},
{'label': 'La Loma', 'value': 'La Loma'},
{'label': 'La Pintada', 'value': 'La Pintada'},
{'label': 'La Represa', 'value': 'La Represa'},
{'label': 'La Villa de Los Santos', 'value': 'La Villa de Los Santos'},
{'label': 'Las Acacias', 'value': 'Las Acacias'},
{'label': 'Las Cruces', 'value': 'Las Cruces'},
{'label': 'Las Cumbres', 'value': 'Las Cumbres'},
{'label': 'Las Lajas', 'value': 'Las Lajas'},
{'label': 'Las Lomas', 'value': 'Las Lomas'},
{'label': 'Las Mañanitas', 'value': 'Las Mañanitas'},
{'label': 'Las Margaritas', 'value': 'Las Margaritas'},
{'label': 'Las Mercedes', 'value': 'Las Mercedes'},
{'label': 'Las Ollas Arriba', 'value': 'Las Ollas Arriba'},
{'label': 'Las Tablas', 'value': 'Las Tablas'},
{'label': 'Las Uvas', 'value': 'Las Uvas'},
{'label': 'Lidice', 'value': 'Lidice'},
{'label': 'Linda Vista', 'value': 'Linda Vista'},
{'label': 'Llano Bonito', 'value': 'Llano Bonito'},
{'label': 'Llano Grande', 'value': 'Llano Grande'},
{'label': 'Llanos de Curundu', 'value': 'Llanos de Curundu'},
{'label': 'Los Andes', 'value': 'Los Andes'},
{'label': 'Los Angeles', 'value': 'Los Angeles'},
{'label': 'Los Naranjos', 'value': 'Los Naranjos'},
{'label': 'Los Olivos', 'value': 'Los Olivos'},
{'label': 'Los Rios', 'value': 'Los Rios'},
{'label': 'Los Santos', 'value': 'Los Santos'},
{'label': 'Los Santos Provincia', 'value': 'Los Santos Provincia'},
{'label': 'Macaracas', 'value': 'Macaracas'},
{'label': 'Marbella', 'value': 'Marbella'},
{'label': 'Maria Chiquita', 'value': 'Maria Chiquita'},
{'label': 'Mariatos', 'value': 'Mariatos'},
{'label': 'Mateo Iturralde', 'value': 'Mateo Iturralde'},
{'label': 'Mendoza', 'value': 'Mendoza'},
{'label': 'Milla 8', 'value': 'Milla 8'},
{'label': 'Miraflores', 'value': 'Miraflores'},
{'label': 'Nata', 'value': 'Nata'},
{'label': 'Nueva Gorgona', 'value': 'Nueva Gorgona'},
{'label': 'Nuevo Belen', 'value': 'Nuevo Belen'},
{'label': 'Nuevo Emperador', 'value': 'Nuevo Emperador'},
{'label': 'Nuevo Tocumen', 'value': 'Nuevo Tocumen'},
{'label': 'Obarrio', 'value': 'Obarrio'},
{'label': 'Ocu', 'value': 'Ocu'},
{'label': 'Omar Torrijos', 'value': 'Omar Torrijos'},
{'label': 'Oria Arriba', 'value': 'Oria Arriba'},
{'label': 'Pacora', 'value': 'Pacora'},
{'label': 'Palmira', 'value': 'Palmira'},
{'label': 'Panama', 'value': 'Panama'},
{'label': 'Panama Oeste', 'value': 'Panama Oeste'},
{'label': 'Panama Pacifico', 'value': 'Panama Pacifico'},
{'label': 'Panama Provincia', 'value': 'Panama Provincia'},
{'label': 'Panama Viejo', 'value': 'Panama Viejo'},
{'label': 'Paraiso', 'value': 'Paraiso'},
{'label': 'Parita', 'value': 'Parita'},
{'label': 'Parque Lefevre', 'value': 'Parque Lefevre'},
{'label': 'Paseo del Valle', 'value': 'Paseo del Valle'},
{'label': 'Pedasi', 'value': 'Pedasi'},
{'label': 'Pedregal', 'value': 'Pedregal'},
{'label': 'Penonome', 'value': 'Penonome'},
{'label': 'Perejil', 'value': 'Perejil'},
{'label': 'Pese', 'value': 'Pese'},
{'label': 'Playa Barqueta', 'value': 'Playa Barqueta'},
{'label': 'Playa Coronado', 'value': 'Playa Coronado'},
{'label': 'Playa Gorgona', 'value': 'Playa Gorgona'},
{'label': 'Playa las Lajas', 'value': 'Playa las Lajas'},
{'label': 'Playa Leona', 'value': 'Playa Leona'},
{'label': 'Playa Malibu', 'value': 'Playa Malibu'},
{'label': 'Playas', 'value': 'Playas'},
{'label': 'Pocri', 'value': 'Pocri'},
{'label': 'Portobello', 'value': 'Portobello'},
{'label': 'Portobelo', 'value': 'Portobelo'},
{'label': 'Pueblo Nuevo', 'value': 'Pueblo Nuevo'},
{'label': 'Puerto Armuelles', 'value': 'Puerto Armuelles'},
{'label': 'Puerto Caimito', 'value': 'Puerto Caimito'},
{'label': 'Puerto Pilon', 'value': 'Puerto Pilon'},
{'label': 'Punta Chame', 'value': 'Punta Chame'},
{'label': 'Punta Pacifica', 'value': 'Punta Pacifica'},
{'label': 'Punta Paitilla', 'value': 'Punta Paitilla'},
{'label': 'Punto Barco', 'value': 'Punto Barco'},
{'label': 'Rancho Cafe', 'value': 'Rancho Cafe'},
{'label': 'Remedios', 'value': 'Remedios'},
{'label': 'Reparto Nuevo Panama', 'value': 'Reparto Nuevo Panama'},
{'label': 'Rio Abajo', 'value': 'Rio Abajo'},
{'label': 'Rio Grande', 'value': 'Rio Grande'},
{'label': 'Rio Hato', 'value': 'Rio Hato'},
{'label': 'Rodman', 'value': 'Rodman'},
{'label': 'Rufina Alfaro', 'value': 'Rufina Alfaro'},
{'label': 'Sabanitas', 'value': 'Sabanitas'},
{'label': 'Sajalices', 'value': 'Sajalices'},
{'label': 'San Antonio', 'value': 'San Antonio'},
{'label': 'San Carlos', 'value': 'San Carlos'},
{'label': 'San Francisco', 'value': 'San Francisco'},
{'label': 'San Gerardo de Mayela', 'value': 'San Gerardo de Mayela'},
{'label': 'San Isidro', 'value': 'San Isidro'},
{'label': 'San Jose', 'value': 'San Jose'},
{'label': 'San Juan', 'value': 'San Juan'},
{'label': 'San Martin', 'value': 'San Martin'},
{'label': 'San Miguelito', 'value': 'San Miguelito'},
{'label': 'San Pablo Nuevo', 'value': 'San Pablo Nuevo'},
{'label': 'San Pablo Viejo', 'value': 'San Pablo Viejo'},
{'label': 'Santa Ana', 'value': 'Santa Ana'},
{'label': 'Santa Clara', 'value': 'Santa Clara'},
{'label': 'Santa Librada', 'value': 'Santa Librada'},
{'label': 'Santa Maria', 'value': 'Santa Maria'},
{'label': 'Santa Rita', 'value': 'Santa Rita'},
{'label': 'Santa Rosa', 'value': 'Santa Rosa'},
{'label': 'Santiago', 'value': 'Santiago'},
{'label': 'Sona', 'value': 'Sona'},
{'label': 'Sora', 'value': 'Sora'},
{'label': 'Taboga', 'value': 'Taboga'},
{'label': 'Tocumen', 'value': 'Tocumen'},
{'label': 'Tonosi', 'value': 'Tonosi'},
{'label': 'Tulu', 'value': 'Tulu'},
{'label': 'Tumba Muerto', 'value': 'Tumba Muerto'},
{'label': 'Urbanizacion Don Bosco', 'value': 'Urbanizacion Don Bosco'},
{'label': 'Vacamonte', 'value': 'Vacamonte'},
{'label': 'Veracruz', 'value': 'Veracruz'},
{'label': 'Veraguas Provincia', 'value': 'Veraguas Provincia'},
{'label': 'Via Argentina', 'value': 'Via Argentina'},
{'label': 'Via Brasil', 'value': 'Via Brasil'},
{'label': 'Via Cincuentenario', 'value': 'Via Cincuentenario'},
{'label': 'Via España', 'value': 'Via España'},
{'label': 'Via Porras', 'value': 'Via Porras'},
{'label': 'Via Tocumen', 'value': 'Via Tocumen'},
{'label': 'Via Transistmica', 'value': 'Via Transistmica'},
{'label': 'Victoriano Lorenzo', 'value': 'Victoriano Lorenzo'},
{'label': 'Villa Belen', 'value': 'Villa Belen'},
{'label': 'Villa Caceres', 'value': 'Villa Caceres'},
{'label': 'Villa de las Fuentes', 'value': 'Villa de las Fuentes'},
{'label': 'Villa Lucre', 'value': 'Villa Lucre'},
{'label': 'Villa Rosario', 'value': 'Villa Rosario'},
{'label': 'Villa Zaita', 'value': 'Villa Zaita'},
{'label': 'Vista Alegre', 'value': 'Vista Alegre'},
{'label': 'Vista Hermosa', 'value': 'Vista Hermosa'},
{'label': 'Volcan', 'value': 'Volcan'}]


####################
# Dropdown Tipo
####################
ddbox2 = [{'label': 'Houses \00 \00 ', 'value': 'Casas'},
{'label': 'Apartaments', 'value': 'Apartamentos'}]

##################
# Images
#################
image_filename = './assets/banner.png' 
encoded_image = base64.b64encode(open(image_filename, 'rb').read())






########
# FIG 1
########

scatter1= px.scatter(df, x="m2_const", y="$_m2", 
                     color='Location',size='$_m2',
                     width=635, height=400,
                     template="plotly_dark",
                    title="Prices per Square Meter vs Total Square Meters <br>" +
                          "<i>Values per Property</i>")

# Transparent background
scatter1.update_layout({
                        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                        
                        })

########
# FIG 2
########
scatter2 = px.scatter(df1, x="m2_const", y="$_m2", 
                      color='Location',size='$_m2',
                      width=635, height=400,
                      template="plotly_dark",
                      title="Prices per Square Meter vs Total Square Meters <br>" +
                            "<i>Values expressed as median, by Location</i>")
# Transparent background
scatter2.update_layout({
                        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                        })
########
# FIG 3
########
gauge1 = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = 100,
        title = {'text': "Price per Square Meter"},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {'axis': {'range': [None, 4500]},
             'steps' : [
                 {'range': [0, 1000], 'color': "lightgray"},
                 {'range': [1000, 4500], 'color': "gray"}],
             'threshold' : {'line': {'color': "red", 'width': 3}, 'thickness': 0.75, 'value': 4100}}
        ))

# Transparent background
gauge1.update_layout({
                        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                        'width' : 400,
                        'height': 350,
                        'template':"plotly_dark"
                        
                        })
########
# FIG 4
########
gauge2 = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = 50000,
        title = {'text': "Property Reasonable Price"},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {'axis': {'range': [None, 7000000]},
             'steps' : [
                 {'range': [0, 1000000], 'color': "lightgray"},
                 {'range': [1000000, 5000000], 'color': "gray"}],
             'threshold' : {'line': {'color': "red", 'width': 3}, 'thickness': 0.75, 'value': 5000000}}
        ))


# Transparent background
gauge2.update_layout({
                        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                        'width' : 400,
                        'height': 350,
                        'template':"plotly_dark"
                        })

########
# FIG 5
########
hist1 = px.histogram(df, x="$_m2", nbins=10,                     
                     width=350, height=350,
                     template="plotly_dark",
                     title="Distribution: Prices per Square Meter")

# Transparent background
hist1.update_layout({
                        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                        'template':"plotly_dark"
                        })



#############
# Layout
#############
#'background-image': 'url("/assets/logo.png)'
# 'backgroundColor': colors['background']
# html.H1(children='Blasser Analytica'),
app.layout = html.Div(style={
                             'background-repeat': 'no-repeat',
                             'background-position': 'right top',
                             'background-image': 'url("/assets/logo_small.jpg")',
                             'height' : "100%",
                             'width' : "100%"
                             },
                      children=[
    
                          
    html.H3(style={'color': 'white'},children='Panama Real Estate Insights'),
    
    html.Div(html.P(['', html.Br(), ''])),
    
    html.Div([
            

        ]),


   html.Div([
       
    dcc.Graph(
    id='scatter-plot1',  style={'display': 'inline-block',"border":"0px black solid"},
    figure=scatter1),

    
   dcc.Graph(
    id='scatter-plot2', style={'display': 'inline-block',"border":"0px black solid"},
    figure=scatter2)
       ]),
   
   html.Hr(),
   
   html.H4(style={'color': 'white'},children='Predictive Model: Pricing'),
   
   
   dcc.Markdown('''
                
        This machine learning model is intended to return a reasonable price for your property,
         based on **real** market data. Some Locations might not have both Property Types.
        
       Please input the following parameters:
       
       *Property Type | Location | Number of Rooms | Number of Bathrooms | Total Construction Square Meters*
        '''),

   
   
   dbc.Row([dbc.Col([
           dcc.RadioItems(
           id='type-radio',
           options=ddbox2,
           value="Apartamentos",
           labelStyle={'display': 'inline-block'}),
           html.Div(id='dd2-output-container')
           ],width={'size': 2, "offset": 0, 'order': 1})
          
           ]),

   dbc.Row([dbc.Col([
           dcc.Dropdown(
           id='area-dropdown',
           options=ddbox,
           value="Costa del Este"),
           html.Div(id='dd-output-container')
           ],width={'size': 2, "offset": 0, 'order': 1}),
           
           dbc.Col([
            dcc.Slider(
            id='my-slider1',
            min=1,
            max=10,
            step=1,
            value=1),html.Div(id='slider-output-container1')
            ],width={'size': 3, "offset": 0, 'order': 1}),
           
           dbc.Col([
            dcc.Slider(
            id='my-slider2',
            min=1,
            max=10,
            step=0.5,
            value=1),html.Div(id='slider-output-container2')
            ],width={'size': 3, "offset": 0, 'order': 1}),
           
           dbc.Col([
            dcc.Slider(
            id='my-slider3',
            min=25,
            max=1200,
            step=0.25,
            value=25),html.Div(id='slider-output-container3')
            ],width={'size': 3, "offset": 0, 'order': 1}),
          
           ]),
   
   html.Div([
       dcc.Graph(
       id='gauge1',  style={'display': 'inline-block',"border":"0px black solid"},
       figure=gauge1),
        
       dcc.Graph(
       id='gauge2',  style={'display': 'inline-block',"border":"0px black solid"},
       figure=gauge2),
       
       dcc.Graph(
       id='hist1',  style={'display': 'inline-block',"border":"0px black solid"},
       figure=hist1)  
       
           ])
       
   
   
   ])

# color="#9B51E0",
######################
# Functions Pred / VaR
######################

# Location = "24 de Diciembre"
# Tipo = "Apartamentos"
# Cuartos = str(2)
# Baños = str(2)
# Metraje = str(200)


def predict(Location,Tipo,Cuartos,Baños,Metraje):
    start = time.time()
    
    # Filter
    dfi = df.copy()
    dfi['Fecha'] = pd.to_datetime(dfi['Fecha'])
    dfi['Dias_publicado'] = (dfi['Fecha'] - datetime.today()).dt.days
    dfi = dfi[(dfi["Location"] == Location)&(dfi['Tipo']==Tipo)]
    dfi = dfi.reindex(columns=['Baños','Cuartos','m2_const','Dias_publicado','$_m2'])
    
    # Reshape
    X = dfi.iloc[:, :-1].values
    y = dfi.iloc[:, -1].values


    # Split 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
    
    
    # Regression
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    y_pred = regressor.predict(X_test)
    np.set_printoptions(precision=2)
    
    # Prediction
    Baños = float(Baños)
    Cuartos = int(Cuartos)
    Metraje = float(Metraje)
    Dias = 0 ## Dias de publicacion
    
    m2 = round(regressor.predict([[Baños,Cuartos,Metraje,Dias]])[0],2)
    total = round(regressor.predict([[Baños,Cuartos,Metraje,Dias]])[0]*Metraje,2)
    
    end = time.time()
    time_= str(round(end - start,2)) + " segundos."
    
    done = str(m2) + ":" + str(total)
    
    return done



###################
# Call Backs Form
##################

# Cuartos
@app.callback(
    dash.dependencies.Output('slider-output-container1', 'children'),
    [dash.dependencies.Input('my-slider1', 'value')])
def update_output1(value):
    return 'You have selected {} room(s)'.format(value)

# Baños
@app.callback(
    dash.dependencies.Output('slider-output-container2', 'children'),
    [dash.dependencies.Input('my-slider2', 'value')])
def update_output2(value):
    return 'You have selected {} bathroom(s)'.format(value)

# Metraje
@app.callback(
    dash.dependencies.Output('slider-output-container3', 'children'),
    [dash.dependencies.Input('my-slider3', 'value')])
def update_output3(value):
    return 'You have selected {} square meters'.format(value)


######################
# Call Backs Functions
######################
@app.callback(
    dash.dependencies.Output('gauge1', 'figure'),
    [dash.dependencies.Input('area-dropdown', 'value')],
    [dash.dependencies.Input('type-radio', 'value')],
    [dash.dependencies.Input('my-slider1', 'value')],
    [dash.dependencies.Input('my-slider2', 'value')],
    [dash.dependencies.Input('my-slider3', 'value')])
 

# Prediction Gauge 1
def update_output(Location,Tipo,Cuartos,Baños,Metraje):
    filtered_data = df[(df['Location']==Location) & (df['Tipo']==Tipo)]
    if filtered_data.shape[0] < 10:
        raise PreventUpdate
        
    else:
        done = predict(Location,Tipo,Cuartos,Baños,Metraje)
        done = float(done.split(":")[0])
        
        gauge1 = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = done,
                title = {'text': "Price per Square Meter"},
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {'axis': {'range': [None, 4500]},
                     'steps' : [
                         {'range': [0, 1000], 'color': "lightgray"},
                         {'range': [1000, 4500], 'color': "gray"}],
                     'threshold' : {'line': {'color': "red", 'width': 3}, 'thickness': 0.75, 'value': 4100}}
                ))
        
        # Transparent background
        gauge1.update_layout({
                                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                'width' : 400,
                                'height': 350,
                                'template':"plotly_dark"
                                
                                })   
    
        return gauge1


@app.callback(
    dash.dependencies.Output('gauge2', 'figure'),
    [dash.dependencies.Input('area-dropdown', 'value')],
    [dash.dependencies.Input('type-radio', 'value')],
    [dash.dependencies.Input('my-slider1', 'value')],
    [dash.dependencies.Input('my-slider2', 'value')],
    [dash.dependencies.Input('my-slider3', 'value')])
# Prediction Gauge 2
def update_output(Location,Tipo,Cuartos,Baños,Metraje):
    filtered_data = df[(df['Location']==Location) & (df['Tipo']==Tipo)]
    if filtered_data.shape[0] < 10:
        raise PreventUpdate   
        
    else:
        done = predict(Location,Tipo,Cuartos,Baños,Metraje)
        done = float(done.split(":")[1])
        
        gauge2 = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = done,
                title = {'text': "Property Reasonable Price"},
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {'axis': {'range': [None, 7000000]},
                     'steps' : [
                         {'range': [0, 1000000], 'color': "lightgray"},
                         {'range': [1000000, 5000000], 'color': "gray"}],
                     'threshold' : {'line': {'color': "red", 'width': 3}, 'thickness': 0.75, 'value': 5000000}}
                ))
        
        
        # Transparent background
        gauge2.update_layout({
                                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                'width' : 400,
                                'height': 350,
                                'template':"plotly_dark"
                                })
    
        return gauge2


# Refresn Distribution Chart Pred
@app.callback(
    dash.dependencies.Output('hist1', 'figure'),
    [dash.dependencies.Input('area-dropdown', 'value')],
    [dash.dependencies.Input('type-radio', 'value')]
    )


def update_output(value1,value2):
    filtered_data = df[(df['Location']==value1) & (df['Tipo']==value2)]
    dict_ = {"Apartamentos" :"Apartments","Casas":"Houses"}
    hist1 = px.histogram(filtered_data, x="$_m2", nbins=10,                     
                         width=350, height=350,
                         template="plotly_dark",
                         title="Distribution: Prices per Square Meter<br>" +
                               "<i>{} in {}</i>".format(dict_[value2],value1))
    
    hist1.update_layout({
                            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                            'template':"plotly_dark"
                            })
    
    
    return hist1



if __name__ == '__main__':
    app.run_server(host= '0.0.0.0',debug=True)





