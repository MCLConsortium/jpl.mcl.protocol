# encoding: utf-8
# Copyright 2008—2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''EDRN Summarizer Service: interfaces
'''

from zope.interface import Interface
from zope.container.constraints import contains
from jpl.mcl.protocol import _
from plone.app.textfield import RichText
from zope import schema

class IGraphGenerator(Interface):
    '''An object that creates statement graphs.'''
    def generateGraph():
        '''Generate this object's Summarizer graph.'''

class IJsonGenerator(Interface):
    '''An object that creates json.'''
    def generateJson():
        '''Generate this object's Summarizer json.'''

class IAsserter(Interface):
    '''An object that describes subjects with a known predicate and a given object'''
    def characterize(obj):
        '''Characterize some subject using a known predicate for complementary ``obj``.  Returns a sequence of doubles
        containing a predicate URI (a URIRef) and an appropriate Literal or URIRef object.'''

class ISignature(Interface):
    '''An object that describes a signature'''
    name = schema.TextLine(
        title=_(u'Signature Name'),
        description=_(u'Name of this signature.'),
        required=True,
    )
    collections = schema.TextLine(
        title=_(u'List of Collections'),
        description=_(u'Collections associated with this signature.'),
        required=True,
    )
    type = schema.TextLine(
        title=_(u'Signature Type'),
        description=_(u'Signature type.'),
        required=False,
    )
    protocol = schema.TextLine(
        title=_(u'Protocol'),
        description=_(u'Protocols associated with this signature.'),
        required=False,
    )
    disease = schema.TextLine(
        title=_(u'Disease'),
        description=_(u'Disease associated with this signature.'),
        required=False,
    )
    species = schema.TextLine(
        title=_(u'Species'),
        description=_(u'Species associated with this signature.'),
        required=False,
    )
    status = schema.TextLine(
        title=_(u'Validation Status'),
        description=_(u'Validation status of this signature.'),
        required=False,
    )
    purpose = schema.TextLine(
        title=_(u'Clinical Purpose'),
        description=_(u'Clinical purpose of this signature.'),
        required=False,
    )
    evidence = schema.TextLine(
        title=_(u'Evidence Code'),
        description=_(u'Evidence Code of this signature.'),
        required=False,
    )
    specimen = schema.TextLine(
        title=_(u'Specimen'),
        description=_(u'Specimen associated with this signature.'),
        required=False,
    )
    registered = schema.Datetime(
        title=_(u'Registered Date'),
        description=_(u'Registered date of this signature.'),
        required=False,
    )

class IScience(Interface):
    '''An object that describes a Science Data'''
    collectionname = schema.TextLine(
        title=_(u'Collection Name'),
        description=_(u'Name of this collection.'),
        required=True,
    )
    description = schema.TextLine(
        title=_(u'Collection Description'),
        description=_(u'Description of this collection.'),
        required=False,
    )
    site = schema.TextLine(
        title=_(u'Participating Site'),
        description=_(u'Participating site for this collection.'),
        required=True,
    )
    organ = schema.TextLine(
        title=_(u'Organ'),
        description=_(u'Organ associated with this collection.'),
        required=False,
    )
    disease = schema.TextLine(
        title=_(u'Disease'),
        description=_(u'Disease of this collection.'),
        required=False,
    )
    imagedata = schema.TextLine(
        title=_(u'Image Data'),
        description=_(u'Image Data in this collection.'),
        required=False,
    )
    pathologydata= schema.TextLine(
        title=_(u'Pathology Data'),
        description=_(u'Pathology Data of this collection.'),
        required=False,
    )
    clinicaldata= schema.TextLine(
        title=_(u'Clinical Data'),
        description=_(u'Clinical Data of this collection.'),
        required=False,
    )
    genomicdata= schema.TextLine(
        title=_(u'Genomic Data'),
        description=_(u'Genomic Data of this collection.'),
        required=False,
    )
class IPerson(Interface):
    '''An object that describes a Person'''
    title = schema.TextLine(
        title=_(u'First Name'),
        description=_(u'First name of this person.'),
        required=True,
    )
    lastname = schema.TextLine(
        title=_(u'Last Name'),
        description=_(u'Last name of this person.'),
        required=True,
    )
    degree = schema.TextLine(
        title=_(u'Degrees'),
        description=_(u'Degress of this person.'),
        required=False,
    )
    institution = schema.TextLine(
        title=_(u'Institution'),
        description=_(u'Institution this person belong to.'),
        required=False,
    )
    email = schema.TextLine(
        title=_(u'Email'),
        description=_(u'Email of this person.'),
        required=False,
    )
    phone = schema.TextLine(
        title=_(u'Telephone'),
        description=_(u'Phone of this person.'),
        required=False,
    )

class IOrgan(Interface):
    '''An object that describes an Organ'''
class IFundedSite(Interface):
    '''An object that describes an Funded Site'''
    title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'Title of this funded site.'),
        required=True,
    )
    description = RichText(
        title=_(u'Description'),
        description=_(u'Description of this institution.'),
        required=True,
    )
    abstract = RichText(
        title=_(u'Abstract'),
        description=_(u'Abstract of this funded site.'),
        required=True,
    )
    organ = schema.TextLine(
        title=_(u'Organ'),
        description=_(u'Organs associated with this institutionn.'),
        required=True,
    )
    principalInvestigator = schema.TextLine(
        title=_(u'Principal Investigators'),
        description=_(u'Principal Investigators in this institution.'),
        required=True,
    )
    additionalStaff = schema.TextLine(
        title=_(u'Additional Staff'),
        description=_(u'Additional staff of this institution.'),
        required=True,
    )

class IInstitution(Interface):
    '''An object that describes an institution'''
    title = schema.TextLine(
        title=_(u'Name'),
        description=_(u'Name of this institution.'),
        required=True,
    )
    department = schema.TextLine(
        title=_(u'Department'),
        description=_(u'Department of this institution.'),
        required=True,
    )
    abbreviation = schema.TextLine(
        title=_(u'Abbreviation'),
        description=_(u'Abbreviation of the name of this project.'),
        required=True,
    )
    url = schema.TextLine(
        title=_(u'URL'),
        description=_(u'Web url of this institution.'),
        required=True,
    )
    description = RichText(
        title=_(u'Description'),
        description=_(u'Description of this institution.'),
        required=True,
    )

class IProject(Interface):
    '''An object that describes a Project'''
    title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'Title of this project.'),
        required=True,
    )
    abbreviation = schema.TextLine(
        title=_(u'Abbreviation'),
        description=_(u'Abbreviation of the name of this project.'),
        required=True,
    )
    description = RichText(
        title=_(u'Description'),
        description=_(u'A short summary of the project.'),
        required=False,
    )
    sites = schema.TextLine(
        title=_(u'Sites'),
        description=_(u'Sites associated with this project.'),
        required=True,
    )
    
class IPublication(Interface):
    '''An object that describes an Publication'''
    title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'Title of this resource.'),
        required=True,
    )
    description = RichText(
        title=_(u'Description'),
        description=_(u'A short summary of the resource.'),
        required=False,
    )
    journal = schema.TextLine(
        title=_(u'Journal'),
        description=_(u'Journal of this publication.'),
        required=False,
    )
    author = schema.TextLine(
        title=_(u'Author'),
        description=_(u'Author of this publication.'),
        required=False,
    )
    publicationdate= schema.Datetime(
        title=_(u'Publication Date'),
        description=_(u'Date of this publication.'),
        required=False,
    )
    pubmedid= schema.TextLine(
        title=_(u'Pubmed ID'),
        description=_(u'Pubmed ID of this publication.'),
        required=False,
    )

class IProtocolFolder(Interface):
    '''Study folder.'''
    contains('jpl.mcl.protocol.interfaces.IProtocol', 'jpl.mcl.protocol.interfaces.IProtocolFolder')
    title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'Descriptive name of this folder.'),
        required=True,
    )
    description = RichText(
        title=_(u'Description'),
        description=_(u'A short summary of this folder.'),
        required=False,
    )
    rdfDataSource = schema.TextLine(
        title=_(u'RDF Data Source'),
        description=_(u'URL to a source of Resource Description Format data that mandates the contents of this folder.'),
        required=False,
    )

class IProtocol(Interface):
    contains(
        'Products.ATContentTypes.interfaces.IATDocument',
        'Products.ATContentTypes.interfaces.IATFile',
        'Products.ATContentTypes.interfaces.IATImage',
    )
    '''Protocol.'''
    title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'Title of this resource.'),
        required=True,
    )
    description = RichText(
        title=_(u'Description'),
        description=_(u'A short summary of the resource.'),
        required=False,
    )
    identifier = schema.TextLine(
        title=_(u'Identifier'),
        description=_(u'The Uniform Resource Identifier identifying the resource.'),
        required=True,
    )
    organs = schema.TextLine(
        title=_(u'Organs'),
        description=_(u'Organs associated with this protocol.'),
        required=False,
#        schema=IOrgan
    )
    principleInvestigator = schema.TextLine(
        title=_(u'PIs'),
        description=_(u'Principle Investigator leading this protocol.'),
        required=False,
#        schema=IPerson
    )
    startDate = schema.Datetime(
        title=_(u'Start Date'),
        description=_(u'When this protocol began or will begin.'),
        required=False,
    )
    siteContact = schema.TextLine(
        title=_(u'Site Contact'),
        description=_(u'Site contact associated with this protocol.'),
        required=False,
    )
    irbApproval = schema.TextLine(
        title=_(u'IRB Approval'),
        description=_(u'A note about whether Internal Review Board approval is required, has been given, or has not been given.'),
        required=False,
    )
    irbNumber = schema.TextLine(
        title=_(u'IRB Approval #'),
        description=_(u'The approval identification number given to this protocol by the Internal Review Board.'),
        required=False,
    )
    irbContact = schema.TextLine(
        title=_(u'IRB Contact'),
        description=_(u'Contact in the Internal Review Board protocol.'),
        required=False,
    )
    irbContactEmail = schema.TextLine(
        title=_(u'IRB Contact Email'),
        description=_(u'Contact email in the Internal Review Board protocol.'),
        required=False,
    )
    humanSubjectTraining = schema.TextLine(
        title=_(u'Human Subject Training'),
        description=_(u'A note about whether human subject training is required, has been given, or has not been given.'),
        required=False,
    )
    abstract = RichText(
        title=_(u'Abstract'),
        description=_(u'A not-quite-as-brief summary.'),
        required=False
    )

