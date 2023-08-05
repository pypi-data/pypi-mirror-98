macropragma - apply macros/substitutions/modifications on top of your source code
--
# Introduction
The intention is to easily modify/add/remove macros within source files. Typical usage is during installation procesess in order to modify involved source files.

# Usage
* Create "my.yaml" file.
* Add it to the prebuild, build or installation task.
# Examples
## Execution
```
python3 -m macropragma -h
# Typical usage:
python3 -m macropragma -c <CONFIG_YAML=my.yaml> -d <PROJECT_ROOT>
```
## <CONFIG_YAML=my.yaml>
```
# One full entry
db/evr-mtca-300u.db: #file to process
    greps: #grep for the lines under concern
        - "$(SYS)"
        - "$(D)"
    subs: #substitute the elements
        "{$(D)}": "$(D)"
        "{$(D)": "$(D)"
        "$(D)-": "$(D)"
        "}": "-"
        ":": ""
        "$(SYS)$(D)": "$(P)$(R=)$(S=:)"
    output: #store the processed file into
        "db/evr-mtca-300u-univ.db"
```
