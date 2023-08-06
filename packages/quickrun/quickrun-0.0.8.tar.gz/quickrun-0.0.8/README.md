# quickrun

quickrun is a module designed to make it easy to run commands and gather info from multiple servers.  

## Dependencies
- python3.8
- aws cli (v1)

---

## Getting started

#### Setup
Install:  
```
pip3 install quickrun
```

Use:  
```python
import quickrun
from quickrun.cli.aws import find_instances

# Define instance
qr = quickrun.QuickRun()

# Configure

qr.servers = [ quickrun.Server(host="my-ip-address-or-hostname", name="my-web-server", user="username") ]
# or from aws cli
qr.servers = quickrun.Servers.from_list(find_instances({ 'tag:environment': 'production', 'tag:name': '*web*' }, region='eu-west-1'))

qr.commands = [ quickrun.Command(name="Get openssl version", cmd="openssl version") ]
qr.formatter = quickrun.formatters.table

# Call
qr.main()
qr.display()
```

This will display something like:
```
                                            Results
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ server             ┃ host        ┃ command         ┃ output                     ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ my-instance-name-1 │ 192.168.0.1 │ openssl version │ OpenSSL 1.1.1  11 Sep 2018 │
│ my-instance-name-2 │ 192.168.0.1 │ openssl version │ OpenSSL 1.1.1  11 Sep 2018 │
│ my-instance-name-3 │ 192.168.0.1 │ openssl version │ OpenSSL 1.1.1  11 Sep 2018 │
│ my-instance-name-4 │ 192.168.0.1 │ openssl version │ OpenSSL 1.1.1  11 Sep 2018 │
└────────────────────┴─────────────┴─────────────────┴────────────────────────────┘
```

#### Making a script

##### Option 1: Basic script using some of the functions
You can just write a normal python script and use some of the functions from this module.  
See `examples/healthcheck.py` as an example.  

##### Option 2: Calling out to QuickRun
There is also the base `QuickRun` class which can be configured and called.  
See `examples/openssl-version.py` and `examples/list-logs.py` as examples.  

##### Option 3: Extending QuickRun
You could also create your own class extending from `QuickRun`.  
This is handy since you can override the [hook methods](#Hooks).  
See `examples/get-memory-settings.py` as an example.  

---

## Helpers

There are a few core helpers built in to quickrun.    

##### Formatters
There are a few formatters defined in `quickrun.formatters`
-	`default`: Just prints out the python object
- `none`: Does nothing
- `fake_shell`: Formats the run as if it was ran directly
- `table`: Outputs the run as a table


##### cli.aws
There is also a helpful `quickrun.cli.aws.find_instances()` function that takes a dict of filters and returns matching instances.  

Example:
```python
find_instances({ 'tag:name': 'web', 'tag:environment': 'prod' }, region='eu-west-1')
```

##### cli.helpers
There is a collection of misc CLI helpers in `quickrun.cli.helpers`.  
Currently there is only `challenge(expect: str) -> bool` which prompts the user to re-enter a value.  

---

## Hooks

TODO
