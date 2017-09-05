import itertools
import pandas as pd
import codecs
import xml.etree.ElementTree as ET
ET.register_namespace('', 'http://www.tei-c.org/ns/1.0')

# CSV Read
dfInscription = pd.read_csv('./metadata/inscription.csv', keep_default_na=False, encoding='utf8')
dfInscription.set_index('Inscription ID', inplace=True)

inscriptionIds = [x for x in list(dfInscription.loc['Inscription ID']) if len(x) > 0]

for inscriptionId in inscriptionIds:
    print(inscriptionId)
    snippetFileName = './snippets/' + inscriptionId + '.xml'
    rootSnippetFileName = './rootSnippets/' + inscriptionId + '.xml'
    with codecs.open(snippetFileName, 'rb') as f, codecs.open(rootSnippetFileName, 'w') as g:
        fileRead = f.read()
        # Remove BOM (zero-width non-breaking space) from start of snippetFile
        # https://stackoverflow.com/questions/8898294/convert-utf-8-with-bom-to-utf-8-with-no-bom-in-python#8898439
        fileReadDecode = fileRead.decode('utf-8-sig')
        fileReadEncode = fileReadDecode.encode('utf-8')
        output = '<div type="edition" xml:lang="san-Latn">\n{0}</div>'.format(fileReadEncode)
        g.write(output)
