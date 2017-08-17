import itertools
import pandas as pd
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
    with open(snippetFileName, 'rb') as f, open(rootSnippetFileName, 'wb') as g:
        g.write('<div type="edition" xml:lang="san-Latn">{}</div>'.format(f.read()))
