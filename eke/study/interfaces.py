# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''EKE Studies: interfaces.
'''

from eke.knowledge.interfaces import IKnowledgeFolder, IKnowledgeObject, IDisease
from eke.publications.interfaces import IPublication
from eke.site.interfaces import ISite
from eke.study import ProjectMessageFactory as _
from zope import schema
from zope.container.constraints import contains
from zope.interface import Interface

class IStudyFolder(IKnowledgeFolder):
    '''Study folder.'''
    contains('eke.study.interfaces.IProtocol', 'eke.study.interfaces.IStudyFolder')

# Pre-declare IProtocol since it's self-referential:
class IProtocol(IKnowledgeObject):
    pass

class IProtocol(IKnowledgeObject):
    contains(
        'Products.ATContentTypes.interfaces.IATDocument',
        'Products.ATContentTypes.interfaces.IATFile',
        'Products.ATContentTypes.interfaces.IATImage',
    )
    '''Protocol.'''
    abstract = schema.Text(
        title=_(u'Abstract'),
        description=_(u'A not-quite-as-brief summary.'),
        required=False
    )
    involvedInvestigatorSites = schema.List(
        title=_(u'Involved Involved Sites'),
        description=_(u'Sites at which the investigators are involved with this protocol.'),
        required=False,
        value_type=schema.Object(
            title=_(u'Involved Investigator Site'),
            description=_(u'Site at which the investigator is involved with this protocol.'),
            required=False,
            schema=ISite
        )
    )
    coordinatingInvestigatorSite = schema.Object(
        title=_(u'Coordinating Investigator Site'),
        description=_(u'Site at which the coordinating investigator is located.'),
        required=False,
        schema=ISite
    )
    leadInvestigatorSite = schema.Object(
        title=_(u'Lead Investigator Site'),
        description=_(u'Site at which you can find the investigator leading this protocol.'),
        required=False,
        schema=ISite
    )
    bmName = schema.TextLine(
        title=_(u'Biomarker Name'),
        description=_(u'A protocol may have associated with it a biomarker name, which turns out to be free text for anything.'),
        required=False
    )
    collaborativeGroupText = schema.Text(
        title=_(u'Collaborative Group Text'),
        description=_(u'Text explaining the collaborative nature of this protocol.'),
        required=False
    )
    phasedStatus = schema.TextLine(
        title=_(u'Phased Status'),
        description=_(u'Status of this protocol when phased through time and space.'),
        required=False
    )
    aims = schema.Text(
        title=_(u'Aims'),
        description=_(u'Purpose, intention, or desired outcomes of this protocol.'),
        required=False
    )
    analyticMethod = schema.Text(
        title=_(u'Analytic Method'),
        description=_(u'The method or methods used to analyze the protocol.'),
        required=False
    )
    blinding = schema.Text(
        title=_(u'Blinding'),
        description=_(u'How investigators were effectively blinded by various techniques to assure impartiality.'),
        required=False
    )
    cancerTypes = schema.List(
        title=_(u'Cancer Types'),
        description=_(u'What cancers this protocol is analyzing.'),
        required=False,
        value_type=schema.Object(
            title=_(u'Cancer Type'),
            description=_(u'A cancer this protocol is analyzing.'),
            schema=IDisease
        )
    )
    comments = schema.Text(
        title=_(u'Comments'),
        description=_(u'Any commentary from insightful to invective about this protocol.'),
        required=False,
    )
    dataSharingPlan = schema.Text(
        title=_(u'Data Sharing Plan'),
        description=_(u'Any plans on sharing data.'),
        required=False,
    )
    inSituDataSharingPlan = schema.Text(
        title=_(u'In Situ Data Sharing Plan'),
        description=_(u'The data sharing plan that is actually in place in the protocol.'),
        required=False,
    )
    startDate = schema.Datetime(
        title=_(u'Start Date'),
        description=_(u'When this protocol began or will begin.'),
        required=False,
    )
    estimatedFinishDate = schema.Datetime(
        title=_(u'Estimated Finish Date'),
        description=_(u'When this protocol is predicted to cease.'),
        required=False,
    )
    finishDate = schema.Datetime(
        title=_(u'Finish Date'),
        description=_(u'When this protocol actually ceased.'),
        required=False,
    )
    design = schema.TextLine(
        title=_(u'Design'),
        description=_(u'The design type of this protocol.'),
        required=False,
    )
    fieldOfResearch = schema.List(
        title=_(u'Fields of Research'),
        description=_(u'A list of numeric codes identifying what fields of research the protocol is pursuing.'),
        required=False,
        value_type=schema.Int(
            title=_(u'Field of Research Code'),
            description=_(u'A code identifying a single field of research.')
        )
    )
    abbrevName = schema.TextLine(
        title=_(u'Abbreviated Name'),
        description=_(u'A shorter and possibly far more convenient name for the protocol.'),
        required=False,
    )
    objective = schema.Text(
        title=_(u'Objective'),
        description=_(u'The thing aimed at or sought by this protocol.'),
        required=False,
    )
    project = schema.Bool(
        title=_(u'Project?'),
        description=_(u"True if this protocol actually a project, false if it's really a protocol."),
        required=False,
        default=False,
    )
    protocolType = schema.TextLine(
        title=_(u'Protocol Type'),
        description=_(u'The kind of protocol this is.'),
        required=False,
    )
    publications = schema.List(
        title=_(u'Publications'),
        description=_(u'What publications have been published about this protocol.'),
        required=False,
        value_type=schema.Object(
            title=_(u'Publication'),
            description=_(u'A single publication'),
            schema=IPublication
        )
    )
    outcome = schema.Text(
        title=_(u'Outcome'),
        description=_(u'The outcome (or expected outcome) of executing this protocol.'),
        required=False,
    )
    secureOutcome = schema.Text(
        title=_(u'Secure Outcome'),
        description=_(u'The secure outcome (or expected secure outcome) of executing this protocol.'),
        required=False,
    )
    plannedSampleSize = schema.TextLine(
        title=_(u'Planned Sample Size'),
        description=_(u'The size of the sample the protocol is expected to use.'),
        required=False,
    )
    finalSampleSize = schema.TextLine(
        title=_(u'Final Sample Size'),
        description=_(u'The size of the sample the protocol actually used.'),
        required=False,
    )
    isAPilotFor = schema.List(
        title=_(u'Piloting Protocol'),
        description=_(u'The protocols—if any—for which this protocol is a pilot.'),
        required=False,
        value_type=schema.Object(
            title=_(u'Piloting Protocol'),
            description=_(u'The protocol—if any—for which this protocol is a pilot.'),
            schema=IProtocol
        )
    )
    obtainsData = schema.List(
        title=_(u'Data Source Protocols'),
        description=_(u'The protocols—if any—from which this protocol obtains data.'),
        required=False,
        value_type=schema.Object(
            title=_(u'Data Source Protocol'),
            description=_(u'The protocol—if any—for which this protocol obtains data.'),
            schema=IProtocol
        )
    )
    providesData = schema.List(
        title=_(u'Data Sink Protocols'),
        description=_(u'The protocols—if any—to which this protocol provides data.'),
        required=False,
        value_type=schema.Object(
            title=_(u'Data Sink Protocol'),
            description=_(u'The protocol—if any—to which this protocol provides data.'),
            schema=IProtocol
        )
    )
    obtainsSpecimens = schema.List(
        title=_(u'Specimen Source Protocols'),
        description=_(u'The protocols—if any—from which this protocol obtains specimens.'),
        required=False,
        value_type=schema.Object(
            title=_(u'Specimen Source Protocol'),
            description=_(u'The protocol—if any—for which this protocol obtains specimens.'),
            schema=IProtocol
        )
    )
    providesSpecimens = schema.List(
        title=_(u'Specimen Sink Protocols'),
        description=_(u'The protocols—if any—to which this protocol provides specimens.'),
        required=False,
        value_type=schema.Object(
            title=_(u'Specimen Sink Protocol'),
            description=_(u'The protocol—if any—to which this protocol provides specimens.'),
            schema=IProtocol
        )
    )
    relatedProtocols = schema.List(
        title=_(u'Related Protocols'),
        description=_(u'The protocols—if any—to which this protocol has some relationship.'),
        required=False,
        value_type=schema.Object(
            title=_(u'Related Protocol'),
            description=_(u'The protocol—if any—to which this protocol has some relationship.'),
            schema=IProtocol
        )
    )
    animalSubjectTraining = schema.TextLine(
        title=_(u'Animal Subject Training'),
        description=_(u'A note about whether animal subject training is required, has been given, or has not been given.'),
        required=False,
    )
    humanSubjectTraining = schema.TextLine(
        title=_(u'Human Subject Training'),
        description=_(u'A note about whether human subject training is required, has been given, or has not been given.'),
        required=False,
    )
    irbApproval = schema.TextLine(
        title=_(u'IRB Approval'),
        description=_(u'A note about whether Internal Review Board approval is required, has been given, or has not been given.'),
        required=False,
    )
    originalIRBApprovalDate = schema.Datetime(
        title=_(u'Original IRB Approval Date'),
        description=_(u'The date on which the first, original IRB approval was given for this protocol.'),
        required=False,
    )
    currentIRBApprovalDate = schema.Datetime(
        title=_(u'Current IRB Approval Date'),
        description=_(u'The date on which the current IRB approval was given for this protocol.'),
        required=False,
    )
    currentIRBExpirationDate = schema.Datetime(
        title=_(u'Current IRB Expiration Date'),
        description=_(u'The date on which the current IRB approval will expire.'),
        required=False,
    )
    irbNotes = schema.Text(
        title=_(u'IRB Notes'),
        description=_(u'General notes about the Internal Review Board with regard to this protocol.'),
        required=False,
    )
    irbNumber = schema.TextLine(
        title=_(u'IRB Number'),
        description=_(u'The approval identification number given to this protocol by the Internal Review Board.'),
        required=False,
    )
    siteRoles = schema.List(
        title=_(u'Site Roles'),
        description=_(u'The roles the site plays in executing this protocol.'),
        required=False,
        value_type=schema.TextLine(
            title=_(u'Site Role'),
            description=_(u'The role the site plays in executing this protocol.')
        )
    )
    reportingStage = schema.TextLine(
        title=_(u'Reporting Stage'),
        description=_(u'Sequence of reporting for this protocol.'),
        required=False,
    )
    biomarkers = schema.List(
        title=_(u'Biomarkers'),
        description=_(u'Biomarkers being studied by this protocol.'),
        required=False,
        value_type=schema.Object(
            title=_(u'Biomarker'),
            description=_(u'A single biomarker being studied by this protocol.'),
            required=False,
            schema=Interface
        )
    )
    datasets = schema.List(
        title=_(u'Datasets'),
        description=_(u'Datasets generated by this protocol.'),
        required=False,
        value_type=schema.Object(
            title=_(u'Dataset'),
            description=_(u'A single dataset generated by this protocol.'),
            required=False,
            schema=Interface
        )
    )
    