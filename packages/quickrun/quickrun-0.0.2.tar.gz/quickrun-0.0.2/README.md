# quickrun

quickrun is a module designed to make it easy to run commands and gather info from multiple servers.  

## Dependencies
- python3.8
- jq
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

# Define instance
qr = quickrun.QuickRun()

# Configure
qr.servers = [ quickrun.Server(ip="my-ip-address", name="my-web-server", user="username") ]
qr.commands = [ quickrun.Command(name="Disk usage", cmd="df -h") ]
qr.formatter = quickrun.formatters.table

# Call
qr.main()
qr.display()
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


##### aws_cli
There is also a helpful `quickrun.aws_cli.find_instances()` function that takes a string and region and returns all instances with the `name` tag containing that string.  

---

## Hooks

TODO
