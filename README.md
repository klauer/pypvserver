## pypvserver
Python EPICS PV Server, based on pcaspy

### Requires
* pcaspy >= 0.6.0

### Example

```bash
$ ipython
```
```python
In [1]: from pypvserver import (PypvServer, PyPV)
In [2]: server = PypvServer(prefix='PREFIX:')
In [3]: pv = PyPV('pv1', 123.0, server=server)
In [4]: pv
Out[5]: PyPV('pv1', value=123.0, alarm=0, severity=0)

# Tweak its value a bit...
In [6]: pv.put(1)
In [7]: pv.put(2)
In [8]: pv.put(3)
```

Here's what happens from the EPICS client (`camonitor`):
```sh
$ camonitor PREFIX:pv1
PREFIX:pv1                     2016-01-25 13:48:51.112522 123
PREFIX:pv1                     2016-01-25 13:49:12.286193 1
PREFIX:pv1                     2016-01-25 13:49:13.714229 2
PREFIX:pv1                     2016-01-25 13:49:14.761100 3

$ cainfo PREFIX:pv1
PREFIX:pv1
    State:            connected
    Host:             localhost:56144
    Access:           read, write
    Native data type: DBF_DOUBLE
    Request type:     DBR_DOUBLE
    Element count:    1
```
