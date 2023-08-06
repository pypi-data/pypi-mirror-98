from paver.easy import *
from paver.setuputils import setup

options = environment.options

NAME = 'pinkbelt'
VERSION = '0.16.1'

requires = ['six', 'click', 'requests', 'PyGithub', 'slacker>=0.6.2', 'pyopenssl', 'ndg-httpsclient', 'pyasn1', 'twine']

setup(
    name=NAME,
    version=VERSION,
    description='Opinionated Product Development Automation',
    long_description="""
    # Pink Belt: Opinionated Product Development Automation

    Integrates useful GitHub workflow with Trello and Slack.
    """,
    long_description_content_type = "text/markdown",
    author='Lukas Linhart',
    author_email='bugs@almad.net',
    url='http://github.com/Almad/pink-belt',
    license='MIT',
    packages=[NAME, NAME + '.apis', NAME + '.commands'],
    install_requires=requires,
    # requires=requires,
    tests_require=['nose', 'virtualenv'],
    test_suite='nose.collector',
    zip_safe=False,
    # Yes, entry_points are nice and shiny and should be used in 21st century
    # Unfortunately, having some dependencies, the load_entry_point in the ge-
    # nerated console script blows up with pkg_resources.DistributionNotFound: requests
    # if it was installed with pip.
    # Pradoxically, solution is to easy_install -U all the dependencies.
    # Therefore, just fall back to the good, old, simple disutils script that works.
    scripts=['distutils_scripts/bb'],
    # entry_points={
    #     'console_scripts': [
    #         'bb = pinkbelt.tasks:main'
    #     ]
    # },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Environment :: Console",
        "Topic :: Documentation",
        "Topic :: Utilities",
        "Topic :: Software Development :: Build Tools",
    ]
)

options.setup.package_data = paver.setuputils.find_package_data("pinkbelt", package="pinkbelt",
                                                only_in_packages=False)


@task
@consume_args
def bump(args):
    version = list(map(int, VERSION.split('.')[0:3]))

    if len(args) > 0 and args[0] == 'major':
        version[1] += 1
        version[2] = 0
    else:
        version[2] += 1

    version = list(map(str, version))

    module_content = "VERSION='%s'\n" % '.'.join(version)

    # bump version in pinkbelt
    with open(path('pinkbelt/version.py'), 'w') as f:
        f.write(module_content)

    # bump version in sphinx
    conf = []
    with open(path('docs/source/conf.py'), 'r') as f:
        for line in f.readlines():
            if line.startswith('version = '):
                line = "version = '%s'\n" % '.'.join(version[0:2])
            elif line.startswith('release = '):
                line = "release = '%s'\n" % '.'.join(version[0:3])

            conf.append(line)

    with open(path('docs/source/conf.py'), 'w') as f:
        f.writelines(conf)

    # bump version in this pavement file itself
    # we cannot just import it because it implies pinkbelt already been
    # installed/in path, which may cause some interesting problems
    # solvable by mangling with sys.path, but this just feels...better
    conf = []
    with open(path('./pavement.py'), 'r') as f:
        for line in f.readlines():
            if line.startswith('VERSION = '):
                line = "VERSION = '%s'\n" % '.'.join(version)

            conf.append(line)

    with open(path('./pavement.py'), 'w') as f:
        f.writelines(conf)

    sh("git commit pavement.py pinkbelt/version.py docs/source/conf.py -m 'Version bump to %s'" % '.'.join(version))


@task
def release():
    sh("git tag -s '%(name)s-%(version)s' -m 'Version bump to %(version)s'" % {'name': NAME, 'version': VERSION})
    sh("git push --tags")
    sh("git push")
    sh("python setup.py sdist bdist_wheel")
    sh("twine upload dist/*%s*" % VERSION)
