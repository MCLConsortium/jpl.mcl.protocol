from plone.rest import Service
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse
from utils import csvToDict
import pickle, requests, os, urllib, re
import mygene, json

class IDSearch(Service):

    implements(IPublishTraverse)

    def __init__(self, context, request):
        super(IDSearch, self).__init__(context, request)
        self.params = []

    def publishTraverse(self, request, name):
        self.params.append(name)
        return self
    def queryMyGene(self, query):
        results = None
        #number of times to retry connecting to mygene
        retries = 0
        while True:
            try:
                mg = mygene.MyGeneInfo()
                results = mg.query(query, fields="symbol,ensembl.gene,pdb,reporter,generif.pubmed,uniprot.Swiss-Prot", species="human", size="1")
                break
            except requests.ConnectionError:
                #connection not working, retry
                retries += 1
                if retries < 5:
                    continue
                else:
                    print "MyGene not responding, try next symbol"
                    results = {}
                    results.pop("total",None)
                    results['info'] = "Not able to connect to mygene webservice"
                    break
        # check mygene
        if 'total' not in results:
            #debugging why total is not available in json
            results['success'] = False
            results['info'] = "No total in results for {}".format(query)
        else:
            results['success'] = True

        return results
    def packageMyGeneResp(self, response):
        newresponse = {}
        if response['success'] and response['total'] > 0:
            hit = response['hits'][0]
            newresponse['ensembl'] = [hit['ensembl']['gene']]
            newresponse['uniprot'] = [hit['uniprot']['Swiss-Prot']]
            pubmeds = []
            for dic in hit["generif"]:
                pubmeds.append(str(dic['pubmed']))
            newresponse['pubmed'] = pubmeds
            probeids = []
            for key in hit["reporter"].keys():
                if isinstance(hit["reporter"][key], basestring):
                    hit["reporter"][key] = [hit["reporter"][key]]
                for item in hit["reporter"][key]:
                    if item.endswith("_at"):
                        probeids.append(item)

            newresponse['probe_id'] = probeids
            newresponse['pdb'] = [hit['pdb']]
            newresponse['symbol'] = [hit['symbol']]

        return newresponse

    #pickle csv file into dictionaries so you don't have to create them everytime
    def pickleCSVDict(self, ifile, keycol, valcol, pickleExt):
      pickleref = ifile+pickleExt
      if os.path.isfile(pickleref):
        fref = open(pickleref, "rb")
        refDict = pickle.load(fref)
      else:
        refDict = csvToDict(ifile, keycol, valcol)
        pickle.dump(refDict, open(pickleref, "wb"))
      return refDict

    def getBiomartDicts(self):
        biomartfiles = ["pdb", "embl", "protein_id", "unigene", "uniprot_sptrembl", "uniprot_swissprot", "uniprot_genename", "uniparc", "hgnc_symbol"]

        dictionary = None
        biomartdicts = []
        biomartrevdicts = []
        for ifile in biomartfiles:
            dictionary = self.pickleCSVDict("edrn/summarizer/data/mart_"+ifile+".csv", 1, 0, ".pickle")
            biomartdicts.append(dictionary)
        for ifile in biomartfiles:
            dictionary = self.pickleCSVDict("edrn/summarizer/data/mart_"+ifile+".csv", 0, 1, ".rev.pickle")
            biomartrevdicts.append(dictionary)
        return biomartfiles, biomartdicts, biomartrevdicts    

    def queryBiomart(self, query):
        biomartfiles, biomartdicts, biomartrevdicts = self.getBiomartDicts()
        results = {}
        #check biomart
        for idx in range(0, len(biomartfiles)):
            if query in list(biomartdicts[idx].keys()):
                if biomartfiles[idx] not in results:
                  results[biomartfiles[idx]] = []
                results[biomartfiles[idx]] += biomartdicts[idx][query]
            if query in list(biomartrevdicts[idx].keys()):
                if "probeset_id" not in results:
                  results["probeset_id"] = []
                results["probeset_id"].append(biomartrevdicts[idx][query])
        return results
    def queryBioDBnet(self, query):
        biodbresp = {}
        #taxons can be used: human-9606
        url = 'http://biodbnet-abcc.ncifcrf.gov/webServices/rest.php/biodbnetRestApi.json'
        annotservice = '?method=db2db&format=row&input={}&inputValues={}&outputs={}&taxonId={}'
        typeservice = '?method=dbfind&inputValues={}&output=geneid&taxonId={}&format=row'
        taxon = "9606"
        output_types = 'genesymbol,ensemblgeneid,pdbid,affyid,pubmedid,uniprotaccession'
        types = urllib.urlopen(url+typeservice.format(query,taxon))
        typesresp = json.loads(types.read())
        querytype = ""
        if len(typesresp) > 0:
            if 'Input Type' in typesresp[0].keys():
                querytype = typesresp[0]['Input Type']

        if querytype != "":
            annot = urllib.urlopen(url+annotservice.format(querytype, query,output_types,taxon))
            annotresp = json.loads(annot.read())
            if len(annotresp) > 0:
                biodbresp = annotresp[0]
                
        return biodbresp

    def replaceBDBwithMyGene(self, bdbresp, packagedmygene):
        bdbMygeneMapping = {
                "symbol":"Gene Symbol",
                "ensembl":"Ensembl Gene ID",
                "pdb":"PDB ID",
                "probe_id":"Affy ID",
                "pubmed":"PubMed ID",
                "uniprot":"UniProt Accession"
            }
        for key in bdbMygeneMapping.keys():
            if bdbresp[bdbMygeneMapping[key]] != "-":
                packagedmygene[key] = re.compile(r'\/\/+').split(bdbresp[bdbMygeneMapping[key]])

        return packagedmygene

    def addLinkAnnotation(self, geneinfo):
        urlMapping = {
                "symbol":"http://www.genecards.org/cgi-bin/carddisp.pl?gene=",
                "ensembl":"http://uswest.ensembl.org/Homo_sapiens/Gene/Summary?g=",
                "pdb":"http://www.rcsb.org/pdb/explore.do?structureId=",
                "pubmed":"http://www.ncbi.nlm.nih.gov/pubmed/",
                "uniprot":"http://www.uniprot.org/uniprot/"
            }
        titleMapping = {
                "symbol":"GeneCards",
                "ensembl":"Ensembl",
                "pdb":"PDB",
                "pubmed":"PubMed",
                "uniprot":"Uniprot",
                "probe_id":"Probe ID"
            }
        newgeneinfo = {}
        for key in geneinfo.keys():

            newgeneinfo[key] = {}
            if key in titleMapping.keys():
                newgeneinfo[key]['Title'] = titleMapping[key]

            uriprefix = ""
            newgeneinfo[key]['Items'] = []
            if key in urlMapping.keys():
                uriprefix = urlMapping[key]
            for item in geneinfo[key]:
                newgeneinfo[key]['Items'].append(uriprefix + item)

        return newgeneinfo
            
    def render(self):
        if len(self.params) > 0:
            id = self.params[0]
            mygeneresults = self.queryMyGene(id)
            #biomartresults = self.queryBiomart(id)    - disabled because biomart is currently under maintenance
            tempids = self.packageMyGeneResp(mygeneresults)
            bdbresp = self.queryBioDBnet(id)
            
            if len(bdbresp.keys()) > 0:
                tempids = self.replaceBDBwithMyGene(bdbresp, tempids)

            final_ids = self.addLinkAnnotation(tempids)
            return final_ids

        else:
            return {'Error': "No query inputed. Please use idsearch/query to get info on your prospective id"}
