SETUP_INFO = dict(
    name='getlino',
    version='21.3.1',
    install_requires=['click', 'virtualenv', 'jinja2', 'distro'],
    # tests_require=['docker', 'atelier'],
    # test_suite='tests',
    description="Lino installer",
    long_description="""
A command-line tool to install and configure Lino in different environments.

Note: If you **just want to install** Lino, then this repository is **not for
you**. You want to read the  `Lino book <https://www.lino-framework.org>`__
instead. This repository is for people who want to help with developing the tool
that you use to install Lino.

The project homepage is https://getlino.lino-framework.org

    """,
    author='Rumma & Ko Ltd',
    author_email='team@lino-framework.org',
    url="https://getlino.lino-framework.org",
    license='BSD-2-Clause',
    entry_points={
        'console_scripts': ['getlino = getlino.cli:main']
    },

    classifiers="""\
Programming Language :: Python :: 3
Development Status :: 5 - Production/Stable
Environment :: Console
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
License :: OSI Approved :: BSD License
Operating System :: OS Independent
Topic :: System :: Installation/Setup
Topic :: Software Development :: Libraries :: Python Modules
""".splitlines())

SETUP_INFO.update(
    zip_safe=False,
    include_package_data=True)

SETUP_INFO.update(packages=[n for n in """
getlino
""".splitlines() if n])
