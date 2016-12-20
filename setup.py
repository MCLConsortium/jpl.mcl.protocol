# encoding: utf-8
# Copyright 2008-2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from setuptools import setup, find_packages
from ConfigParser import SafeConfigParser
import os.path

# Package data
# ------------

_name            = 'jpl.mcl.protocol'
_version         = '0.0.2'
_description     = 'JPL MCL Protocol Server'
_author          = 'David Liu'
_authorEmail     = 'david.liu@jpl.nasa.gov'
_maintainer      = 'David Liu'
_maintainerEmail = 'david.liu@jpl.nasa.gov'
_license         = 'ALv2'
_namespaces      = ['jpl', 'jpl.mcl']
_zipSafe         = False
_keywords        = 'JPL MCL Protocol web zope plone cancer bioinformatics detection informatics edrn'
_testSuite       = 'jpl.mcl.protocol.tests.test_suite'
_entryPoints     = {
    'z3c.autoinclude.plugin': ['target=plone'],
}
_requirements = [
    'collective.autopermission',
    'Pillow',
    'plone.app.dexterity [grok, relations]',
    'z3c.relationfield',
    'plone.app.relationfield',
    'plone.rest',
    'plone.behavior',
    'Products.CMFPlone',
    'rdflib',
    'jsonlib',
    'mygene',
    'requests',
    'biopython',
    'setuptools',
    'z3c.suds',
]
_extras = {
    'test': ['plone.app.testing', 'rdfextras'],
}
_name        = 'jpl.mcl.protocol'
_version     = '0.0.2'
_description = 'Study and protocol information for the MCL'
_author      = 'Sean Kelly'
_authorEmail = 'sean.kelly@jpl.nasa.gov'
_license     = 'ALv2'
_namespaces  = ['jpl.mcl']
_zipSafe     = False
_keywords    = 'web zope plone edrn cancer biomarkers jpl.mcl.protocol protocol'
_entryPoints = {
    'z3c.autoinclude.plugin': ['target=plone'],
}
_extras = {
    'test': ['plone.app.testing'],
}
_externalRequirements = [
    'setuptools',
    'Products.CMFPlone',
    'eke.knowledge',
    'eke.site',
    'eke.publications',
    'eke.biomarker',
    'eke.ecas',
    'zope.globalrequest',
    'z3c.autoinclude',
]
_classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Framework :: Plone',
    'Intended Audience :: Healthcare Industry',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'License :: Other/Proprietary License',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

# Setup Metadata
# --------------

def _read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

_header = '*' * len(_name) + '\n' + _name + '\n' + '*' * len(_name)
_longDescription = _header + '\n\n' + _read('README.rst') + '\n\n' + _read('docs', 'INSTALL.txt') + '\n\n' \
    + _read('docs', 'HISTORY.txt') + '\n'
open('doc.txt', 'w').write(_longDescription)
_cp = SafeConfigParser()
_cp.read([os.path.join(os.path.dirname(__file__), 'setup.cfg')])
_reqs = _externalRequirements + _cp.get('source-dependencies', 'eggs').strip().split()

setup(
    author=_author,
    author_email=_authorEmail,
    classifiers=_classifiers,
    description=_description,
    entry_points=_entryPoints,
    extras_require=_extras,
    include_package_data=True,
    install_requires=_requirements,
    keywords=_keywords,
    license=_license,
    long_description=_longDescription,
    maintainer=_maintainer,
    maintainer_email=_maintainerEmail,
    name=_name,
    namespace_packages=_namespaces,
    packages=find_packages(exclude=['ez_setup', 'distribute_setup', 'bootstrap']),
    url='https://github.com/EDRN/' + _name,
    install_requires=_reqs,
    keywords=_keywords,
    license=_license,
    long_description=_longDescription,
    name=_name,
    namespace_packages=_namespaces,
    packages=find_packages(exclude=['ez_setup']),
    url='https://github.com/MCLConsortium/' + _name,
    version=_version,
    zip_safe=_zipSafe,
)
