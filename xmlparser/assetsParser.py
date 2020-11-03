import pathlib

import xmltodict


def extract_directory(url):
    url = url.split('?download-url=')[1]
    url = url.lstrip()
    url = url.rstrip()
    url = '/'.join(url.split('/')[2:] if url.split('/')[0] == '' else url.split('/')[1:])
    url = ''.join(url.split('&name='))
    return '/'+url

def extract_filename(url):
    query = str(url.split('/')[-1]).split('&')
    for par in query:
        if 'name=' in par:
            return par.split('name=')[1]

def extract_filetype(filename):
        return filename.split('.')[-1]

class assetDocument():
    def __init__(self,assetURL,special=False):
        self.filename= extract_filename(url=assetURL) if not special else assetURL.split('/')[-1]
        self.directory = extract_directory(url=assetURL) if not special else assetURL
        self.filetype= extract_filetype(filename=self.filename)

    def __eq__(self, other):
        return self.filename == other.filename
    def __hash__(self):
        return hash(self.filename)

def parsemainstream(path):
    with open(str(pathlib.Path(path))) as fd:
        index = xmltodict.parse(fd.read())
    assets = []
    for item in index['root']['Message']:
        if item.get('String') and item.get('String') == 'setContentSo':
            try:
                urladd = item['Array']['Object']['newValue']['documentDescriptor']['downloadUrl']
                assert urladd,'empty urladd document'
            except:
                pass
            else:
                assets.append(
                    assetDocument(assetURL=urladd)
                )
                continue
            try:
                urladd = item['Array']['Object']['newValue']['documentDescriptor']['playbackFileNameHTMLClient']
                thename = item['Array']['Object']['newValue']['documentDescriptor']['theName']
                assert all([thename,urladd])
            except:
                continue
            else:
                assets.append(
                    assetDocument(assetURL=urladd+'default/'+thename,special=True)
                )

    return list(set(assets)) if assets else None