"""
graph-theory
"""
build_tag = "7cf0d10ffa099ef42adc30ca26d0a5be7a2ffff65db4df6b67f17fb6a1c80e2e"
from setuptools import setup
from pathlib import Path


folder = Path(__file__).parent
file = "README.md"
readme = folder / file
assert isinstance(readme, Path)
assert readme.exists(), readme
with open(str(readme), encoding='utf-8') as f:
    long_description = f.read()

keywords = list({
    'complex-networks', 'discrete mathematics', 'graph', 'Graph Theory', 'graph-algorithms', 'graph-analysis',
    'graph-generation', 'graph-theory', 'graph-visualization', 'graphs', 'math', 'Mathematics', 'maths',
    'minimum-spanning-trees', 'network', 'Networks', 'optimization', 'python', 'shortest-path', 'tsp', 'tsp-solver',
    'assignment problem', 'flow-problem', 'hash', 'graph-hash', 'random graph', 'search', 'cycle', 'path',
    'component', 'components', 'adjacency', 'matrix', 'all pairs shortest path', 'finite state machine', 'fsm',
    'traffic-jam', 'traffic-jam-solver', 'solver', 'hill-climbing', 'simple', 'simple-path'
})

keywords.sort(key=lambda x: x.lower())


setup(
    name="graph-theory",
    version="2021.3.15.33896",
    url="https://github.com/root-11/graph-theory",
    license="MIT",
    author="Bjorn Madsen",
    author_email="bjorn.madsen@operationsresearchgroup.com",
    description="A graph library",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=keywords,
    packages=["graph"],
    include_package_data=True,
    data_files=[(".", ["LICENSE", "README.md"])],
    platforms="any",
    install_requires=[],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)


