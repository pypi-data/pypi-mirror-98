# quickrun

quickrun is a module designed to make it easy to run commands and gather info from multiple servers.  

## Dependencies
- python3.8
- jq
- aws cli (v1)

---

## Getting started

#### Setup
```
$ git clone ...
$ cd quickrun
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

#### Defining new scripts

All scripts live in the `run/` directory.  
There are a few ways to use this module.  

##### Option 1: Basic script using some of the functions
You can just write a normal python script and use some of the functions from this module.  
See `run/tomcat-cycle.py` as an example.  

##### Option 2: Calling out to QuickRun
There is also the base `QuickRun` class which can be configured and called.  
See `run/openssl-version.py` and `run/list-logs.py` as examples.  

##### Option 3: Extending QuickRun
You could also create your own class extending from `QuickRun`.  
This is handy since you can override the [hook methods](#Hooks).  
See `run/get-memory-settings.py` as an example.  

---

## Helpers

There are a few core helpers built in to quickrun.    

##### Formatters
There are a few formatters defined in `quickrun/lib/formatters.py`
-	`default`: Just prints out the python object
- `none`: Does nothing
- `fake_shell`: Formats the run as if it was ran directly
- `table`: Outputs the run as a table


##### aws_cli
In `quickrun/lib/aws_cli.py` there is also a helpful `find_instances()` function that takes a string and region and returns all instances with the `name` tag containing that string.  

---

## Hooks

TODO
