# End to end tests

The goal here is to test the actual tool running the commands the user would run. Example:

```bash
vaultscan version
```

So, before run it on the pipeline we need to install the package using pip, so you can run it using the real command.

## Libraries
We are using the ```subprocess``` library here, but you can also look at pip install ```pytest-console-scripts```.