# encoding: utf-8
# Copyright 2009-2010 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''EKE Studies: Protocol.'''

from eke.knowledge import dublincore
from eke.knowledge.browser.utils import MarkupFilterer
from eke.knowledge.content import knowledgeobject
from eke.knowledge.interfaces import IDisease
from eke.publications.interfaces import IPublication
from eke.site.interfaces import ISite
from eke.study import ProjectMessageFactory as _
from eke.study.config import PROJECTNAME
from eke.study.interfaces import IProtocol
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.schemata import NextPreviousAwareSchema
from Products.ATContentTypes.lib.constraintypes import ConstrainTypesMixinSchema
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from zope.interface import implements, directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

# Maximum number of protocols that we'll allow to all have the same title.
MAX_PROTOCOL_INDEX = 100

# To support CA-586, we'll make "description" a computed field whose value comes from
# the abstract, objectives, aims, or results outcome.
ProtocolSchema = knowledgeobject.KnowledgeObjectSchema.copy() + ConstrainTypesMixinSchema.copy() + NextPreviousAwareSchema.copy()
del ProtocolSchema['description']
ProtocolSchema += atapi.Schema((
    atapi.ComputedField(
        'description',
        accessor='Description',
        allowable_content_types=('text/plain',),
        default=u'',
        default_content_type='text/plain',
        expression='context._computeDescription()',
        searchable=True,
        widget=atapi.ComputedWidget(
            visible={'edit': 'invisible', 'view': 'invisible'},
        ),
    ),
    atapi.TextField(
        'abstract',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.TextAreaWidget(
            label=_(u'Abstract'),
            description=_(u'A not-quite-as-brief summary.'),
        ),
        predicateURI='http://purl.org/dc/terms/description',
    ),
    atapi.ReferenceField(
        'involvedInvestigatorSites',
        enforceVocabulary=True,
        multiValued=True,
        relationship='involvedInvestigatorSitesForProtocol',
        required=False,
        storage=atapi.AnnotationStorage(),
        vocabulary_factory=u'eke.site.Sites',
        vocabulary_display_path_bound=-1,
        widget=atapi.ReferenceWidget(
            label=_(u'Involved Investigator Site'),
            description=_(u'Sites at which the investigators are involved with this protocol.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#involvedInvestigatorSite',
        predicateTarget=ISite,
    ),
    atapi.ReferenceField(
        'coordinatingInvestigatorSite',
        enforceVocabulary=True,
        multiValued=False,
        relationship='coordinatingInvestigatorSiteForProtocol',
        required=False,
        storage=atapi.AnnotationStorage(),
        vocabulary_factory=u'eke.site.Sites',
        vocabulary_display_path_bound=-1,
        widget=atapi.ReferenceWidget(
            label=_(u'Coordinating Investigator Site'),
            description=_(u'Site at which the coordinating investigator is located.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#coordinatingInvestigatorSite',
        predicateTarget=ISite,
    ),
    atapi.ReferenceField(
        'leadInvestigatorSite',
        enforceVocabulary=True,
        multiValued=False,
        relationship='leadInvestigatorSiteForProtocol',
        required=False,
        storage=atapi.AnnotationStorage(),
        vocabulary_factory=u'eke.site.Sites',
        vocabulary_display_path_bound=-1,
        widget=atapi.ReferenceWidget(
            label=_(u'Lead Investigator Site'),
            description=_(u'Site at which you can find the investigator leading this protocol.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#leadInvestigatorSite',
        predicateTarget=ISite,
    ),
    atapi.StringField(
        'bmName',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Biomarker Name'),
            description=_(u'Biomarker name, which turns out to be free text for anything.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#bmName',
    ),
    atapi.TextField(
        'collaborativeGroupText',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.TextAreaWidget(
            label=_(u'Collaborative Group Text'),
            description=_(u'Text explaining the collaborative nature of this protocol.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#collaborativeGroupText',
    ),
    atapi.StringField(
        'phasedStatus',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.StringWidget(
            label=_(u'Phased Status'),
            description=_(u'Status of this protocol when phased through time and space.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#phasedStatus',
    ),
    atapi.TextField(
        'aims',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.TextAreaWidget(
            label=_(u'Aims'),
            description=_(u'Purpose, intention, or desired outcomes of this protocol.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#aims',
    ),
    atapi.TextField(
        'analyticMethod',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.TextAreaWidget(
            label=_(u'Analytic Method'),
            description=_(u'The method or methods used to analyze the protocol.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#analyticMethod',
    ),
    atapi.StringField(
        'blinding',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.StringWidget(
            label=_(u'Blinding'),
            description=_(u'How investigators were effectively blinded by various techniques to assure impartiality.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#blinding',
    ),
    atapi.ReferenceField(
        'cancerTypes',
        enforceVocabulary=True,
        multiValued=True,
        relationship='cancerTypesStudiedByProtocol',
        required=False,
        storage=atapi.AnnotationStorage(),
        vocabulary_factory=u'eke.knowledge.Diseases',
        vocabulary_display_path_bound=-1,
        widget=atapi.ReferenceWidget(
            label=_(u'Cancer Types'),
            description=_(u'What cancers this protocol is analyzing.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#cancerType',
        predicateTarget=IDisease,
    ),
    atapi.TextField(
        'comments',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.TextAreaWidget(
            label=_(u'Comments'),
            description=_(u'Any commentary from insightful to invective about this protocol.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#comments',
    ),
    atapi.TextField(
        'dataSharingPlan',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.TextAreaWidget(
            label=_(u'Data Sharing Plan'),
            description=_(u'Any plans on sharing data.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#dataSharingPlan',
    ),
    atapi.TextField(
        'inSituDataSharingPlan',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.TextAreaWidget(
            label=_(u'In Situ Data Sharing Plan'),
            description=_(u'The data sharing plan that is actually in place in the protocol.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#inSituDataSharingPlan',
    ),
    atapi.DateTimeField(
        'startDate',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.CalendarWidget(
            label=_(u'Start Date'),
            description=_(u'When this protocol began or will begin.'),
            show_hm=False,
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#startDate',
    ),
    atapi.DateTimeField(
        'estimatedFinishDate',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.CalendarWidget(
            label=_(u'Estimated Finish Date'),
            description=_(u'When this protocol is predicted to cease.'),
            show_hm=False,
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#estimatedFinishDate',
    ),
    atapi.DateTimeField(
        'finishDate',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.CalendarWidget(
            label=_(u'Finish Date'),
            description=_(u'When this protocol actually ceased.'),
            show_hm=False,
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#finishDate',
    ),
    atapi.StringField(
        'design',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.StringWidget(
            label=_(u'Design'),
            description=_(u'The design type of this protocol.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#design',
    ),
    atapi.LinesField(
        'fieldOfResearch',
        storage=atapi.AnnotationStorage(),
        required=False,
        multiValued=True,
        widget=atapi.LinesWidget(
            label=_(u'Fields of Research'),
            description=_(u'A list of numeric codes identifying what fields of research the protocol is pursuing.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#fieldOfResearch',
    ),
    atapi.StringField(
        'abbrevName',
        storage=atapi.AnnotationStorage(),
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'Abbreviated Name'),
            description=_(u'A shorter and possibly far more convenient name for the protocol.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#abbreviatedName',
    ),
    atapi.TextField(
        'objective',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.TextAreaWidget(
            label=_(u'Objective'),
            description=_(u'The thing aimed at or sought by this protocol.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#objective',
    ),
    atapi.BooleanField(
        'project',
        storage=atapi.AnnotationStorage(),
        required=False,
        default=False,
        widget=atapi.BooleanWidget(
            label=_(u'Project?'),
            description=_(u"True if this protocol actually a project, false if it's really a protocol."),
        ),
    ),
    atapi.StringField(
        'protocolType',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.StringWidget(
            label=_(u'Protocol Type'),
            description=_(u'The kind of protocol this is.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#protocolType',
    ),
    atapi.ReferenceField(
        'publications',
        enforceVocabulary=True,
        multiValued=True,
        relationship='publicationsPublishedByProtocol',
        required=False,
        storage=atapi.AnnotationStorage(),
        vocabulary_factory=u'eke.publications.PublicationsVocabulary',
        vocabulary_display_path_bound=-1,
        widget=atapi.ReferenceWidget(
            label=_(u'Publications'),
            description=_(u'What publications have been published about this protocol.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#publications',
        predicateTarget=IPublication,
    ),
    atapi.TextField(
        'outcome',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.TextAreaWidget(
            label=_(u'Outcome'),
            description=_(u'The outcome (or expected outcome) of executing this protocol.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#outcome',
    ),
    atapi.TextField(
        'secureOutcome',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.TextAreaWidget(
            label=_(u'Secure Outcome'),
            description=_(u'The secure outcome (or expected secure outcome) of executing this protocol.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#secureOutcome',
    ),
    atapi.StringField(
        'plannedSampleSize',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.StringWidget(
            label=_(u'Planned Sample Size'),
            description=_(u'The size of the sample the protocol is expected to use.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#plannedSampleSize',
    ),
    atapi.StringField(
        'finalSampleSize',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.StringWidget(
            label=_(u'Final Sample Size'),
            description=_(u'The size of the sample the protocol actually used.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#finalSampleSize',
    ),
    atapi.ReferenceField(
        'isAPilotFor',
        enforceVocabulary=True,
        multiValued=True,
        relationship='thisProtocolIsAPilotFor',
        required=False,
        storage=atapi.AnnotationStorage(),
        vocabulary_factory=u'eke.study.ProtocolsVocabulary',
        vocabulary_display_path_bound=-1,
        widget=atapi.ReferenceWidget(
            label=_(u'Piloting Protocol'),
            description=_(u'The protocols---if any---for which this protocol is a pilot.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#isAPilot',
        predicateTarget=IProtocol,
    ),
    atapi.ReferenceField(
        'obtainsData',
        enforceVocabulary=True,
        multiValued=True,
        relationship='thisProtocolObtainsDataFrom',
        required=False,
        storage=atapi.AnnotationStorage(),
        vocabulary_factory=u'eke.study.ProtocolsVocabulary',
        vocabulary_display_path_bound=-1,
        widget=atapi.ReferenceWidget(
            label=_(u'Data Source Protocols'),
            description=_(u'The protocols---if any---from which this protocol obtains data.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#obtainsDataFrom',
        predicateTarget=IProtocol,
    ),
    atapi.ReferenceField(
        'providesData',
        enforceVocabulary=True,
        multiValued=True,
        relationship='thisProtocolProvidesDataTo',
        required=False,
        storage=atapi.AnnotationStorage(),
        vocabulary_factory=u'eke.study.ProtocolsVocabulary',
        vocabulary_display_path_bound=-1,
        widget=atapi.ReferenceWidget(
            label=_(u'Data Sink Protocols'),
            description=_(u'The protocols---if any---to which this protocol provides data.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#providesDataTo',
        predicateTarget=IProtocol,
    ),
    atapi.ReferenceField(
        'obtainsSpecimens',
        enforceVocabulary=True,
        multiValued=True,
        relationship='thisProtocolObtainsSpecimensFrom',
        required=False,
        storage=atapi.AnnotationStorage(),
        vocabulary_factory=u'eke.study.ProtocolsVocabulary',
        vocabulary_display_path_bound=-1,
        widget=atapi.ReferenceWidget(
            label=_(u'Specimen Source Protocols'),
            description=_(u'The protocols---if any---from which this protocol obtains specimens.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#obtainsSpecimensFrom',
        predicateTarget=IProtocol,
    ),
    atapi.ReferenceField(
        'providesSpecimens',
        enforceVocabulary=True,
        multiValued=True,
        relationship='thisProtocolProvidesSpecimensTo',
        required=False,
        storage=atapi.AnnotationStorage(),
        vocabulary_factory=u'eke.study.ProtocolsVocabulary',
        vocabulary_display_path_bound=-1,
        widget=atapi.ReferenceWidget(
            label=_(u'Specimen Sink Protocols'),
            description=_(u'The protocols---if any---from which this protocol provides specimens.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#contributesSpecimensTo',
        predicateTarget=IProtocol,
    ),
    atapi.ReferenceField(
        'relatedProtocols',
        enforceVocabulary=True,
        multiValued=True,
        relationship='thisProtocolHasOtherRelationshipWith',
        required=False,
        storage=atapi.AnnotationStorage(),
        vocabulary_factory=u'eke.study.ProtocolsVocabulary',
        vocabulary_display_path_bound=-1,
        widget=atapi.ReferenceWidget(
            label=_(u'Related Protocols'),
            description=_(u'The protocol---if any---to which this protocol has some relationship.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#hasOtherRelationship',
        predicateTarget=IProtocol,
    ),
    atapi.StringField(
        'animalSubjectTraining',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.StringWidget(
            label=_(u'Animal Subject Training'),
            description=_(u'A note about whether animal subject training is required, has been given, or has not been given.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#animalSubjectTrainingReceived',
    ),
    atapi.StringField(
        'humanSubjectTraining',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.StringWidget(
            label=_(u'Human Subject Training'),
            description=_(u'A note about whether human subject training is required, has been given, or has not been given.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#humanSubjectTrainingReceived',
    ),
    atapi.StringField(
        'irbApproval',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.StringWidget(
            label=_(u'IRB Approval'),
            description=_(u'A note about whether Internal Review Board approval is required, has been given, or otherwise.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#irbApprovalNeeded',
    ),
    atapi.DateTimeField(
        'originalIRBApprovalDate',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.CalendarWidget(
            label=_(u'Original IRB Approval Date'),
            description=_(u'The date on which the first, original IRB approval was given for this protocol.'),
            show_hm=False,
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#originalIRBApprovalDate',
    ),
    atapi.DateTimeField(
        'currentIRBApprovalDate',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.CalendarWidget(
            label=_(u'Current IRB Approval Date'),
            description=_(u'The date on which the current IRB approval was given for this protocol.'),
            show_hm=False,
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#currentIRBApprovalDate',
    ),
    atapi.DateTimeField(
        'currentIRBExpirationDate',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.CalendarWidget(
            label=_(u'Current IRB Expiration Date'),
            description=_(u'The date on which the current IRB approval will expire.'),
            show_hm=False,
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#irbExpirationDate',
    ),
    atapi.TextField(
        'irbNotes',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.TextAreaWidget(
            label=_(u'IRB Notes'),
            description=_(u'General notes about the Internal Review Board with regard to this protocol.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#irbNotes',
    ),
    atapi.StringField(
        'irbNumber',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.StringWidget(
            label=_(u'IRB Number'),
            description=_(u'The approval identification number given to this protocol by the Internal Review Board.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#irbNumber',
    ),
    atapi.LinesField(
        'siteRoles',
        storage=atapi.AnnotationStorage(),
        required=False,
        multiValued=True,
        widget=atapi.LinesWidget(
            label=_(u'Site Roles'),
            description=_(u'The roles the site plays in executing this protocol.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#siteRole',
    ),
    atapi.StringField(
        'reportingStage',
        storage=atapi.AnnotationStorage(),
        required=False,
        widget=atapi.StringWidget(
            label=_(u'Reporting Stage'),
            description=_(u'Sequence of reporting for this protocol.'),
        ),
        predicateURI='http://edrn.nci.nih.gov/rdf/schema.rdf#reportingStage',
    ),
    atapi.ReferenceField(
        'biomarkers',
        enforceVocabulary=True,
        multiValued=True,
        relationship='biomarkersStudiedByThisProtocol',
        required=False,
        storage=atapi.AnnotationStorage(),
        vocabulary_factory=u'eke.biomarker.BiomarkersVocabulary',
        vocabulary_display_path_bound=-1,
        widget=atapi.ReferenceWidget(
            label=_(u'Biomarkers'),
            description=_(u'Biomarkers under study by this protocol.'),
        ),
    ),
    atapi.ReferenceField(
        'datasets',
        enforceVocabulary=True,
        multiValued=True,
        relationship='datasetsGeneratedByThisProtocol',
        required=False,
        storage=atapi.AnnotationStorage(),
        vocabulary_factory=u'eke.ecas.DatasetsVocabulary',
        vocabulary_display_path_bound=-1,
        widget=atapi.ReferenceWidget(
            label=_(u'Datasets'),
            description=_(u'Datasets generated by this protocol.'),
        ),
    ),
    atapi.ComputedField(
        'piName',
        required=False,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        expression='context._computePIName()',
        multiValued=False,
        modes=('view',),
        widget=atapi.ComputedWidget(
            visible={'edit': 'invisible', 'view': 'invisible'},
        ),
    ),
    atapi.ComputedField(
        'datasetNames',
        required=False,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        expression='context._computeDatasetNames()',
        multiValued=True,
        modes=('view',),
        widget=atapi.ComputedWidget(
            visible={'edit': 'invisible', 'view': 'invisible'},
        ),
    ),
    atapi.ComputedField(
        'involvedSiteNames',
        required=False,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        expression='context._computeInvolvedSiteNames()',
        multiValued=True,
        modes=('view',),
        widget=atapi.ComputedWidget(
            visible={'edit': 'invisible', 'view': 'invisible'},
        ),
    ),
    atapi.ComputedField(
        'principalInvestigatorUID',
        accessor='piUID',
        required=False,
        searchable=False,
        expression='context._computePIUID()',
        modes=('view',),
        widget=atapi.ComputedWidget(
            visible={'edit': 'invisible', 'view': 'invisible'},
        ),
    ),
))
# FIXME: KnowledgeObjectSchema has title's predicate set to something wrong.
# When that's finally fixed, remove this line:
ProtocolSchema['title'].predicateURI = dublincore.TITLE_URI

finalizeATCTSchema(ProtocolSchema, folderish=True, moveDiscussion=False)

class Protocol(folder.ATFolder, knowledgeobject.KnowledgeObject):
    '''Protocol.'''
    implements(IProtocol)
    schema                       = ProtocolSchema
    portal_type                  = 'Protocol'
    title                        = atapi.ATFieldProperty('title')
    description                  = atapi.ATFieldProperty('description')
    abstract                     = atapi.ATFieldProperty('abstract')
    involvedInvestigatorSites    = atapi.ATReferenceFieldProperty('involvedInvestigatorSites')
    coordinatingInvestigatorSite = atapi.ATReferenceFieldProperty('coordinatingInvestigatorSite')
    leadInvestigatorSite         = atapi.ATReferenceFieldProperty('leadInvestigatorSite')
    bmName                       = atapi.ATFieldProperty('bmName')
    collaborativeGroupText       = atapi.ATFieldProperty('collaborativeGroupText')
    phasedStatus                 = atapi.ATFieldProperty('phasedStatus')
    aims                         = atapi.ATFieldProperty('aims')
    analyticMethod               = atapi.ATFieldProperty('analyticMethod')
    blinding                     = atapi.ATFieldProperty('blinding')
    cancerTypes                  = atapi.ATReferenceFieldProperty('cancerTypes')
    comments                     = atapi.ATFieldProperty('comments')
    dataSharingPlan              = atapi.ATFieldProperty('dataSharingPlan')
    inSituDataSharingPlan        = atapi.ATFieldProperty('inSituDataSharingPlan')
    startDate                    = atapi.ATFieldProperty('startDate')
    estimatedFinishDate          = atapi.ATFieldProperty('estimatedFinishDate')
    finishDate                   = atapi.ATFieldProperty('finishDate')
    design                       = atapi.ATFieldProperty('design')
    fieldOfResearch              = atapi.ATFieldProperty('fieldOfResearch')
    abbrevName                   = atapi.ATFieldProperty('abbrevName')
    objective                    = atapi.ATFieldProperty('objective')
    project                      = atapi.ATFieldProperty('project')
    protocolType                 = atapi.ATFieldProperty('protocolType')
    publications                 = atapi.ATReferenceFieldProperty('publications')
    outcome                      = atapi.ATFieldProperty('outcome')
    secureOutcome                = atapi.ATFieldProperty('secureOutcome')
    plannedSampleSize            = atapi.ATFieldProperty('plannedSampleSize')
    finalSampleSize              = atapi.ATFieldProperty('finalSampleSize')
    isAPilotFor                  = atapi.ATReferenceFieldProperty('isAPilotFor')
    obtainsData                  = atapi.ATReferenceFieldProperty('obtainsData')
    providesData                 = atapi.ATReferenceFieldProperty('providesData')
    obtainsSpecimens             = atapi.ATReferenceFieldProperty('obtainsSpecimens')
    providesSpecimens            = atapi.ATReferenceFieldProperty('providesSpecimens')
    relatedProtocols             = atapi.ATReferenceFieldProperty('relatedProtocols')
    animalSubjectTraining        = atapi.ATFieldProperty('animalSubjectTraining')
    humanSubjectTraining         = atapi.ATFieldProperty('humanSubjectTraining')
    irbApproval                  = atapi.ATFieldProperty('irbApproval')
    originalIRBApprovalDate      = atapi.ATFieldProperty('originalIRBApprovalDate')
    currentIRBApprovalDate       = atapi.ATFieldProperty('currentIRBApprovalDate')
    currentIRBExpirationDate     = atapi.ATFieldProperty('currentIRBExpirationDate')
    irbNotes                     = atapi.ATFieldProperty('irbNotes')
    irbNumber                    = atapi.ATFieldProperty('irbNumber')
    siteRoles                    = atapi.ATFieldProperty('siteRoles')
    reportingStage               = atapi.ATFieldProperty('reportingStage')
    biomarkers                   = atapi.ATReferenceFieldProperty('biomarkers')
    datasets                     = atapi.ATReferenceFieldProperty('datasets')
    piName                       = atapi.ATFieldProperty('piName')
    datasetNames                 = atapi.ATFieldProperty('datasetNames')
    involvedSiteNames            = atapi.ATFieldProperty('involvedSiteNames')
    def _computePIName(self):
        if not self.leadInvestigatorSite:
            return None
        if not self.leadInvestigatorSite.principalInvestigator:
            return None
        return self.leadInvestigatorSite.principalInvestigator.title
    def _computeDatasetNames(self):
        if not self.datasets:
            return []
        return [i.title for i in self.datasets if i and i.title]
    def _computeInvolvedSiteNames(self):
        if not self.involvedInvestigatorSites:
            return []
        return [i.title for i in self.involvedInvestigatorSites if i and i.title]
    def _computeDescription(self):
        # CA-580 order: abstract is most important; then objective, then aims, finally outcome.
        # If none of those have any text, punt.
        for fieldName in ('abstract', 'objective', 'aims', 'outcome'):
            value = getattr(self, fieldName, None)
            if value:
                filterer = MarkupFilterer()
                filterer.feed(safe_unicode(value))
                return filterer.getResult()
        return u''
    def _computePIUID(self):
        return self.leadInvestigatorSite is not None and self.leadInvestigatorSite.getPiUID() or None

atapi.registerType(Protocol, PROJECTNAME)

def getUniqueLabel(title, protocols):
    if title not in protocols: return title
    index = 1
    while index < MAX_PROTOCOL_INDEX:
        index += 1
        newTitle = u'{} ({})'.format(title, index)
        if newTitle not in protocols: return newTitle
    raise ValueError(u"There can't be {} protocols all named '{}'. Something else is wrong.".format(index, title))

def ProtocolVocabularyFactory(context):
    catalog = getToolByName(context, 'portal_catalog')
    # TODO: filter by review_state?
    results = catalog(object_provides=IProtocol.__identifier__)
    protocols = {}
    for i in results:
        title, uid = i.Title.decode('utf-8'), i.UID
        label = getUniqueLabel(title, protocols)
        protocols[label] = uid
    labels = protocols.keys()
    labels.sort()
    terms = [SimpleVocabulary.createTerm(protocols[i], protocols[i], i) for i in labels]
    return SimpleVocabulary(terms)
directlyProvides(ProtocolVocabularyFactory, IVocabularyFactory)

def TeamProjectsVocabularyFactory(context):
    catalog = getToolByName(context, 'portal_catalog')
    # TODO: filter by review_state?
    results = catalog(object_provides=IProtocol.__identifier__, sort_on='sortable_title', project=True)
    return SimpleVocabulary([SimpleVocabulary.createTerm(i.UID, i.UID, i.Title.decode('utf-8')) for i in results])
directlyProvides(TeamProjectsVocabularyFactory, IVocabularyFactory)

def ProtocolUpdater(context, event):
    context.piName = context._computePIName()
    context.datasetNames = context._computeDatasetNames()
    context.involvedSiteNames = context._computeInvolvedSiteNames()
    context.setDescription(context._computeDescription())
    context.reindexObject()
