import setuptools

setuptools.setup(name='cropmetapop',
                 version='1.1.2',
                 description='The crop metapopulation modelisation software',
                 url='https://sourcesup.renater.fr/www/cmp/',
                 author='Equipe DEAP',
                 author_email='baptiste.rouger@inra.fr',
                 license='GNU GPL v3',
                 long_description="Please refer to the official website : https://sourcesup.renater.fr/www/cmp/",
                 packages=['cropmetapop'],
                 install_requires=[
                     'simuPOP',
                     'numpy',
                     'python-igraph'
                 ],
                 scripts=['bin/cropmetapop'],
                 zip_safe=False)
