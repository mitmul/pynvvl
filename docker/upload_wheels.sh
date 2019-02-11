#!/bin/bash

twine upload --repository pypi dist/cuda-8.0/*.whl
twine upload --repository pypi dist/cuda-9.0/*.whl
twine upload --repository pypi dist/cuda-9.1/*.whl
twine upload --repository pypi dist/cuda-10.0/*.whl
