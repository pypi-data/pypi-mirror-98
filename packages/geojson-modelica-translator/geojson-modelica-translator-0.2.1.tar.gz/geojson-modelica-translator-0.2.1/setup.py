# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geojson_modelica_translator',
 'geojson_modelica_translator.geojson',
 'geojson_modelica_translator.model_connectors',
 'geojson_modelica_translator.model_connectors.couplings',
 'geojson_modelica_translator.model_connectors.districts',
 'geojson_modelica_translator.model_connectors.energy_transfer_systems',
 'geojson_modelica_translator.model_connectors.load_connectors',
 'geojson_modelica_translator.model_connectors.networks',
 'geojson_modelica_translator.model_connectors.plants',
 'geojson_modelica_translator.modelica',
 'geojson_modelica_translator.modelica.lib',
 'geojson_modelica_translator.modelica.lib.runner',
 'geojson_modelica_translator.system_parameters',
 'management']

package_data = \
{'': ['*'],
 'geojson_modelica_translator.geojson': ['data/schemas/*'],
 'geojson_modelica_translator.model_connectors.couplings': ['templates/CoolingIndirect_Network2Pipe/*',
                                                            'templates/CoolingIndirect_NetworkChilledWaterStub/*',
                                                            'templates/HeatingIndirect_Network2Pipe/*',
                                                            'templates/HeatingIndirect_NetworkHeatedWaterStub/*',
                                                            'templates/Network2Pipe_CoolingPlant/*',
                                                            'templates/Network2Pipe_HeatingPlant/*',
                                                            'templates/Spawn_EtsColdWaterStub/*',
                                                            'templates/Spawn_EtsHotWaterStub/*',
                                                            'templates/Teaser_EtsColdWaterStub/*',
                                                            'templates/Teaser_EtsHotWaterStub/*',
                                                            'templates/TimeSeriesMFT_CoolingIndirect/*',
                                                            'templates/TimeSeriesMFT_HeatingIndirect/*',
                                                            'templates/TimeSeries_CoolingIndirect/*',
                                                            'templates/TimeSeries_EtsColdWaterStub/*',
                                                            'templates/TimeSeries_EtsHotWaterStub/*',
                                                            'templates/TimeSeries_HeatingIndirect/*'],
 'geojson_modelica_translator.model_connectors.districts': ['templates/*'],
 'geojson_modelica_translator.model_connectors.energy_transfer_systems': ['templates/*'],
 'geojson_modelica_translator.model_connectors.load_connectors': ['templates/*'],
 'geojson_modelica_translator.model_connectors.networks': ['templates/*'],
 'geojson_modelica_translator.model_connectors.plants': ['templates/*'],
 'geojson_modelica_translator.modelica': ['model_connectors/templates/*',
                                          'templates/*']}

install_requires = \
['BuildingsPy==2.1.0',
 'click==7.1.2',
 'geojson==2.5.0',
 'jsonpath-ng==1.5.2',
 'jsonschema==3.2.0',
 'modelica-builder==0.1.1',
 'requests==2.25.1',
 'teaser==0.7.5']

entry_points = \
{'console_scripts': ['format_modelica_files = '
                     'management.format_modelica_files:fmt_modelica_files',
                     'uo_des = management.uo_des:cli',
                     'update_licenses = '
                     'management.update_licenses:update_licenses',
                     'update_schemas = '
                     'management.update_schemas:update_schemas']}

setup_kwargs = {
    'name': 'geojson-modelica-translator',
    'version': '0.2.1',
    'description': 'Package for converting GeoJSON to Modelica models for Urban Scale Analyses.',
    'long_description': 'GeoJSON Modelica Translator (GMT)\n---------------------------------\n\n.. image:: https://github.com/urbanopt/geojson-modelica-translator/actions/workflows/ci.yml/badge.svg?branch=develop\n    :target: https://github.com/urbanopt/geojson-modelica-translator/actions/workflows/ci.yml\n\n.. image:: https://coveralls.io/repos/github/urbanopt/geojson-modelica-translator/badge.svg?branch=develop\n    :target: https://coveralls.io/github/urbanopt/geojson-modelica-translator?branch=develop\n\n.. image:: https://badge.fury.io/py/GeoJSON-Modelica-Translator.svg\n    :target: https://pypi.org/project/GeoJSON-Modelica-Translator/\n\nDescription\n-----------\n\nThe GeoJSON Modelica Translator (GMT) is a one-way trip from GeoJSON in combination with a well-defined instance of the system parameters schema to a Modelica package with multiple buildings loads, energy transfer stations, distribution networks, and central plants. The project will eventually allow multiple paths to build up different district heating and cooling system topologies; however, the initial implementation is limited to 1GDH and 4GDHC.\n\nThe project is motivated by the need to easily evaluate district energy systems. The goal is to eventually cover the various generations of heating and cooling systems as shown in the figure below. The need to move towards 5GDHC systems results in higher efficiencies and greater access to additional waste-heat sources.\n\n.. image:: https://raw.githubusercontent.com/urbanopt/geojson-modelica-translator/develop/docs/images/des-generations.png\n\nGetting Started\n---------------\n\nThe GeoJSON Modelica Translator is in alpha-phase development and the functionality is limited. Currently, the proposed approach for getting started is outlined in this readme. You need Python 3, pip 3, and Poetry to install/build the packages. Note that the best approach is to use Docker to run the Modelica models as this approach does not require Python 2.\n\n* Clone this repo into a working directory\n* (optional/as-needed) Add Python 3 to the environment variables\n* Install Poetry (:code:`pip install poetry`). More information on Poetry can be found `here <https://python-poetry.org/docs/>`_.\n* Install `Docker <https://docs.docker.com/get-docker/>`_ for your platform\n* Configure Docker on your local desktop to have at least 4 GB Ram and 2 cores. This is configured under the Docker Preferences.\n* Install the Modelica Buildings Library from GitHub\n    * Clone https://github.com/lbl-srg/modelica-buildings/ into a working directory outside of the GMT directory\n    * Change to the directory inside the modelica-buildings repo you just checked out. (:code:`cd modelica-buildings`)\n    * Install git-lfs\n        * Mac: :code:`brew install git-lfs; git lfs install`\n        * Ubuntu: :code:`sudo apt install git-lfs; git lfs install`\n    * Pull the correct staging branch for this project with: :code:`git checkout issue2204_gmt_mbl`\n    * Add the Modelica Buildings Library path to your MODELICAPATH environment variable (e.g., export MODELICAPATH=${MODELICAPATH}:$HOME/path/to/modelica-buildings).\n* Return to the GMT root directory and run :code:`poetry install`\n* Test if everything is installed correctly by running :code:`poetry run tox`\n    * This should run all unit tests, pre-commit, and build the docs.\n\nThe tests should all pass assuming the libraries are installed correctly on your computer. Also, there will be a set of Modelica models that are created and persisted into the :code:`tests/output` folder and the :code:`tests/model_connectors/output` folder. These files can be inspected in your favorite Modelica editor.\n\nDevelopers\n**********\n\nThis project used `pre-commit <https://pre-commit.com/>`_ to ensure code consistency. To enable pre-commit, run the following from the command line.\n\n.. code-block:: bash\n\n    pip install pre-commit\n    pre-commit install\n\nTo run pre-commit against the files without calling git commit, then run the following. This is useful when cleaning up the repo before committing.\n\n.. code-block:: bash\n\n    pre-commit run --all-files\n\nGeoJSON\n+++++++\n\nThis module manages the connection to the GeoJSON file including any calculations that are needed. Calculations can include distance calculations, number of buildings, number of connections, etc.\n\nThe GeoJSON model should include checks for ensuring the accuracy of the area calculations, non-overlapping building areas and coordinates, and various others.\n\nLoad Model Connectors\n+++++++++++++++++++++\n\nThe Model Connectors are libraries that are used to connect between the data that exist in the GeoJSON with a model-based engine for calculating loads (and potentially energy consumption). Examples includes, TEASER, Data-Driven Model (DDM), CSV, Spawn, etc.\n\n\nSimulation Mapper Class / Translator\n++++++++++++++++++++++++++++++++++++\n\nThe Simulation Mapper Class can operate at mulitple levels:\n\n1. The GeoJSON level -- input: geojson, output: geojson+\n2. The Load Model Connection -- input: geojson+, output: multiple files related to building load models (spawn, rom, csv)\n3. The Translation to Modelica -- input: custom format, output: .mo (example inputs: geojson+, system design parameters). The translators are implicit to the load model connectors as each load model requires different paramters to calculate the loads.\n\nIn some cases, the Level 3 case (translation to Modelica) is a blackbox method (e.g. TEASER) which prevents a simulation mapper class from existing at that level.\n\nRunning Simulations\n-------------------\n\nThe GeoJSON to Modelica Translator contains a :code:`ModelicaRunner.run_in_docker(...)` method. It is recommended\nto use this method in a python script if needed as it will copy the required files into the correct location. If\ndesired, a user can run the simulations manually using JModelica (via Docker). Follow the step below to configure\nthe runner to work locally.\n\n* Make sure jm_ipython.sh is in your local path.\n* After running the :code:`py.test`, go into the :code:`geojson_modelica_translator/modelica/lib/runner/` directory.\n* Copy :code:`jmodelica.py` to the :code:`tests/model_connectors/output` directory.\n* From the :code:`tests/model_connectors/output` directory, run examples using either of the the following:\n    * :code:`jm_ipython.sh jmodelica.py spawn_single.Loads.B5a6b99ec37f4de7f94020090.coupling`\n    * :code:`jm_ipython.sh jmodelica.py spawn_single/Loads/B5a6b99ec37f4de7f94020090/coupling.mo`\n    * The warnings from the simulations can be ignored. A successful simulation will return Final Run Statistics.\n* Install matplotlib package. :code:`pip install matplotlib`\n* Visualize the results by inspecting the resulting mat file using BuildingsPy. Run this from the root directory of the GMT.\n\n    .. code-block:: python\n\n        %matplotlib inline\n        import os\n        import matplotlib.pyplot as plt\n\n        from buildingspy.io.outputfile import Reader\n\n        mat = Reader(os.path.join(\n            "tests", "model_connectors", "output", "spawn_single_Loads_B5a6b99ec37f4de7f94020090_coupling_result.mat"),\n            "dymola"\n        )\n        # List off all the variables\n        for var in mat.varNames():\n            print(var)\n\n        (time1, zn_1_temp) = mat.values("bui.znPerimeter_ZN_3.TAir")\n        (_time1, zn_4_temp) = mat.values("bui.znPerimeter_ZN_4.TAir")\n        plt.style.use(\'seaborn-whitegrid\')\n\n        fig = plt.figure(figsize=(16, 8))\n        ax = fig.add_subplot(211)\n        ax.plot(time1 / 3600, zn_1_temp - 273.15, \'r\', label=\'$T_1$\')\n        ax.plot(time1 / 3600, zn_4_temp - 273.15, \'b\', label=\'$T_4$\')\n        ax.set_xlabel(\'time [h]\')\n        ax.set_ylabel(r\'temperature [$^\\circ$C]\')\n        # Simulation is only for 168 hours?\n        ax.set_xlim([0, 168])\n        ax.legend()\n        ax.grid(True)\n        fig.savefig(\'indoor_temp_example.png\')\n\nManaged Tasks\n-------------\n\nUpdating Schemas\n****************\n\nThere is managed task to automatically pull updated GeoJSON schemas from the :code:`urbanopt-geojson-gem` GitHub project. A developer can run this command by calling\n\n.. code-block:: bash\n\n    poetry run update_schemas\n\nThe developer should run the test suite after updating the schemas to ensure that nothing appears to have broken. Note that the tests do not cover all of the properties and should not be used as proof that everything works with the updated schemas.\n\n\nUpdating Licenses\n*****************\n\nTo apply the copyright/license to all the files, run the following managed task\n\n.. code-block:: bash\n\n    poetry run update_licenses\n\n\nTemplating Diagram\n------------------\n.. image:: https://raw.githubusercontent.com/urbanopt/geojson-modelica-translator/develop/docs/images/des-connections.png\n\nRelease Instructions\n--------------------\n\n* Bump version to <NEW_VERSION> in setup.py (use semantic versioning as much as possible).\n* Run `autopep8` to nicely format the code (or run `pre-commit --all-files`).\n* Create a PR against develop into main.\n* After main branch passes, then merge and checkout the main branch. Build the distribution using the following code:\n\n.. code-block:: bash\n\n    # Remove old dist packages\n    rm -rf dist/*\n    poetry build\n\n* Run `git tag <NEW_VERSION>`. (Note that `python setup.py --version` pulls from the latest tag.)\n* Verify that the files in the dist/* folder have the correct version (no dirty, no sha)\n* Run the following to release\n\n.. code-block:: bash\n\n    poetry publish\n\n* Build and release the documentation\n\n.. code-block:: bash\n\n    # Build and verify with the following\n    cd docs\n    poetry run make html\n    cd ..\n\n    # release using\n    ./docs/publish_docs.sh\n\n* Push the tag to GitHub after everything is published to PyPi, then go to GitHub and add in the CHANGELOG.rst notes into the tagged release and officially release.\n\n.. code-block:: bash\n\n    git push origin <NEW_VERSION>\n',
    'author': 'URBANopt DES Team',
    'author_email': 'nicholas.long@nrel.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://docs.urbanopt.net',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
