from setuptools import setup

setup(
    name='oversnips',
    version='0.0.1',
    packages=['org.oversnips'],
    scripts=['oversnips.py'],
    url='',
    license='',
    author='smile innovation',
    author_email='tech-dir-innovation@smile.fr',
    description='',
    install_requires=[
        "snips-nlu",
	"snips-nlu-metrics",
	"snips-nlu-ontology",
	"snips-nlu-utils",
	"Flask",
	"Flask-RESTful"
    ]
)
