#!/bin/sh
rm -f dist/spotdesirability*; python -m build; python -m pip install dist/spotdesirability*.tar.gz
python -m mkdocs build
