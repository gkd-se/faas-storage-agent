How to use our template to build openFaas funcitons?
You can read this [doc](https://github.com/openfaas/faas-cli/blob/master/guide/TEMPLATE.md).
And you can do as tests : tests/integration_tests/wheel
```shell
# In the root path of this project
cp -r template  tests/integration_tests/wheel/
faas-cli build -f tests/integration_tests/wheel/wheel.yml
```