import io

from setuptools import setup, find_packages


def readme():
    with io.open('README.md', encoding='utf-8') as f:
        return f.read()

def requirements(filename):
    reqs = list()
    with io.open(filename, encoding='utf-8') as f:
        for line in f.readlines():
            reqs.append(line.strip())
    return reqs

setup(
    name='finnomena_api',
    version='1.0.0',
    packages=find_packages(),
    url='https://github.com/phachara-laohrenu/finnomena-api-unofficial',
    license='MIT License',
    author='Phachara Laohrenu',
    author_email='phachara.lahorenu@gmail.com',
    description='An unofficial API for finnomena.com',
    long_description=readme(),
    long_description_content_type='text/markdown',
    install_requires=requirements(filename='requirements.txt'),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries"
    ],
    python_requires='>=3.6',

    keywords=', '.join([
        'investing', 'investing-api', 'historical-data',
        'financial-data', 'funds'
    ]),
    project_urls={
        'Bug Reports': 'https://github.com/phachara-laohrenu/finnomena-api-unofficial/issues',
        'Source': 'https://github.com/phachara-laohrenu/finnomena-api-unofficial',
    },
)