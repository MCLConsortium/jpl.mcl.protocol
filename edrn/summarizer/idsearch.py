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
            newresponse['ensembl'] = hit['ensembl']['gene']
            newresponse['uniprot'] = hit['uniprot']['Swiss-Prot']
            pubmeds = []
            for dic in hit["generif"]:
                pubmeds.append(str(dic['pubmed']))
            newresponse['pubmed'] = ",".join(pubmeds)
            probeids = []
            for key in hit["reporter"].keys():
                if not isinstance(hit["reporter"][key], basestring):
                    hit["reporter"][key] = ",".join(hit["reporter"][key])
                if hit["reporter"][key].endswith("_at"):
                    probeids.append(hit["reporter"][key])
            newresponse['probe_id'] = ",".join(probeids)

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
        for key in packagedmygene.keys():
            if bdbresp[bdbMygeneMapping[key]] != "-":
                packagedmygene[key] = re.sub(r'\/\/+',',',bdbresp[bdbMygeneMapping[key]])

        return packagedmygene

    def render(self):
        if len(self.params) > 0:
            id = self.params[0]
            mygeneresults = self.queryMyGene(id)
            final_ids = self.packageMyGeneResp(mygeneresults)
            bdbresp = self.queryBioDBnet(id)
            
            if len(bdbresp.keys()) > 0:
                final_ids = self.replaceBDBwithMyGene(bdbresp, final_ids)

            #biomartresults = self.queryBiomart(id)    - disabled because biomart is currently under maintenance

            return final_ids
        else:
            return {'Error': "No query inputed. Please use idsearch/query to get info on your prospective id"}
