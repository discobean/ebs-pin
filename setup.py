from pip.req import parse_requirements
from setuptools import setup

install_reqs = parse_requirements('requirements.txt', session='hack')
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='ebs-pin',
    version='0.1',
    scripts=['scripts/ebs-pin'],
    packages=['ebspin'],
    install_requires=reqs,
    keywords='ebs ebspin ebs-pin'
)

