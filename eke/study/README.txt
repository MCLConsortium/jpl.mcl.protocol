This package provides Plone 3 content objects for the EDRN Knowledge
Environment (EKE_)'s management, display, and RDF ingest of studies and
protocols.  A protocol is an official record and plan for scientific inquiry
especially involving medical procedures and with living subjects.  EDRN
pursues many protocols that research cancer biomarkers.  This component,
``eke.study``, provides search, display, and RDF ingest of protocol
information.


Content Types
=============

The content types introduced in this package include the following:

Study Folder
    A folder that contains studies and protocols, and may be populated
    from an RDF data source.  It may also contain Study Folders as
    sub-folders.
Protocol
    A single protocol carried out by EDRN and identified by URI_.

The remainder of this document demonstrates the content types and RDF ingest
using a series of functional tests.


Tests
=====

First we have to set up some things and login to the site::

    >>> app = layer['app']
    >>> from plone.testing.z2 import Browser
    >>> from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD
    >>> browser = Browser(app)
    >>> browser.handleErrors = False
    >>> browser.addHeader('Authorization', 'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD))
    >>> portal = layer['portal']    
    >>> portalURL = portal.absolute_url()

We'll also have a second browser that's unprivileged for some later
demonstrations::

    >>> unprivilegedBrowser = Browser(app)

Now we can check out the new types introduced in this package.


Addable Content
---------------

Here we'll exercise some of the content objects available in this project and
demonstrate their properties and constraints.


Study Folder
~~~~~~~~~~~~

A study folder contains protocols and other study folders.  They can be
created anywhere in the portal::

    >>> browser.open(portalURL)
    >>> l = browser.getLink(id='study-folder')
    >>> l.url.endswith('createObject?type_name=Study+Folder')
    True
    >>> l.click()
    >>> browser.getControl(name='title').value = u'Questionable Studies'
    >>> browser.getControl(name='description').value = u'This folder is just for functional tests.'
    >>> browser.getControl(name='rdfDataSource').value = u'testscheme://localhost/protocols/a'
    >>> browser.getControl(name='form.button.save').click()
    >>> 'questionable-studies' in portal.objectIds()
    True
    >>> f = portal['questionable-studies']
    >>> f.title
    'Questionable Studies'
    >>> f.description
    'This folder is just for functional tests.'
    >>> f.rdfDataSource
    'testscheme://localhost/protocols/a'

Study Folders hold Protocols as well as other Study Folders.  We'll test
adding Protocols below, but let's make sure there's a link to created nested
Study Folders::

    >>> browser.open(portalURL + '/questionable-studies')
    >>> l = browser.getLink(id='study-folder')
    >>> l.url.endswith('createObject?type_name=Study+Folder')
    True


Protocol
~~~~~~~~

A single Protocol object corresponds with a single real-world EDRN member
protocol or study; they may be created only within Study Folders::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='protocol')
    Traceback (most recent call last):
    ...
    LinkNotFoundError

So, let's create one in our above Study Folder.  Before we start setting up
attributes, though, we'll need some related objects that protocols have links
to.  A protocol refers to sites::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='site-folder').click()
    >>> browser.getControl(name='title').value = u'Questionable Sites'
    >>> browser.getControl(name='description').value = u'This folder is just for functional tests.'
    >>> browser.getControl(name='rdfDataSource').value = 'testscheme://localhost/sites/b'
    >>> browser.getControl(name='peopleDataSource').value = 'testscheme://localhost/people/b'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/questionable-sites/ingest')

A protocol also refers to diseases::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='knowledge-folder').click()
    >>> browser.getControl(name='title').value = u'My Manifold Diseases'
    >>> browser.getControl(name='description').value = u'This folder is just for functional tests.'
    >>> browser.getControl(name='rdfDataSource').value = u'testscheme://localhost/diseases/b'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/my-manifold-diseases/ingest')

A protocol also refers to publications::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='publication-folder').click()
    >>> browser.getControl(name='title').value = u'Ye Olde Bookshelfe'
    >>> browser.getControl(name='description').value = u'This folder is just for functional tests.'
    >>> browser.getControl(name='rdfDataSource').value = u'testscheme://localhost/pubs/b'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/ye-olde-bookshelfe/ingest')

Now we can create our test Protocol::

    >>> browser.open(portalURL + '/questionable-studies')
    >>> l = browser.getLink(id='protocol')
    >>> l.url.endswith('createObject?type_name=Protocol')
    True
    >>> l.click()
    >>> browser.getControl(name='title').value = 'MK Ultra'
    >>> browser.getControl(name='identifier').value = 'http://cia.gov/edrn/mk-ultra'
    >>> browser.getControl(name='abstract').value = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    >>> browser.getControl(name='involvedInvestigatorSites:list').displayValue = ["Dr Tongue's 3D Clinic", 'A Plain 2D Clinic']
    >>> browser.getControl(name='coordinatingInvestigatorSite:list').displayValue = ["Dr Tongue's 3D Clinic"]
    >>> browser.getControl(name='leadInvestigatorSite:list').displayValue = ['A Plain 2D Clinic']
    >>> browser.getControl(name='bmName').value = 'I had a huge BM once.'
    >>> browser.getControl(name='collaborativeGroupText').value = 'Sed do eiusmod tempor incididunt ut labore.'
    >>> browser.getControl(name='phasedStatus').value = 'Stun'
    >>> browser.getControl(name='aims').value = 'Quis nostrud exercitation ullamco laboris nisi ut aliquip.'
    >>> browser.getControl(name='analyticMethod').value = 'Duis aute irure dolor in reprehenderit in voluptate velit.'
    >>> browser.getControl(name='blinding').value = 'AGGH! THE LIGHT!!!1'
    >>> browser.getControl(name='cancerTypes:list').displayValue = ['Anal seepage', 'Rectocele']
    >>> browser.getControl(name='comments').value = 'Eyew.'
    >>> browser.getControl(name='dataSharingPlan').value = 'For each operand that names a file of a type other than directory.'
    >>> browser.getControl(name='inSituDataSharingPlan').value = 'The dd utility copies the standard input to the standard output.'
    >>> from datetime import datetime, timedelta
    >>> today = datetime.now()
    >>> tomorrow = today + timedelta(1)
    >>> dayAfter = tomorrow + timedelta(1)
    >>> yesterday = today - timedelta(1)
    >>> browser.getControl(name='startDate_year').displayValue = [str(yesterday.year)]
    >>> browser.getControl(name='startDate_month').value = ['%02d' % yesterday.month]
    >>> browser.getControl(name='startDate_day').value = ['%02d' % yesterday.day]
    >>> browser.getControl(name='estimatedFinishDate_year').displayValue = [str(tomorrow.year)]
    >>> browser.getControl(name='estimatedFinishDate_month').value = ['%02d' % tomorrow.month]
    >>> browser.getControl(name='estimatedFinishDate_day').value = ['%02d' % tomorrow.day]
    >>> browser.getControl(name='finishDate_year').displayValue = [str(dayAfter.year)]
    >>> browser.getControl(name='finishDate_month').value = ['%02d' % dayAfter.month]
    >>> browser.getControl(name='finishDate_day').value = ['%02d' % dayAfter.day]
    >>> browser.getControl(name='design').value = 'Sunt in culpa qui officia deserunt mollit anim id est laborum.'
    >>> browser.getControl(name='fieldOfResearch:lines').value = '3\n14\n7'
    >>> browser.getControl(name='abbrevName').value = 'MKU'
    >>> browser.getControl(name='objective').value = 'The cat utility reads files sequentially, writing them to standard output.'
    >>> browser.getControl('Project?').selected = False
    >>> browser.getControl(name='protocolType').value = 'Silly'
    >>> browser.getControl(name='publications:list').displayValue = ['Teriyaki Beef', 'Glazed Roast Chicken']
    >>> browser.getControl(name='outcome').value = "Tar is short for ``tape archiver'', so named for historical reasons."
    >>> browser.getControl(name='secureOutcome').value = 'OpenSSL is a cryptography toolkit.'
    >>> browser.getControl(name='plannedSampleSize').value = '156'
    >>> browser.getControl(name='finalSampleSize').value = '0' # They all must've died
    >>> browser.getControl(name='animalSubjectTraining').value = 'Maybe'
    >>> browser.getControl(name='humanSubjectTraining').value = 'Possibly'
    >>> browser.getControl(name='irbApproval').value = 'Potentially'
    >>> browser.getControl(name='originalIRBApprovalDate_year').displayValue = [str(yesterday.year)]
    >>> browser.getControl(name='originalIRBApprovalDate_month').value = ['%02d' % yesterday.month]
    >>> browser.getControl(name='originalIRBApprovalDate_day').value = ['%02d' % yesterday.day]
    >>> browser.getControl(name='currentIRBApprovalDate_year').displayValue = [str(tomorrow.year)]
    >>> browser.getControl(name='currentIRBApprovalDate_month').value = ['%02d' % tomorrow.month]
    >>> browser.getControl(name='currentIRBApprovalDate_day').value = ['%02d' % tomorrow.day]
    >>> browser.getControl(name='currentIRBExpirationDate_year').displayValue = [str(dayAfter.year)]
    >>> browser.getControl(name='currentIRBExpirationDate_month').value = ['%02d' % dayAfter.month]
    >>> browser.getControl(name='currentIRBExpirationDate_day').value = ['%02d' % dayAfter.day]
    >>> browser.getControl(name='irbNotes').value = 'The jot utility is used to print out increasing, decreasing, random, ...'
    >>> browser.getControl(name='irbNumber').value = '3'
    >>> browser.getControl(name='siteRoles:lines').value = 'Reference\nAnalysis Lab'
    >>> browser.getControl(name='reportingStage').value = 'Lab Processing Stage'
    >>> browser.getControl(name='form.button.save').click()
    >>> 'mk-ultra' in f.objectIds()
    True
    >>> mku = f['mk-ultra']
    >>> mku.title
    'MK Ultra'
    >>> mku.description
    u'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    >>> mku.identifier
    'http://cia.gov/edrn/mk-ultra'
    >>> mku.abstract
    'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    >>> involvedSites = [i.title for i in mku.involvedInvestigatorSites]
    >>> u"Dr Tongue's 3D Clinic" in involvedSites and u'A Plain 2D Clinic' in involvedSites
    True
    >>> mku.coordinatingInvestigatorSite.title
    u"Dr Tongue's 3D Clinic"
    >>> mku.leadInvestigatorSite.title
    u'A Plain 2D Clinic'
    >>> mku.bmName
    'I had a huge BM once.'
    >>> mku.collaborativeGroupText
    'Sed do eiusmod tempor incididunt ut labore.'
    >>> mku.phasedStatus
    'Stun'
    >>> mku.aims
    'Quis nostrud exercitation ullamco laboris nisi ut aliquip.'
    >>> mku.analyticMethod
    'Duis aute irure dolor in reprehenderit in voluptate velit.'
    >>> mku.blinding
    'AGGH! THE LIGHT!!!1'
    >>> cancerTypes = [i.title for i in mku.cancerTypes]
    >>> cancerTypes.sort()
    >>> cancerTypes
    ['Anal seepage', 'Rectocele']
    >>> mku.comments
    'Eyew.'
    >>> mku.dataSharingPlan
    'For each operand that names a file of a type other than directory.'
    >>> mku.inSituDataSharingPlan
    'The dd utility copies the standard input to the standard output.'
    >>> mku.startDate.year() == yesterday.year
    True
    >>> mku.startDate.month() == yesterday.month
    True
    >>> mku.startDate.day() == yesterday.day
    True
    >>> mku.estimatedFinishDate.year() == tomorrow.year
    True
    >>> mku.estimatedFinishDate.month() == tomorrow.month
    True
    >>> mku.estimatedFinishDate.day() == tomorrow.day
    True
    >>> mku.finishDate.year() == dayAfter.year
    True
    >>> mku.finishDate.month() == dayAfter.month
    True
    >>> mku.finishDate.day() == dayAfter.day
    True
    >>> mku.design
    'Sunt in culpa qui officia deserunt mollit anim id est laborum.'
    >>> mku.fieldOfResearch
    ('3', '14', '7')
    >>> mku.abbrevName
    'MKU'
    >>> mku.objective
    'The cat utility reads files sequentially, writing them to standard output.'
    >>> mku.project
    False
    >>> mku.protocolType
    'Silly'
    >>> pubTitles = [i.title for i in mku.publications]
    >>> pubTitles.sort()
    >>> pubTitles
    ['Glazed Roast Chicken', 'Teriyaki Beef']
    >>> mku.outcome
    "Tar is short for ``tape archiver'', so named for historical reasons."
    >>> mku.secureOutcome
    'OpenSSL is a cryptography toolkit.'
    >>> mku.plannedSampleSize
    '156'
    >>> mku.finalSampleSize
    '0'
    >>> mku.animalSubjectTraining
    'Maybe'
    >>> mku.humanSubjectTraining
    'Possibly'
    >>> mku.irbApproval
    'Potentially'
    >>> mku.originalIRBApprovalDate.year() == yesterday.year
    True
    >>> mku.originalIRBApprovalDate.month() == yesterday.month
    True
    >>> mku.originalIRBApprovalDate.day() == yesterday.day
    True
    >>> mku.currentIRBApprovalDate.year() == tomorrow.year
    True
    >>> mku.currentIRBApprovalDate.month() == tomorrow.month
    True
    >>> mku.currentIRBApprovalDate.day() == tomorrow.day
    True
    >>> mku.currentIRBExpirationDate.year() == dayAfter.year
    True
    >>> mku.currentIRBExpirationDate.month() == dayAfter.month
    True
    >>> mku.currentIRBExpirationDate.day() == dayAfter.day
    True
    >>> mku.irbNotes
    'The jot utility is used to print out increasing, decreasing, random, ...'
    >>> mku.irbNumber
    '3'
    >>> mku.siteRoles
    ('Reference', 'Analysis Lab')
    >>> mku.reportingStage
    'Lab Processing Stage'
    >>> len(mku.piUID()) > 20
    True

Notice that the description is the same as the abstract?  That's thanks to
CA-586, which copies the abstract text to the description field (unless there
is no abstract text, then it tries the objective text, aims text, and outcome
text).  Notice also that the lead investigator's UID was set; that was thanks
to CA-604 which wanted PIs to appear in the folder view (more on that below).


Documentation Contained in Protocols
''''''''''''''''''''''''''''''''''''

CA-583 mandated that Protocols could contain and display various files (like
PDF protocol documents), images, and pages.  Can they?  First off, let's visit
the protocol we created and ensure it has *no* documentation at all yet::

    >>> browser.open(portalURL + '/questionable-studies/mk-ultra')
    >>> 'Documentation' in browser.contents
    False

OK, all clear.  Let's add a file::

    >>> import cStringIO, base64
    >>> fakeFile = cStringIO.StringIO('%PDF-1.3\n% No really, this is a PDF.\n%%EOF')
    >>> browser.open(portalURL + '/questionable-studies/mk-ultra')
    >>> l = browser.getLink(id='file')
    >>> l.url.endswith('createObject?type_name=File')
    True
    >>> l.click()
    >>> browser.getControl(name='title').value = u'How to Poison Millions'
    >>> browser.getControl(name='description').value = u'An IRB-less guide.'
    >>> browser.getControl(name='file_file').add_file(fakeFile, 'application/pdf', 'poisoning.pdf')
    >>> browser.getControl(name='form.button.save').click()

And an image::

    >>> fakeImage = cStringIO.StringIO(base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=='))
    >>> browser.open(portalURL + '/questionable-studies/mk-ultra')
    >>> l = browser.getLink(id='image')
    >>> l.url.endswith('createObject?type_name=Image')
    True
    >>> l.click()
    >>> browser.getControl(name='title').value = u'Injection Site'
    >>> browser.getControl(name='description').value = u'Photograph showing where secret injections should be administered.'
    >>> browser.getControl(name='image_file').add_file(fakeImage, 'image/png', 'injection.png')
    >>> browser.getControl(name='form.button.save').click()

And a plain old web page::

    >>> browser.open(portalURL + '/questionable-studies/mk-ultra')
    >>> l = browser.getLink(id='document')
    >>> l.url.endswith('createObject?type_name=Document')
    True
    >>> l.click()
    >>> browser.getControl(name='title').value = u'Avoiding Capture'
    >>> browser.getControl(name='description').value = u'How to avoid getting caught.'
    >>> browser.getControl(name='text').value = u'<p>First, hide really, <em>really</em>, well.</p>'
    >>> browser.getControl(name='form.button.save').click()

If we now visit the original protocol, we should see links to these items
prominently displayed::

    >>> browser.open(portalURL + '/questionable-studies/mk-ultra')
    >>> browser.contents
    '...Documentation...avoiding-capture...how-to-poison-millions...injection-site...'

Works great!


Team Projects
'''''''''''''

Apparently, some protocols are so perilous, so dicey, so dangerously hard to
execute that they gain the distinction of being not just mere protocols, but
*Team Projects*, requiring an entire squad of intrepid researchers.

What does that mean for protocols?  Not much, luckily.  In fact, protocols
already have a field "project" that indicates if they're a team project or a
mere protocol::

    >>> browser.open(portalURL + '/questionable-studies/mk-ultra')
    >>> 'Team Project' in browser.contents
    False
    >>> browser.getLink('Edit').click()
    >>> browser.getControl('Project?').selected = True
    >>> browser.getControl(name='form.button.save').click()
    >>> 'Team Project' in browser.contents
    True


Inter-Protocol Relationships
''''''''''''''''''''''''''''

One protocol may be related to another in various ways.  Let's create a second
protocol so we can test these relationships::

    >>> browser.open(portalURL + '/questionable-studies')
    >>> browser.getLink(id='protocol').click()
    >>> browser.getControl(name='title').value = 'MK Super Ultra'
    >>> browser.getControl(name='identifier').value = 'http://cia.gov/edrn/mk-super-ultra'
    >>> browser.getControl(name='abstract').value = 'Huh?'
    >>> browser.getControl(name='isAPilotFor:list').displayValue = ['MK Ultra']
    >>> browser.getControl(name='obtainsData:list').displayValue = ['MK Ultra']
    >>> browser.getControl(name='providesData:list').displayValue = ['MK Ultra']
    >>> browser.getControl(name='obtainsSpecimens:list').displayValue = ['MK Ultra']
    >>> browser.getControl(name='providesSpecimens:list').displayValue = ['MK Ultra']
    >>> browser.getControl(name='relatedProtocols:list').displayValue = ['MK Ultra']
    >>> browser.getControl(name='form.button.save').click()
    >>> mksu = f['mk-super-ultra']
    >>> mksu.isAPilotFor[0] == mku
    True
    >>> mksu.obtainsData[0] == mku
    True
    >>> mksu.providesData[0] == mku
    True
    >>> mksu.obtainsSpecimens[0] == mku
    True
    >>> mksu.providesSpecimens[0] == mku
    True
    >>> mksu.relatedProtocols[0] == mku
    True


Protocol View
~~~~~~~~~~~~~

According to http://oodt.jpl.nasa.gov/jira/browse/CA-422, the lead and
coordinating investigating sites should show the sites' PIs, not the name of
the site.  Does it?  Let's find out::

    >>> browser.open(portalURL + '/questionable-studies/mk-ultra')
    >>> browser.contents
    '...Lead Investigator...Alottaspank, Dirk...Coordinating Investigator...Cusexijilomimi, Crystal Hotstuff...'

And according to http://oodt.jpl.nasa.gov/jira/browse/CA-436, it should also
the site names of the lead and coordinating investigators (title of the issue
notwithstanding).  Checking::

    >>> browser.contents
    '...Lead Investigator...Alottaspank...A Plain 2D Clinic...Coordinating Investigator...Cusexijilomimi...Dr Tongue...'
    
Works great!  Also, CA-659 wants the protocol ID on the view::

    >>> browser.contents
    '...Protocol ID:...mk-ultra...'

Also works great.

CA-1122 wants non-EDRN protocols to display a warning to that effect::

    >>> browser.open(portalURL + '/questionable-studies')
    >>> browser.getLink(id='protocol').click()
    >>> browser.getControl(name='title').value = 'The Outsiders'
    >>> browser.getControl(name='identifier').value = 'http://edrn.nci.nih.gov/data/protocols/23456'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.contents
    '...Not an EDRN Protocol...'

It knows it's not an EDRN protocol because the last component of the
identifier is a number ≥ 1000.


Study Folder View
~~~~~~~~~~~~~~~~~

The study folder-by default-displays protocols in alphabetical order by name.
Checking that::

    >>> browser.open(portalURL + '/questionable-studies')
    >>> browser.contents
    '...MK Super Ultra...MK Ultra...'

Of course, the user can sort by clicking on the column headings.

Additionally, any nested study folders should appear above the list of protocols::

    >>> 'Special Subsection' not in browser.contents
    True
    >>> browser.getLink(id='study-folder').click()
    >>> browser.getControl(name='title').value = u'Special Subsection on Morally Dubious Protocols'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/questionable-studies')
    >>> browser.contents
    '...Special Subsection...MK Super Ultra...MK Ultra...'

Further, the list of studies should include abstracts next to each one, but
truncated beyond a certain length::

    >>> 'Ut enim ad minim veniam, quis ...' in browser.contents
    True

CA-604 says we should also show the PI names for each protocol.  Do we?  Take
a look::

    >>> browser.contents
    '...MK Super Ultra...Not listed...MK Ultra...Alottaspank...'

Study folders should also support pagination.  Let's add a huge wad of
protocols to our folder and see if it paginates::

    >>> for i in xrange(0, 40):
    ...     browser.open(portalURL + '/questionable-studies')
    ...     browser.getLink(id='protocol').click()
    ...     browser.getControl(name='title').value = 'Protocol %d' % i
    ...     browser.getControl(name='identifier').value = 'http://great-protocols.com/protocols/%d' % i
    ...     browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/questionable-studies')
    >>> browser.contents
    '...Next...13...items...'


RDF Ingestion
-------------

Study folders support a URL-callable method that causes them to ingest content
via RDF, just like Knowledge Folders in the ``eke.knowledge`` package.

First, let's make a brand new folder in which to experiment::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='study-folder').click()
    >>> browser.getControl(name='title').value = 'Annoying Studies'
    >>> browser.getControl(name='rdfDataSource').value = u'testscheme://localhost/protocols/a'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/annoying-studies/content_status_modify?workflow_action=publish')
    >>> f = portal['annoying-studies']

Ingesting from the RDF data source ``testscheme://localhost/studies/a``::

    >>> browser.open(portalURL + '/annoying-studies/ingest')
    >>> browser.contents
    '...The following items have been created...Public Safety...'
    >>> f.objectIds()
    ['ps-public-safety']
    >>> p1 = f['ps-public-safety']
    >>> p1.title
    'Public Safety'
    >>> p1.identifier
    'http://swa.it/edrn/ps'
    >>> p1.abstract
    'Clinic surveillance and intelligence gathering.'
    >>> involvedSites = [i.title for i in p1.involvedInvestigatorSites]
    >>> u"Dr Tongue's 3D Clinic" in involvedSites and u'A Plain 2D Clinic' in involvedSites
    True
    >>> p1.coordinatingInvestigatorSite.title
    u"Dr Tongue's 3D Clinic"
    >>> p1.leadInvestigatorSite.title
    u'A Plain 2D Clinic'
    >>> p1.bmName
    'Federico.'
    >>> p1.collaborativeGroupText
    'Works with the Special Ops group.'
    >>> p1.phasedStatus
    'Stun'
    >>> p1.aims
    'Gather intelligence and do surveillance.'
    >>> p1.analyticMethod
    'Top secret.'
    >>> p1.blinding
    'Pepper spray'
    >>> p1.cancerTypes[0].title
    'Anal seepage'
    >>> p1.comments
    'Ugh.'
    >>> p1.dataSharingPlan
    'We will be very open with our data.'
    >>> p1.inSituDataSharingPlan
    'No data may be shared.'
    >>> p1.startDate.year(), p1.startDate.month(), p1.startDate.day()
    (1967, 12, 21)
    >>> p1.estimatedFinishDate.year(), p1.estimatedFinishDate.month(), p1.estimatedFinishDate.day()
    (2029, 6, 15)
    >>> p1.finishDate.year(), p1.finishDate.month(), p1.finishDate.day()
    (2011, 11, 6)
    >>> p1.design
    'Pair fratelli with cyborg girls with night-vision goggles.'
    >>> '3' in p1.fieldOfResearch and '14' in p1.fieldOfResearch and '7' in p1.fieldOfResearch
    True
    >>> p1.abbrevName
    'PS'
    >>> p1.objective
    'Track terrorist activity.'
    >>> p1.project
    False
    >>> p1.protocolType
    'Fictional'
    >>> p1.publications[0].title
    'Teriyaki Beef'
    >>> p1.outcome
    'Increased public safety.'
    >>> p1.secureOutcome
    'Better control of the citizenry.'
    >>> p1.plannedSampleSize
    '12'
    >>> p1.finalSampleSize
    '48'
    >>> p1.animalSubjectTraining
    'No'
    >>> p1.humanSubjectTraining
    'No'
    >>> p1.irbApproval
    'No'
    >>> p1.originalIRBApprovalDate.year(), p1.originalIRBApprovalDate.month(), p1.originalIRBApprovalDate.day()
    (1963, 2, 28)
    >>> p1.currentIRBApprovalDate.year(), p1.currentIRBApprovalDate.month(), p1.currentIRBApprovalDate.day()
    (1963, 9, 27)
    >>> p1.currentIRBExpirationDate.year(), p1.currentIRBExpirationDate.month(), p1.currentIRBExpirationDate.day()
    (1964, 2, 26)
    >>> p1.irbNotes
    'IRB?'
    >>> p1.irbNumber
    'SECRET'
    >>> p1.siteRoles
    ('Consultant',)
    >>> p1.reportingStage
    'Other, specify'

The source ``testscheme://localhost/protocols/b`` contains a Special Ops
protocol which is related to the Public Safety protocol::

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='rdfDataSource').value = 'testscheme://localhost/protocols/b'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.getLink('Ingest').click()
    >>> objIDs = f.objectIds()
    >>> objIDs.sort()
    >>> objIDs
    ['ps-public-safety', 'so-special-ops']
    
Testing the relations::

    >>> p1, p2 = f['ps-public-safety'], f['so-special-ops']
    >>> browser.open(portalURL + '/annoying-studies/so-special-ops')
    >>> p2.isAPilotFor[0] == p1
    True
    >>> p2.obtainsData[0] == p1
    True
    >>> p2.providesData[0] == p1
    True
    >>> p2.obtainsSpecimens[0] == p1
    True
    >>> p2.providesSpecimens[0] == p1
    True
    >>> p2.relatedProtocols[0] == p1
    True

CA-583 added the ability for images, files, and pages to be added as
documentation to protocols.  These additions don't come through the RDF,
however.  They're instead added on the portal side.  Let's add some
documentation to the Special Ops protocol::

    >>> browser.open(portalURL + '/annoying-studies/so-special-ops')
    >>> browser.getLink(id='document').click()
    >>> browser.getControl(name='title').value = u'What "Special" Means'
    >>> browser.getControl(name='description').value = u'An explanation.'
    >>> browser.getControl(name='text').value = u'<p>Lorem ipsum dolor sit amet.</p>'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/annoying-studies/so-special-ops')
    >>> browser.contents
    '...Documentation...what-special-means...'

Great. Now if we re-ingest, is our documentation preserved?

    >>> browser.open(portalURL + '/annoying-studies/ingest')
    >>> browser.open(portalURL + '/annoying-studies/so-special-ops')
    >>> browser.contents
    '...Documentation...what-special-means...'

That would be a yes.    

http://oodt.jpl.nasa.gov/jira/browse/CA-472 reveals that RDF from the DMCC
doesn't contain plain text, but HTML markup.  Sigh.  Let's see if we deal with
that appropriately.  This new data source contains some nasty markup::

    >>> browser.open(portalURL + '/annoying-studies/edit')
    >>> browser.getControl(name='rdfDataSource').value = 'testscheme://localhost/protocols/c'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.getLink('Ingest').click()
    >>> browser.open(portalURL + '/annoying-studies/so-barretts-esophagus-methylation-profiles')
    >>> 'Barrett&#39;s Esophagus' not in browser.contents
    True
    >>> "Barrett's Esophagus" in browser.contents
    True
    >>> "Barrett's abbreviated <strong>Esophagus</strong>" in browser.contents
    True

Meanwhile, CA-586 says when we look at a study folder the list of protocols
should show at least some text under the abstract column.  If a protocol
doesn't have any abstract text, we should then use the aims text, and if
that's empty, the analytic methods text.

Let's take a look.  First, let's make up a brand new study folder:

    >>> browser.open(portalURL)
    >>> browser.getLink(id='study-folder').click()
    >>> browser.getControl(name='title').value = u'Abstracted Studies'
    >>> browser.getControl(name='description').value = u'This folder is to reveal bugs.'
    >>> browser.getControl(name='rdfDataSource').value = u'testscheme://localhost/protocols/d'
    >>> browser.getControl(name='form.button.save').click()

Now we'll ingest from its "d" data source::

    >>> browser.getLink('Ingest').click()

That "d" data source has four protocols in it, each with less and less
information.  Protocol 1 has an abstract, objective, aims, and an outcome.
Protocol 2 loses the abstract but has the objective, aims, and outcome.
Protocol 3 drops the objective.  And protocol 4 drops the aims, leaving only
the outcome.  All four protocols should show some text from each of those
sections, though.

Does it work?  Let's check::

    >>> browser.open(portalURL + '/abstracted-studies')
    >>> browser.contents
    '...Protocol Four...Finally, an outcome!...Protocol One...Abstract...Protocol Three...Aims...Protocol Two...Objective...'

I'd say CA-586 is *fixed*.


Searching
~~~~~~~~~

Issue http://oodt.jpl.nasa.gov/jira//browse/CA-523 says we need to be able to
search by a protocol's abbreviated name.  Does that work?  Let's find out::

    >>> browser.open(portalURL + '/search?SearchableText=abbreviated')
    >>> browser.contents
    '...Esophagus Methylation Profiles...'

Works!  How about biomarker name?

    >>> browser.open(portalURL + '/search?SearchableText=Hidalgo')
    >>> browser.contents
    '...Esophagus Methylation Profiles...'

Great!  How about PI name?

    >>> browser.open(portalURL + '/search?SearchableText=Alottaspank')
    >>> browser.contents
    '...Esophagus Methylation Profiles...'

Fantastic!  How about collaborative group text?

    >>> browser.open(portalURL + '/search?SearchableText=Mankind')
    >>> browser.contents
    '...Esophagus Methylation Profiles...'

Woot!  How about involved investigator sites?

    >>> browser.open(portalURL + '/search?SearchableText=Tongue')
    >>> browser.contents
    '...Esophagus Methylation Profiles...'


Duplicates
~~~~~~~~~~

CA-978 noticed that the DMCC started outputting protocols with duplicate
titles in its RDF output.  This causes this package's protocol vocabulary to
choke, since it used to require unique titles.  But not any more, watch::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='study-folder').click()
    >>> browser.getControl(name='title').value = u'Duplicated Studies'
    >>> browser.getControl(name='description').value = u'This folder is to reveal bugs.'
    >>> browser.getControl(name='rdfDataSource').value = u'testscheme://localhost/protocols/dups'
    >>> browser.getControl(name='form.button.save').click()

Now we'll ingest from its "dups" data source::

    >>> browser.getLink('Ingest').click()

That "dups" data source has two protocols in it with identical titles.  Yet,
as you can see, they ingested just fine::

    >>> dups = portal['duplicated-studies']
    >>> keys = dups.keys()
    >>> keys.sort()
    >>> keys
    ['1-a-duplicate-title', '2-a-duplicate-title']

We can also edit one of them and not get a stack trace::

    >>> browser.open(portalURL + '/duplicated-studies/1-a-duplicate-title')
    >>> browser.getLink('Edit').click()

All better.



RDF Data Sources
~~~~~~~~~~~~~~~~

The URL to an RDF data source is nominally displayed on a study folder::

    >>> browser.open(portalURL + '/annoying-studies')
    >>> browser.contents
    '...RDF Data Source...testscheme://localhost/protocols/c...'

That shows up because we're logged in as an administrator.  Mere mortals
shouldn't see that::

    >>> unprivilegedBrowser.open(portalURL + '/annoying-studies')
    >>> 'RDF Data Source' not in unprivilegedBrowser.contents
    True

That's it!


.. References:
.. _EKE: http://cancer.jpl.nasa.gov/documents/applications/knowledge-environment
.. _RDF: http://w3.org/RDF/
.. _URI: http://w3.org/Addressing/
