# HackEDU Command Line Interface

The HackEDU command-line interface is a wrapper for the HackEDU Public API.

Documentation for the HackEDU API can be found at
[https://developers.hackedu.com](developers.hackedu.com)

## Installing

You can install the latest version of `hackedu-cli` with `pip`:

    pip install hackedu-cli

Or you can build from source by cloning this repository and running setup:

    git clone https://github.com/hack-edu/hackedu-cli
    python setup.py develop


You will now have access to the hackedu command in your terminal.

## Commands

### View the available options

    hackedu --help

### Create your `.hackedu` config file

    hackedu config

You can either define options inside of your `.hackedu` config file, or pass
them in via the command line. If you store your config file anywhere other than
the default location (~/.hackedu), then you'll need to use the --config command
line option.

    hackedu [OPTIONS] COMMAND --config=/path/to/config/.hackedu

You can also define a profile within your config file. For example, a SonarQube
specific profile.

    [default]
    api_key=API_KEY
    hackedu_url=https://api.hackedu.com

    [sonarqube_1]
    source=SOURCE_UUID
    username=USERNAME
    password=PASSWORD
    app=SONARQUBE_APP_NAME

    [sonarqube_2]
    source=SOURCE_UUID
    username=USERNAME
    password=PASSWORD
    app=SONARQUBE_APP_NAME

### Create an Issue Source

    hackedu issue-source create --title=[TITLE] --type=[TYPE]

## List all Issue Sources

    hackedu issue-source ls

### Sync Issues for an Issue Source

    hackedu issues sync sonarqube --username=[USERNAME] --password=[PASSWORD] --url=[URL] --branch=[BRANCH] --app=[APP] --source=[ISSUE_SOURCE_UUID]

### List Issues for an Issue Source

    hackedu issues ls --source=[ISSUE_SOURCE_UUID]

### See the version

    hackedu --version
