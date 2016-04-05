This package provides an RDF-based web service that describes the knowledge
assets of the Early Detection Research Network (EDRN).


Functional Tests
================

To demonstrate the code, we'll classes in a series of functional tests.  And
to do so, we'll need a test browser::

    >>> app = layer['app']
    >>> from plone.testing.z2 import Browser
    >>> from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD
    >>> browser = Browser(app)
    >>> browser.handleErrors = False
    >>> browser.addHeader('Authorization', 'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD))
    >>> portal = layer['portal']    
    >>> portalURL = portal.absolute_url()

Here we go.


RDF Source
==========

An RDF Source is a source of RDF data.  They can be added anywhere in the
portal::


    >>> browser.open(portalURL)
    >>> l = browser.getLink(id='edrn-summarizer-summarizersource')
    >>> l.url.endswith('++add++edrn.summarizer.summarizersource')
    True
    >>> l.click()
    >>> browser.getControl(name='form.widgets.title').value = u'A Simple Source'
    >>> browser.getControl(name='form.widgets.description').value = u"It's just for functional tests."
    >>> browser.getControl(name='form.widgets.active:list').value = False
    >>> browser.getControl(name='form.buttons.save').click()
    >>> 'a-simple-source' in portal.keys()
    True
    >>> source = portal['a-simple-source']
    >>> source.title
    u'A Simple Source'
    >>> source.description
    u"It's just for functional tests."
    >>> source.active
    False

Now, these things are supposed to produce RDF when called with the appropriate
view.  Does it?

    >>> browser.open(portalURL + '/a-simple-source/@@rdf')
    Traceback (most recent call last):
    ...
    ValueError: The Summarizer Source at /plone/a-simple-source does not have an active Summarizer file to send

It doesn't because it hasn't yet made any RDF files to send, and it can't do
that without an RDF generator.  RDF Sources get their data from RDF
Generators.


RDF Generators
==============

RDF Generators have the responsibility of accessing various sources of data
(notably the DMCC's web service) and yielding an RDF graph, suitable for
serializing into XML or some other format.  There are several kinds available.


Null RDF Generator
------------------

One such generator does absolutely nothing: it's the Null RDF Generator, and
all it ever does it make zero statements about anything.  It's not very
useful, but it's nice to have for testing.  Check it out::

    >>> browser.open(portalURL)
    >>> l = browser.getLink(id='edrn-summarizer-nullrdfgenerator')
    >>> l.url.endswith('++add++edrn.summarizer.nullrdfgenerator')
    True
    >>> l.click()
    >>> browser.getControl(name='form.widgets.title').value = u'Silence'
    >>> browser.getControl(name='form.widgets.description').value = u'Just for testing.'
    >>> browser.getControl(name='form.buttons.save').click()
    >>> 'silence' in portal.keys()
    True
    >>> generator = portal['silence']
    >>> generator.title
    u'Silence'
    >>> generator.description
    u'Just for testing.'

We'll set up our RDF source with this generator (and hand-craft the POST
because it's AJAX)::

    >>> from urllib import urlencode
    >>> browser.open(portalURL + '/a-simple-source/edit')
    >>> postParams = {
    ...     'form.widgets.title': source.title,
    ...     'form.widgets.description': source.description,
    ...     'form.widgets.generator:list': '/plone/silence',
    ...     'form.buttons.save': 'Save',
    ... }
    >>> if source.active: postParams['form.widgets.active:list'] = 'selected'
    >>> browser.post(portalURL + '/a-simple-source/@@edit', urlencode(postParams))
    >>> source.generator.to_object.title
    u'Silence'
    >>> browser.open(portalURL + '/a-simple-source')
    >>> browser.contents
    '...Generator...href="http://nohost/plone/silence"...Silence...'

The RDF source still doesn't produce any RDF, though::

    >>> browser.open(portalURL + '/a-simple-source/@@rdf')
    Traceback (most recent call last):
    ...
    ValueError: The Summarizer Source at /plone/a-simple-source does not have an active Summarizer file to send

That's because having the generator isn't enough.  Someone has to actually
*run* the generator.


Running the Generators
----------------------

Tickled by either a cron job or a Zope clock event, a special URL finds every
RDF source and asks it to run its generator to produce a fresh update.  Each
RDF source may (in the future) run its validators against the generated graph
to ensure it has the expected information.  Assuming it passes muster, the
source then saves that output as the latest and greatest RDF to deliver when
demanded.

Tickling::

    >>> browser.open(portalURL + '/@@updateJSON')

And is there any RDF?  Let's check::

    >>> browser.open(portalURL + '/a-simple-source/@@rdf')
    Traceback (most recent call last):
    ...
    ValueError: The Summarizer Source at /plone/a-simple-source does not have an active Summarizer file to send

Still no RDF?!  Right, because RDF Sources can be active or not.  If they're
active, then when it's time to generate RDF their generator will actually get
run.  But the source "A Simple Source" is *not* active.  We didn't check the
active box when we made it.  So, let's fix that and re-tickle::

    >>> browser.open(portalURL + '/a-simple-source/edit')
    >>> browser.getControl(name='form.widgets.active:list').value = True
    >>> browser.getControl(name='form.buttons.save').click()
    >>> browser.open(portalURL + '/@@updateJSON')
    >>> browser.contents
    '...Sources updated:...<span id="numberSuccesses">0</span>...'

To be continued, need to add more tests, the simple test is not working!!
