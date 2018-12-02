from setuptools import setup, find_packages

try:
    # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:
    # for pip <= 9.0.3
    from pip.req import parse_requirements

install_reqs = parse_requirements("requirements.txt", session=False)
requirements_list = [str(ir.req) for ir in install_reqs]

setup(
    name='fiware-sla',
    version='1.0.0',
    packages=find_packages(exclude=['tests*']),
    install_requires=requirements_list,
    url='https://github.com/flopezag/fiware-sla',
    license='Apache 2.0',
    author='Fernando Lopez',
    keywords=['fiware', 'fiware-ops', 'python2', 'pandas', 'JIRA', 'fiware-lab'],
    author_email='fernando.lopez@fiware.org',
    description='Management of FIWARE Lab nodes help-desk tickets SLA data',
    classifiers=[
                  "License :: OSI Approved :: Apache Software License", ],
)
