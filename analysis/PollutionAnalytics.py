import pandas as pd
import matplotlib.pyplot as plt
from db import db

def GetDailyPollutionGraph(day, neighborhood):
    # Data Extraction
    statistics = db['CalidadAire']
    contaminants = db['Contaminantes']
    stations = db['Estaciones']

    stations = stations.find_one({"Nom_barri": neighborhood}, {"_id": 0, "Estacio": 1}).get("Estacio")
    if not stations:
        return None

    statistics = statistics.find({"ESTACIO": stations, "DIA": day})

    # Data Cleaning
    fieldsToRemove = [
        "_id",
        "CODI_PROVINCIA",
        "PROVINCIA",
        "CODI_MUNICIPI",
        "MUNICIPI",
        "ANY",
        "MES",
        "V12"
    ]

    statisticsDF = pd.DataFrame(list(statistics)).drop(columns=fieldsToRemove)
    statisticsDF["ESTACIO"] = neighborhood

    contaminantsDF = pd.DataFrame(contaminants.find())
    contaminantsDF.rename(columns={'Codi_Contaminant': 'CODI_CONTAMINANT'}, inplace=True)

    # Data Analysis
    statisticsDF = pd.merge(statisticsDF, contaminantsDF, on="CODI_CONTAMINANT").drop(columns=["_id"])

    # Data visualization
    try:
        plt.style.use('seaborn-darkgrid')
    except OSError as e:
        print(f"Error loading style: {e}")
        plt.style.use('ggplot')  # Usar un estilo alternativo

    plt.plot(statisticsDF["Desc_Contaminant"], statisticsDF['H12'], marker='o', linestyle='-', color='b', label='Pollution Level (H12)')

    plt.xlabel('Contaminant Name')
    plt.ylabel('Pollution Level (H12)')
    plt.title(f'Pollution Level by Contaminant, {neighborhood}, {day}')

    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("./static/dataVisualization/graphic.png", bbox_inches='tight', dpi=300)

    





    




