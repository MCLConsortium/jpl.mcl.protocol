# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from eke.knowledge.testing import EKE_KNOWLEDGE_FIXTURE
from eke.publications.testing import EKE_PUBLICATIONS_FIXTURE
from eke.site.testing import EKE_SITE_FIXTURE
from plone.app.testing import PloneSandboxLayer, IntegrationTesting, FunctionalTesting
from plone.testing import z2

class EKEStudy(PloneSandboxLayer):
    # defaultBases = (EKE_SITE_FIXTURE, EKE_PUBLICATIONS_FIXTURE, EKE_KNOWLEDGE_FIXTURE)
    defaultBases = (EKE_KNOWLEDGE_FIXTURE,)
    def setUpZope(self, app, configurationContext):
        import eke.study
        self.loadZCML(package=eke.study)
        z2.installProduct(app, 'eke.study')

        # No idea why we can't just include these packages as defaultBases.
        import eke.site
        self.loadZCML(package=eke.site)
        z2.installProduct(app, 'eke.site')
        import eke.publications
        self.loadZCML(package=eke.publications)
        z2.installProduct(app, 'eke.publications')

        import eke.study.tests.base
        eke.study.tests.base.registerLocalTestData()
    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'eke.study:default')
    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'eke.study')

EKE_STUDY_FIXTURE = EKEStudy()
EKE_STUDY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EKE_STUDY_FIXTURE,),
    name='EKEStudy:Integration',
)
EKE_STUDY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EKE_STUDY_FIXTURE,),
    name='EKEStudy:Functional',
)
