import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd


# Read the Data sheet from the shapefile    
landuse = gpd.read_file("F:\\POLYU\\urban informatics\\Group\\data\\landuse_join.shp")
census = gpd.read_file("F:\\POLYU\\urban informatics\\Group\\data\\census_join_2.shp")


landuse_cat = {'Commercial & Office Buildings':0.16, 'Industrial & Manufacturing':0.09, 'Mixed Residential & Commercial Buildings':0.2, 'Multi-Family Elevator Buildings':0.15, 'Multi-Family Walk-up Buildings':0.12, 'One & Two Family Buildings':0.1, 'Open Space & Outdoor Recreation':0.05, 'Parking Facilities':0.05, 'Public Facilities & Institutions':0.05, 'Transportation & Utility':0.03, 'Vacant Land':0}
landuse_name = list(landuse_cat.keys())
Value = []
Landuse_value = []

for i in range(len(census.Geography)):
    landuse_all = landuse.loc[landuse.Geography == census.Geography[i], :]
    landuse_value = 0
    
    for j in landuse_name:
        landusetype = landuse_all.loc[landuse_all.LandUseCat == j, :]
        area = sum(landusetype.Shape_Area)
        areavalue = landuse_cat[j] * area
        landuse_value += areavalue
    
    Landuse_value.append(landuse_value)

    

for k in range(len(census.Geography)):

    max_landuse_value = max(Landuse_value)
    min_landuse_value = min(Landuse_value)
    max_population = max(census.TtlPop2010)
    min_population = min(census.TtlPop2010)
    pop = (census.TtlPop2010[k] - min_population) / (max_population - min_population)
    land = (Landuse_value[k] - min_landuse_value) / (max_landuse_value - min_landuse_value)
    value = 0.4 * round(float(pop) , 4) + 0.6 * round(float(land) , 4)
    Value.append(value)

census['Value'] = Value
census['Landuse_value'] = Landuse_value
census.to_file("F:\\POLYU\\urban informatics\\Group\\data\\census_value.shp")