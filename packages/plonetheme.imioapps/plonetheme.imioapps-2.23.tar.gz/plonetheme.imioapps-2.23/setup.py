from setuptools import setup, find_packages

version = '2.23'

long_description = (
    open('README.rst').read()
    + '\n\n' +
    open('CHANGES.rst').read()
    + '\n')

setup(name='plonetheme.imioapps',
      version=version,
      description="Plone theme for most Imio applications",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Topic :: Software Development :: Libraries :: Python Modules"],
      keywords='Plone IMIO',
      author='IMIO team',
      author_email='devs@imio.be',
      url='http://svn.communesplone.org/svn/communesplone/plonetheme.imioapps/',
      license='gpl',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['plonetheme', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'collective.messagesviewlet',
          'imio.helpers',
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      extras_require={'test': ['plone.app.testing']},
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
