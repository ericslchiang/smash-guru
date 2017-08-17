# Installation
Install `virtualenv` and other libraries:
```
$ ./install.sh
```

# Setup
Setup isolated python environment:
```
$ virtualenv venv
$ source venv/bin/activate
```

If you have not installed pytest yet:
```
$ pip install pytest
```

We're using `pysmash` to get tournament brackets:
```
$ pip install pysmash
```



# Teardown
Teardown python environment:
```
$ deactivate
```
