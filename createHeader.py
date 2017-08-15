import pandas as pd
import xml.etree.ElementTree as ET


# XML
tree = ET.parse('epidocHeaderTemplate.xml')
root = tree.getroot()
# title = root.findall('.//title')

# CSV
dfInscription = pd.read_csv('inscription.csv', keep_default_na=False)
dfInscription.set_index('Inscription ID', inplace=True)
dfObject = pd.read_csv('object.csv', keep_default_na=False)
dfObject.set_index('Object ID', inplace=True)


inscriptionIds = list(dfInscription.loc['Inscription ID'])

for inscriptionId in inscriptionIds:

    inscriptionId = 'IN00004'
    objectId = dfInscription.loc['Parent Object'][inscriptionId]

    for tag in tree.iter():
         if type(tag.text) is str and len(tag.text) > 1:
             if tag.text[0:3] == '#IN':
                 csvMetadataField = tag.text[4:len(tag.text)-1]
                 csvMetadataCell = dfInscription.loc[csvMetadataField][inscriptionId]
                 tag.text = csvMetadataCell
             elif tag.text[0:3] == '#OB':
                 csvMetadataField = tag.text[4:len(tag.text)-1]
                 csvMetadataCell = dfObject.loc[csvMetadataField][objectId]
                 tag.text = csvMetadataCell

    if len(dfObject.loc['Child Objects'][objectId]):
        childObjectCell = dfObject.loc['Child Objects'][objectId]
        childObjects = cObj.split(',')
        # Iterate over childObjects and create msFRag templates.
        # Insert templates into msfrags tag in epidocHeaderTemplate 

    fileName = './headed/' + inscriptionId + '.xml'
    # tree.write(fileName)


# Read inscription columns
# dfInscription = pd.read_csv('inscription.csv', usecols=['IN00001'])
# print(dfInscription.iloc[0:1][0:1])

# # pretty string
# s = etree.tostring(root, pretty_print=True)
# print s
