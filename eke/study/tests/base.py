# encoding: utf-8
# Copyright 2008 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
Testing base code.
'''

import eke.knowledge.tests.base as ekeKnowledgeBase
import eke.publications.tests.base as ekePublicationsBase
import eke.site.tests.base as ekeSiteBase

_firstProtocolRDF = '''<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
    xmlns:edrn="http://edrn.nci.nih.gov/rdf/schema.rdf#"
    xmlns:dc="http://purl.org/dc/terms/"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <rdf:Description rdf:about="http://swa.it/edrn/ps">
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Protocol"/>
        <dc:title>Public Safety</dc:title>
        <dc:description>Clinic surveillance and intelligence gathering.</dc:description>
        <edrn:involvedInvestigatorSite rdf:resource='http://tongue.com/clinic/3d'/>
        <edrn:involvedInvestigatorSite rdf:resource='http://plain.com/2d'/>
        <edrn:coordinatingInvestigatorSite rdf:resource='http://tongue.com/clinic/3d'/>
        <edrn:leadInvestigatorSite rdf:resource='http://plain.com/2d'/>
        <edrn:bmName>Federico.</edrn:bmName>
        <edrn:collaborativeGroupText>Works with the Special Ops group.</edrn:collaborativeGroupText>
        <edrn:phasedStatus>Stun</edrn:phasedStatus>
        <edrn:aims>Gather intelligence and do surveillance.</edrn:aims>
        <edrn:analyticMethod>Top secret.</edrn:analyticMethod>
        <edrn:blinding>Pepper spray</edrn:blinding>
        <edrn:cancerType rdf:resource='http://edrn.nci.nih.gov/data/diseases/1'/>
        <edrn:comments>Ugh.</edrn:comments>
        <edrn:dataSharingPlan>We will be very open with our data.</edrn:dataSharingPlan>
        <edrn:inSituDataSharingPlan>No data may be shared.</edrn:inSituDataSharingPlan>
        <edrn:startDate rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">1967-12-21T00:00:00</edrn:startDate>
        <edrn:estimatedFinishDate rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">2029-06-15T00:00:00</edrn:estimatedFinishDate>
        <edrn:finishDate rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">2011-11-06T00:00:00</edrn:finishDate>
        <edrn:design>Pair fratelli with cyborg girls with night-vision goggles.</edrn:design>
        <edrn:fieldOfResearch>3</edrn:fieldOfResearch>
        <edrn:fieldOfResearch>14</edrn:fieldOfResearch>
        <edrn:fieldOfResearch>7</edrn:fieldOfResearch>
        <edrn:abbreviatedName>PS</edrn:abbreviatedName>
        <edrn:objective>Track terrorist activity.</edrn:objective>
        <edrn:projectFlag>Protocol</edrn:projectFlag>
        <edrn:protocolType>Fictional</edrn:protocolType>
        <edrn:publications rdf:resource='http://is.gd/q6mS'/>
        <edrn:outcome>Increased public safety.</edrn:outcome>
        <edrn:secureOutcome>Better control of the citizenry.</edrn:secureOutcome>
        <edrn:plannedSampleSize>12</edrn:plannedSampleSize>
        <edrn:finalSampleSize>48</edrn:finalSampleSize>
        <edrn:animalSubjectTrainingReceived>No</edrn:animalSubjectTrainingReceived>
        <edrn:humanSubjectTrainingReceived>No</edrn:humanSubjectTrainingReceived>
        <edrn:irbApprovalNeeded>No</edrn:irbApprovalNeeded>
        <edrn:originalIRBApprovalDate rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">1963-02-28T00:00:00</edrn:originalIRBApprovalDate>
        <edrn:currentIRBApprovalDate rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">1963-09-27T00:00:00</edrn:currentIRBApprovalDate>
        <edrn:irbExpirationDate rdf:datatype="http://www.w3.org/2001/XMLSchema#dateTime">1964-02-26T00:00:00</edrn:irbExpirationDate>
        <edrn:irbNotes>IRB?</edrn:irbNotes>
        <edrn:irbNumber>SECRET</edrn:irbNumber>
        <edrn:siteRole>Consultant</edrn:siteRole>
        <edrn:reportingStage>Other, specify</edrn:reportingStage>
    </rdf:Description></rdf:RDF>'''

_secondProtocolRDF = '''<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
    xmlns:edrn="http://edrn.nci.nih.gov/rdf/schema.rdf#"
    xmlns:dc="http://purl.org/dc/terms/"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <rdf:Description rdf:about="http://swa.it/edrn/so">
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Protocol"/>
        <dc:title>Special Ops</dc:title>
        <edrn:isAPilot rdf:resource='http://swa.it/edrn/ps'/>
        <edrn:obtainsDataFrom rdf:resource='http://swa.it/edrn/ps'/>
        <edrn:providesDataTo rdf:resource='http://swa.it/edrn/ps'/>
        <edrn:contributesSpecimensTo rdf:resource='http://swa.it/edrn/ps'/>
        <edrn:obtainsSpecimensFrom rdf:resource='http://swa.it/edrn/ps'/>
        <edrn:hasOtherRelationship rdf:resource='http://swa.it/edrn/ps'/>
    </rdf:Description>
</rdf:RDF>'''

_markedUpProtocolRDF = '''<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
    xmlns:edrn="http://edrn.nci.nih.gov/rdf/schema.rdf#"
    xmlns:dc="http://purl.org/dc/terms/"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <rdf:Description rdf:about="http://swa.it/edrn/so">
        <rdf:type rdf:resource="http://edrn.nci.nih.gov/rdf/types.rdf#Protocol"/>
        <dc:title>Barrett&amp;#39;s Esophagus Methylation Profiles</dc:title>
        <edrn:abbreviatedName>Barrett&amp;#39;s abbreviated &lt;strong&gt;Esophagus&lt;/strong&gt;</edrn:abbreviatedName>
        <edrn:bmName>Hidalgo</edrn:bmName>
        <edrn:leadInvestigatorSite rdf:resource='http://plain.com/2d'/>
        <edrn:involvedInvestigatorSite rdf:resource='http://tongue.com/clinic/3d'/>
        <edrn:collaborativeGroupText>Maybe in order to understand mankind, we have to look at the word itself. Mankind. Basically, it's made up of two separate words&#x2014;'mank' and 'ind'. What do these words mean It's a mystery, and that's why so is mankind.</edrn:collaborativeGroupText>
    </rdf:Description>
</rdf:RDF>'''

_manyProtocolsRDF = '''<?xml version='1.0' encoding='UTF-8'?>
<rdf:RDF
    xmlns:edrn='http://edrn.nci.nih.gov/rdf/schema.rdf#'
    xmlns:dc='http://purl.org/dc/terms/'
    xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>
    <rdf:Description rdf:about='http://protocols.com/protocols/1'>
        <rdf:type rdf:resource='http://edrn.nci.nih.gov/rdf/types.rdf#Protocol'/>
        <dc:title>Protocol One</dc:title>
        <dc:description>Abstract.</dc:description>
        <edrn:objective>Objective.</edrn:objective>
        <edrn:aims>Aims.</edrn:aims>
        <edrn:outcome>Finally, an outcome!</edrn:outcome>
    </rdf:Description>
    <rdf:Description rdf:about='http://protocols.com/protocols/2'>
        <rdf:type rdf:resource='http://edrn.nci.nih.gov/rdf/types.rdf#Protocol'/>
        <dc:title>Protocol Two</dc:title>
        <edrn:objective>Objective.</edrn:objective>
        <edrn:outcome>Finally, an outcome!</edrn:outcome>
    </rdf:Description>
    <rdf:Description rdf:about='http://protocols.com/protocols/3'>
        <rdf:type rdf:resource='http://edrn.nci.nih.gov/rdf/types.rdf#Protocol'/>
        <dc:title>Protocol Three</dc:title>
        <edrn:aims>Aims.</edrn:aims>
        <edrn:outcome>Finally, an outcome!</edrn:outcome>
    </rdf:Description>
    <rdf:Description rdf:about='http://protocols.com/protocols/4'>
        <rdf:type rdf:resource='http://edrn.nci.nih.gov/rdf/types.rdf#Protocol'/>
        <dc:title>Protocol Four</dc:title>
        <edrn:outcome>Finally, an outcome!</edrn:outcome>
    </rdf:Description>
</rdf:RDF>'''

_duplicateProtocolsRDF = '''<?xml version='1.0' encoding='UTF-8'?>
<rdf:RDF
    xmlns:edrn='http://edrn.nci.nih.gov/rdf/schema.rdf#'
    xmlns:dc='http://purl.org/dc/terms/'
    xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>
    <rdf:Description rdf:about='http://protocols.com/protocols/dup/1'>
        <rdf:type rdf:resource='http://edrn.nci.nih.gov/rdf/types.rdf#Protocol'/>
        <dc:title>A Duplicate Title</dc:title>
        <dc:description>Abstract.</dc:description>
        <edrn:objective>Objective.</edrn:objective>
        <edrn:aims>Aims.</edrn:aims>
        <edrn:outcome>Finally, an outcome!</edrn:outcome>
    </rdf:Description>
    <rdf:Description rdf:about='http://protocols.com/protocols/dup/2'>
        <rdf:type rdf:resource='http://edrn.nci.nih.gov/rdf/types.rdf#Protocol'/>
        <dc:title>A Duplicate Title</dc:title>
        <edrn:objective>Objective.</edrn:objective>
        <edrn:outcome>Finally, an outcome!</edrn:outcome>
    </rdf:Description>
</rdf:RDF>'''

_name1RDF = u'''<?xml version='1.0' encoding='UTF-8'?>
<rdf:RDF
    xmlns:edrn='http://edrn.nci.nih.gov/rdf/schema.rdf#'
    xmlns:dc='http://purl.org/dc/terms/'
    xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>
    <rdf:Description rdf:about='http://protocols.com/protocols/renamed/1'>
        <rdf:type rdf:resource='http://edrn.nci.nih.gov/rdf/types.rdf#Protocol'/>
        <dc:title>Name 1</dc:title>
        <dc:description>Abstract.</dc:description>
        <edrn:objective>Objective.</edrn:objective>
        <edrn:aims>Aims.</edrn:aims>
        <edrn:outcome>Finally, an outcome!</edrn:outcome>
    </rdf:Description>
</rdf:RDF>'''

_name2RDF = u'''<?xml version='1.0' encoding='UTF-8'?>
<rdf:RDF
    xmlns:edrn='http://edrn.nci.nih.gov/rdf/schema.rdf#'
    xmlns:dc='http://purl.org/dc/terms/'
    xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>
    <rdf:Description rdf:about='http://protocols.com/protocols/renamed/1'>
        <rdf:type rdf:resource='http://edrn.nci.nih.gov/rdf/types.rdf#Protocol'/>
        <dc:title>Name 2</dc:title>
        <dc:description>Abstract.</dc:description>
        <edrn:objective>Objective.</edrn:objective>
        <edrn:aims>Aims.</edrn:aims>
        <edrn:outcome>Finally, an outcome!</edrn:outcome>
    </rdf:Description>
</rdf:RDF>'''


def registerLocalTestData():
    ekeKnowledgeBase.registerLocalTestData()
    ekePublicationsBase.registerLocalTestData()
    ekeSiteBase.registerLocalTestData()
    ekeKnowledgeBase.registerTestData('/protocols/a', _firstProtocolRDF)
    ekeKnowledgeBase.registerTestData('/protocols/b', _secondProtocolRDF)
    ekeKnowledgeBase.registerTestData('/protocols/c', _markedUpProtocolRDF)
    ekeKnowledgeBase.registerTestData('/protocols/d', _manyProtocolsRDF)
    ekeKnowledgeBase.registerTestData('/protocols/dups', _duplicateProtocolsRDF)
    ekeKnowledgeBase.registerTestData('/protocols/name1', _name1RDF)
    ekeKnowledgeBase.registerTestData('/protocols/name2', _name2RDF)
