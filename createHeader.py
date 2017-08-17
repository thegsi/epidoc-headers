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
                 if len(csvMetadataCell) == 0 and tag.tag in ['measure']:
                     tag.text = 'not available'
                 else:
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
                    if cTag.text[0:3] == '#SO':
                        csvMetadataField = cTag.text[4:len(cTag.text)-1]
                        if len(csvMetadataCell) == 0 and cTag.tag not in ['measure', 'width', 'height', 'depth']:
                            csvMetadataCell = dfObject.loc[csvMetadataField][objectId]
                            cTag.text = csvMetadataCell
                        elif len(csvMetadataCell) == 0 and cTag.tag in ['measure']:
                            cTag.text = 'not available'
                        else:
                            csvMetadataCell = dfObject.loc[csvMetadataField][childObjectId]
                            cTag.text = csvMetadataCell

            # Insert templates into msdesc tag in epidocHeaderTemplate
            msDesc = headerRoot.findall('.//msDesc')[0]
            msDesc.append(childObjectRoot)

    teiHeader = headedRoot.findall('.//{http://www.tei-c.org/ns/1.0}teiHeader')[0]
    teiHeader.append(headerRoot)

    snippetFile = './rootSnippets/' + inscriptionId + '.xml'
    snippetTree = ET.parse(snippetFile)
    snippetRoot = snippetTree.getroot()
    teiText = headedRoot.findall('.//{http://www.tei-c.org/ns/1.0}body')[0]
    teiText.append(snippetRoot)

    fileName = './headed/' + inscriptionId + '.xml'
    headedTree.write(fileName, encoding='utf-8')

    headedFileName = './headed/' + inscriptionId + '.xml'
    declaredFileName = './declared/' + inscriptionId + '.xml'
    with open(headedFileName, 'rb') as f, open(declaredFileName, 'wb') as g:
        g.write('<?xml version="1.0" encoding="UTF-8"?>\n<?xml-model href="http://www.stoa.org/epidoc/schema/latest/tei-epidoc.rng" schematypens="http://relaxng.org/ns/structure/1.0"?>\n<?xml-model href="http://www.stoa.org/epidoc/schema/latest/tei-epidoc.rng" schematypens="http://purl.oclc.org/dsdl/schematron"?>\n{}'.format(f.read()))
