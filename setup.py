from setuptools import setup, Command
import site
import os
import platform




class Reusing(Command):
    description = "Fetch remote modules"
    user_options = [
      # The format is (long option, short option, description).
      ( 'local', None, 'Update files without internet'),
  ]

    def initialize_options(self):
        self.local=False

    def finalize_options(self):
        pass

    def run(self):
        from sys import path
        path.append("moneymoney_pl/reusing")
        print(self.local)
        if self.local is False:
            from github import download_from_github
            download_from_github('turulomio','reusingcode','python/github.py', 'moneymoney_pl/reusing/')
            download_from_github('turulomio','reusingcode','python/casts.py', 'moneymoney_pl/reusing/')
            download_from_github('turulomio','reusingcode','python/datetime_functions.py', 'moneymoney_pl/reusing/')
            download_from_github('turulomio','reusingcode','python/listdict_functions.py', 'moneymoney_pl/reusing/')
            download_from_github('turulomio','reusingcode','python/file_functions.py', 'moneymoney_pl/reusing/')
            download_from_github('turulomio','reusingcode','python/decorators.py', 'moneymoney_pl/reusing/')
            download_from_github('turulomio','reusingcode','python/libmanagers.py', 'moneymoney_pl/reusing/')
            download_from_github('turulomio','reusingcode','python/percentage.py', 'moneymoney_pl/reusing/')
            download_from_github('turulomio','reusingcode','python/currency.py', 'moneymoney_pl/reusing/')
        
        from file_functions import replace_in_file
        replace_in_file("moneymoney_pl/reusing/casts.py","from currency","from moneymoney_pl.reusing.currency")
        replace_in_file("moneymoney_pl/reusing/casts.py","from percentage","from moneymoney_pl.reusing.percentage")
        replace_in_file("moneymoney_pl/reusing/listdict_functions.py","from casts","from moneymoney_pl.reusing.casts")


## Class to define doc command
class Translate(Command):
    description = "Update translations"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        #es
        os.system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o locale/moneymoney_pl.pot *.py moneymoney_pl/*.py moneymoney_pl/reusing/*.py setup.py")
        os.system("msgmerge -N --no-wrap -U locale/es.po locale/moneymoney_pl.pot")
        os.system("msgfmt -cv -o moneymoney_pl/locale/es/LC_MESSAGES/moneymoney_pl.mo locale/es.po")
        os.system("msgfmt -cv -o moneymoney_pl/locale/en/LC_MESSAGES/moneymoney_pl.mo locale/en.po")

    
## Class to define doc command
class Documentation(Command):
    description = "Generate documentation for distribution"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system("moneymoney_pl_demo --create")
        os.system("cp -f moneymoney_pl_documentation_en.odt doc/")
        os.system("cp -f moneymoney_pl_documentation_en.pdf doc/")
        os.system("cp -f moneymoney_pl_documentation_es.odt doc/")
        os.system("cp -f moneymoney_pl_documentation_es.pdf doc/")
        os.system("cp -f moneymoney_pl_example_en.ods doc/")
        os.system("cp -f moneymoney_pl_example_en.pdf doc/")
        os.system("cp -f moneymoney_pl_example_es.ods doc/")
        os.system("cp -f moneymoney_pl_example_es.pdf doc/")
        os.system("moneymoney_pl_demo --remove")

class Procedure(Command):
    description = "Show release procedure"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print("""Nueva versión:
  * Cambiar la versión y la fecha en __init__.py
  * Modificar el Changelog en README
  * python setup.py translate
  * linguist
  * python setup.py translate
  * python setup.py uninstall; python setup.py install
  * python setup.py documentation
  * python setup.py doxygen
  * git commit -a -m 'moneymoney_pl-{0}'
  * git push
  * Hacer un nuevo tag en GitHub
  * python setup.py sdist
  * twine upload dist/moneymoney_pl-{0}.tar.gz 
  * python setup.py uninstall
  * Crea un nuevo ebuild de moneymoney_pl Gentoo con la nueva versión
  * Subelo al repositorio del portage

""".format(__version__))

## Class to define doxygen command
class Doxygen(Command):
    description = "Create/update doxygen documentation in doc/html"

    user_options = [
      # The format is (long option, short option, description).
      ( 'user=', None, 'Remote ssh user'),
      ( 'directory=', None, 'Remote ssh path'),
      ( 'port=', None, 'Remote ssh port'),
      ( 'server=', None, 'Remote ssh server'),
  ]

    def initialize_options(self):
        self.user="root"
        self.directory="/var/www/html/doxygen/moneymoney_pl/"
        self.port=22
        self.server="127.0.0.1"

    def finalize_options(self):
        pass

    def run(self):
        print("Creating Doxygen Documentation")
        os.system("""sed -i -e "41d" doc/Doxyfile""")#Delete line 41
        os.system("""sed -i -e "41iPROJECT_NUMBER         = {}" doc/Doxyfile""".format(__version__))#Insert line 41
        os.system("rm -Rf build")
        os.chdir("doc")
        os.system("doxygen Doxyfile")      
        command=f"""rsync -avzP -e 'ssh -l {self.user} -p {self.port} ' html/ {self.server}:{self.directory} --delete-after"""
        print(command)
        os.system(command)
        os.chdir("..")
  
## Class to define uninstall command
class Uninstall(Command):
    description = "Uninstall installed files with install"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if platform.system()=="Linux":
            os.system("rm -Rf {}/moneymoney_pl*".format(site.getsitepackages()[0]))
            os.system("rm /usr/bin/moneymoney_pl*")
        else:
            os.system("pip uninstall moneymoney_pl")

########################################################################

## Version of moneymoney_pl captured from commons to avoid problems with package dependencies
__version__= None
with open('moneymoney_pl/__init__.py', encoding='utf-8') as f:
    for line in f.readlines():
        if line.find("__version__ =")!=-1:
            __version__=line.split("'")[1]


setup(name='moneymoney_pl',
     version=__version__,
     description='Python module to read and write LibreOffice and MS Office files using uno API',
     long_description='Project web page is in https://github.com/turulomio/moneymoney_pl',
     long_description_content_type='text/markdown',
     classifiers=['Development Status :: 4 - Beta',
                  'Intended Audience :: Developers',
                  'Topic :: Software Development :: Build Tools',
                  'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                  'Programming Language :: Python :: 3',
                 ], 
     keywords='office generator uno pyuno libreoffice',
     url='https://github.com/turulomio/moneymoney_pl',
     author='Turulomio',
     author_email='turulomio@yahoo.es',
     license='GPL-3',
     packages=['moneymoney_pl'],
     install_requires=[],
     cmdclass={'doxygen': Doxygen,
               'uninstall':Uninstall, 
               'translate': Translate,
               'documentation': Documentation,
               'procedure': Procedure,
               'reusing': Reusing,
              },
     zip_safe=False,
     test_suite = 'moneymoney_pl.tests',
     include_package_data=True
)
