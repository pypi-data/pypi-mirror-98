

from setuptools import find_packages, setup

from djangocms_googlecalendar_plugin import __version__


REQUIREMENTS = [
    'django-cms',
    # 'django-filer'
]


CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: Software Development :: Libraries :: Python Modules',
]


setup(
    name='djangocms-googlecalendar-plugin',
    # packages = ['djangocms-googlecalendar-plugin'], 
    version=__version__,
    author='Shawn Hartley',
    author_email='shawn@novusterra.com',
    url='https://github.com/thegrapesofwrath/djangocms-googlecalendar-plugin',
    license='GNU General Public License v3 (GPLv3), see LICENSE.md',
    description='Adds Google Calendar plugins to django CMS.',
    long_description=open('README.md').read(),
    long_description_content_type = 'text/markdown',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    test_suite='tests.settings.run',
)

