# COVID Cloud CLI

## Getting Started
DISCLAIMER: This repo is a work in progress. Anything in 'Getting Started' may be prone to bugs.

This project is written in Python and uses the [Click](https://click.palletsprojects.com/en/7.x/). The documentation is really nice so make sure to have a look if you're running into any problems developing.

1. Run `pip3 install -r requirements.txt` to download all the dependencies 

Sample commands to run to test:
```
python3 covid-cloud.py --help

python3 covid-cloud.py search tables list

python3 covid-cloud.py search tables get coronavirus_public.covid19_italy.data_by_province
```

## How to package the project into a single file executable

This project uses [PyInstaller](https://www.pyinstaller.org/) to create a single binary file that packages everything together so that the user will be able to run the CLI without worrying about any dependencies or whether they even have Python installed. 

However, the Mac variant of the executable created by PyInstaller has a bit of a lengthy start up time, so we've resorted to using PyInstaller's `--onedir` flag which creates a directory with all the dependencies rather than a single file. From the user's perspective, however, it'll still appear to be a single file executable as the Mac variant will be bundled up with a `covid-cloud` shell script which serves as the executable that the user runs. See [here](#for-mac)
 
#### To package on Mac, run:

`pyinstaller --onedir covid-cloud.py --hidden-import cmath`

A `covid-cloud` directory should be created in the ./dist directory. Then you can run the same commands above without `python3` or `.py` in the file name

Sample commands to run to test:

```
./dist/covid-cloud/covid-cloud --help

./dist/covid-cloud/covid-cloud search tables list

./dist/covid-cloud/covid-cloud search tables get coronavirus_public.covid19_italy.data_by_province
```

#### To package on Linux/Windows, run:
 
To package with PyInstaller, run: 

`pyinstaller --onefile covid-cloud.py --hidden-import cmath`

A `covid-cloud` file should be created in the ./dist directory. Then you can run the same commands above without `python3` or `.py` in the file name

Sample commands to run to test:

```
covid-cloud --help

covid-cloud search tables list

covid-cloud search tables get coronavirus_public.covid19_italy.data_by_province
```

#### IMPORTANT NOTE
The executable that is created will be based off of your local OS. If you wish to create an executable that is not your current OS, there are a few ways we go about this.
 
Currently, we use [docker-pyinstaller](https://github.com/cdrx/docker-pyinstaller) to create executables for <u>Windows</u>. To create an executable for Windows, simply run the following in the root directory of this project:

1. Run `pyinstaller --onefile covid-cloud.py --hidden-import cmath` once to generate a `.spec` file in this project (the tool requires the `.spec` file and `requirements.txt` in the root folder)
2. For a Windows executable, run: `docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows`
3. Your executable will be created in the ./dist directory

As for <u>Linux</u>, we have discovered that the above library produces a buggy executable. If you want to produce an executable for Linux, it is better to have someone with a Linux machine to run the packaging commands above to create the executable for you.
    
The same process for <u>Mac</u> will be required if you are working on a non-Mac machine but wish to produce a Mac executable.


## How we distribute the CLI

Currently, we use this repo's 'Releases' page to host our executables: https://github.com/DNAstack/public-covid-cloud-cli/releases

To create the end product CLI executables/zips that you see on the page, do the following:

#### For Linux/Windows
Simply create the single-file executable with the instructions above and drag-and-drop them on the 'Releases' page. Make sure that they are named `covid-cloud-linux` for Linux or `covid-cloud-windows.exe` for Windows

#### For Mac
1. Bundle up the project using the above instructions (**make sure you're using the `--onedir` flag**)
2. Rename the outputted folder as `cli`
3. Copy the shell script (in `resources/covid-cloud`) into the same directory where your `cli` folder is. Then zip them up as one file named `covid-cloud-mac.zip`
4. Drag-and-drop the zip onto the 'Releases' page

## Using the CLI as a Python library
The CLI can also be imported as a Python library. It is hosted on PyPi here: https://pypi.org/project/covid-cloud/

You can simply install it as a dependency with `pip3 install covid_cloud` or through other traditional `pip` ways (e.g. `requirements.txt`)

#### Usage

To use the `covid_cloud` library in Jupyter Notebooks and other Python code, simply import the COVIDCloud object

`from covid_cloud import COVIDCloud`

#### Example

```python
from covid_cloud import COVIDCloud

covid_client = COVIDCloud(search_url='[SEARCH_URL]',drs_url='[DRS_URL]')

# login to Wallet
covid_client.login(personal_access_token='[PAT]',email='[EMAIL]')

# get tables 
tables = covid_client.list_tables()

# get table schema
schema = covid_client.get_table('[TABLE_NAME]')

# query
results = covid_client.query('SELECT * FROM ...')

# load a drs resource into a DataFrame
drs_df = covid_client.load(['[DRS_URL]'])

# download a DRS resource into a file
covid_client.download(['[DRS_URL]'])
```

#### Uploading the project to PyPi
You can find a guide on how to upload projects to PyPi [here](https://packaging.python.org/tutorials/packaging-projects/), but here's a quick TL;DR guide. The project already contains the necessary metadata files, so you just need to run these commands:
1. Run these commands to install necessary dependencies for upload 

    `python3 -m pip install --upgrade build`

    `python3 -m pip install --user --upgrade twine`
    
1. This project is hosted on the `derekdna` PyPi account. Ask Derek for an API token to be able to upload.

1. At the root directory of the project, run `python3 -m build`

1. Still at the root directory, run `twine upload dist/*` . You'll be prompted for credentials from step 2.

1. Done! Give PyPi a minute to index, but afterwards you can install the package by simply running:

    `pip3 install covid-cloud`
    
    or if you want to specify a version:
    
    `pip3 install covid-cloud==<VERSION NUMBER>`

## How to use
### Search the API
```
covid-cloud search query [QUERY] #run an SQL query
```

### Get a list of tables
```
covid-cloud search tables list 
```

## Get info a specific table
```
covid-cloud search tables get [TABLE_ID]
```

### Downloading DRS files
```
covid-cloud files download [URL] [--input/-i INPUT_FILE] [--output/-o OUTPUT_DIRECTORY]
```
