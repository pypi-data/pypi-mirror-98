# This Python file uses the following encoding: utf-8

nutrientsTranslations = {
    'ac. grasos trans': 'Trans Fatty Acids',
    'ac. pantoténico':'Vitamin B5',
    'ac.pantoténico':'Vitamin B5',
    'acesulfame de potassio':'Acesulfame Potassium',
    'acesulfame de potasio':'Acesulfame Potassium',
    'acesulfamo de potasio':'Acesulfame Potassium',
    'acesulfano de potasio':'Acesulfame Potassium',
    'ácido fólico':'Vitamin B9',
    'ácido linoleico':'Linoleic Acid',
    'ácidos grasos omega 3 total':'Omega-3',
    'ácidos grasos omega 6 total':'Omega-6',
    'aspartamo':'Aspartame',
    'azúcar':'Sugar',
    'azúcar añadida':'Added Sugar',
    'azúcares de alcohol':'Sugar Alcohols',
    'azúcares totales':'Sugar',
    'cafeina':'Caffeine',
    'calcio':'Calcium',
    'colesterol':'Cholesterol',
    'dha':'DHA',
    'dha + epa':'DHA + EPA',
    'energía': 'Energy',
    'epa': 'EPA',
    'estevia':'Stevia',
    'fibra dietaria total':'Dietary fiber',
    'fibra dietética':'Dietary fiber',
    'fibra dietética total':'Dietary fiber',
    'fibra insoluble':'Insoluble fiber',
    'fibra soluble':'Soluble fiber',
    'grasas monoinsaturadas':'Monounsaturated Fats',
    'grasas polinsaturadas':'Polyunsaturated Fats',
    'grasas saturadas':'Saturated Fats',
    'grasas totales':'Fats',
    'hidratos de carbono disp.':'Carbohydrates',
    'hierro':'Iron',
    'l-carnitina l-tartrata':'L-carnitine L-tartrate',
    'lactosa':'Lactose',
    'magnesio':'Magnesium',
    'niacina':'Niacin',
    'omega 6':'Omega-6',
    'potasio':'Potassium',
    'proteínas':'Protein',
    'riboflavina':'Vitamin B2',
    'riboflavina b2':'Vitamin B2',
    'sacarosa':'Sucrose',
    'sodio':'Sodium',
    'sucralosa':'Sucralose',
    'taurina':'Taurine',
    'tiamina':'Vitamin B1',
    'tiamina b1':'Vitamin B1',
    'vit b5':'Vitamin B5',
    'vit b6':'Vitamin B6',
    'vit. b6':'Vitamin B6',
    'vit. b12':'Vitamin B12',
    'vit. b3':'Vitamin B3',
    'vitamina a':'Vitamin A',
    'vitamina b1':'Vitamin B1',
    'vitamina b12':'Vitamin B12',
    'vitamina b2':'Vitamin B2',
    'vitamina b3':'Vitamin B3',
    'vitamina b5':'Vitamin B5',
    'vitamina b6':'Vitamin B6',
    'vitamina b9 ácido fólico':'Vitamin B9',
    'vitamina c':'Vitamin C',
    'vitamina d':'Vitamin D',
    'zinc':'Zinc',
    }

def translate(term):
    return nutrientsTranslations[term.lower()]
        
def getSQLUpdates():
    queries = []
    for key in nutrientsTranslations:
        query = 'UPDATE moogliDB.Nutrients SET name="' + nutrientsTranslations[key] + '" WHERE name="' + key + '";'
        queries.append(query)
    with open('updateNutrients.sql', 'w') as filehandle:
        for query in queries:
            filehandle.write('%s\n' % query)
