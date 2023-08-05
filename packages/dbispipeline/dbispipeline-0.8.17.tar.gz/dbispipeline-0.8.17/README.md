# DBIS Pipeline
This pipline can be used to run analyses in a structured way, and stores
configurations and results in a database.

## Usage

the user writes a minimal plan file which contains only the following
information:
 * "how do I get the data?", by providing a dataloader
 * "what to do with the data?", by providing a scikit pipeline
 * "how to process the result?", by providing result handlers.
 * "where to additionally store results?" by providing storage handlers.


Please have a look at the examples for more information.

### CLI
We provide a `dbispipeline-link` tool that can be used to link datasets to
the data directory. This ensures that datasets are linked in a consistent way
even on different machines. The general process is as follows:
 1. Either in the `dbispipeline.ini` or as an argument in the cli call, one can
 define where in general datasets are stored on the local machine. For example,
 many datasets are available on `/storage/nas3/datasets/text`. In this case,
 this would be the value in the configuration:

     ```
    #dbispipeline.ini:
    [project]
    dataset_dir = /storage/nas3/datasets
    ```
 2. In a file `data/links.yaml`, one can define specific datasets that are used
 by the software. Thereby, the first path segment will be cut off (not sure why).
 For example, the following yaml file:

    ```yaml
    ---
    datasets:
      - music/acousticbrainz
      - music/billboard
      - music/millionsongdataset
    ```
    would assume that a physical directory exists at
    `/storage/nas3/datasets/music/billboard` and after calling the script
    `dbispipeline-link` without parameters using the above configuration, the
    following symlinks will be created:
    ```
    data/acousticbrainz -> /storage/nas3/datasets/music/acousticbrainz
    data/billboard -> /storage/nas3/datasets/music/billboard
    data/millionsongdataset -> /storage/nas3/datasets/music/millionsongdataset
    ```

    The value of `dataset_dir` from the config can be overwritten in the cli
    script by using the `-p` option.


## Requirements

* python >= 3.6
* a PostgreSQL database
* an email server if you want to use notification emails


## Installation

1. Install dbispipeline in your python. We recommend using pipenv to keep your
   dependencies clean: `pipenv install dbispipeline`
   This call will install a virtual environment as well as all dependencies.
2. Write your plan(s). See the example plan files for guidance.
3. call `pipenv run dp <yourplanfile.py>`

Enjoy!


## Configuration
The framework look in multiple directories for its configuration files.
* `/usr/local/etc/dbispipeline.ini` used for system wide default.
* `$HOME/.config/dbispipeline.ini` used for user specific configurations.
* `./dbispipeline.ini` for project specific configurations.

And example configuration file looks like this:
```ini
[database]

# url to your postgres database
host = your.personal.database

# your database user name
user = user

# port of your postgres database, default = 5432
# port = 5432

# password of your database user
password = <secure-password>

# database to use
database = pipelineresults

# table to be used
result_table = my_super_awesome_results

[project]
# this will be stored in the database
name = dbispipeline-test

# this is used to store backups of the execution
# it is possible to override this by setting the DBISPIPELINE_BACKUP_DIR
# environment variable
# the default is the temp dir of the os if this option is not set.
backup_dir = tmp

# this is used to linke the used datasets spcified in data/links.yaml
# it is possible to override this by setting the DBISPIPELINE_DATASET_DIR
# environment variable
dataset_dir = /storage/nas/datasets

[mail]
# email address to use as sender
sender = botname@yourserver.com

# recipient. This should probably be set on a home-directory-basis.
recipient = you@yourserver.com

# smtp server address to use
smtp_server = smtp.yourserver.com

# use smtp authentication, default = no
# authenticate = no

# username for smtp authentication, required if authenticate = yes
# username = foo

# password for smtp authentication, required if authenticate = yes
# password = bar

# port to use for smtp server connection, default = 465
# port = 465
```
