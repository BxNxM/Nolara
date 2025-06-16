#!/bin/bash

echo -e "Cleaning build artifacts..."
rm -rf build/ dist/ *.egg-info

echo -e "Building package..."
python3 -m build || exit 1

echo -e "List packages..."
ls -l dist

echo -e "Reinstalling package..."
pip3 install --force-reinstall --no-cache-dir --break-system-packages dist/*.whl

echo -e "New command:\n\tnolara\nDone. Test by running:"
nolara
# python -m nolara.main


