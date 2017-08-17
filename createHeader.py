import pandas as pd
import xml.etree.ElementTree as ET
ET.register_namespace('', 'http://www.tei-c.org/ns/1.0')

# CSV Read
dfInscription = pd.read_csv('./metadata/inscription.csv', keep_default_na=False, encoding='utf8')
dfInscription.set_index('Inscription ID', inplace=True)
dfObject = pd.read_csv('./metadata/object.csv', keep_default_na=False, encoding='utf8')
dfObject.set_index('Object ID', inplace=True)

inscriptionIds = [x for x in list(dfInscription.loc['Inscription ID']) if len(x) > 0]

for inscriptionId in inscriptionIds:
    # XML Read
    headedTree = ET.parse('./templates/epidoc.xml')
    headedRoot = headedTree.getroot()

    headerTree = ET.parse('./templates/header.xml')
    headerRoot = headerTree.getroot()

    inscriptionId = inscriptionId.encode('ascii')
    objectId = dfInscription.loc['Parent Object'][inscriptionId]

    for tag in headerTree.iter():
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
        childObjects = childObjectCell.split(',')

        # Iterate over childObjects and create msFRag templates.
        for c in childObjects:
            childObjectId = c.encode('ascii').strip()
            childObjectTree = ET.parse('./templates/msFrag.xml')
            childObjectRoot = childObjectTree.getroot()

            for cTag in childObjectTree.iter():
                if type(cTag.text) is str and len(cTag.text) > 1:
                    if cTag.text[0:3] == '#IN':
                        csvMetadataField = cTag.text[4:len(cTag.text)-1]
                        csvMetadataCell = dfInscription.loc[csvMetadataField][inscriptionId]
                        cTag.text = csvMetadataCell
                    if cTag.text[0:3] == '#OB':
                        csvMetadataField = cTag.text[4:len(cTag.text)-1]
                        csvMetadataCell = dfObject.loc[csvMetadataField][childObjectId]
                        cTag.text = csvMetadataCell

            # Insert templates into msfrags tag in epidocHeaderTemplate
            msfrags = headerRoot.findall('.//msFrags')[0]
            print(childObjectId)
            msfrags.append(childObjectRoot)

    # print(headerRoot.findall('.//title')[0].text)
    # print(inscriptionId)
    # print(objectId)

    teiHeader = headedRoot.findall('.//{http://www.tei-c.org/ns/1.0}teiHeader')[0]
    teiHeader.append(headerRoot)

    snippetFile = './rootSnippets/' + inscriptionId + '.xml'
    snippetTree = ET.parse(snippetFile)
    snippetRoot = snippetTree.getroot()
    teiText = headedRoot.findall('.//{http://www.tei-c.org/ns/1.0}body')[0]
    teiText.append(snippetRoot)

    fileName = './headed/' + inscriptionId + '.xml'
    headedTree.write(fileName)
