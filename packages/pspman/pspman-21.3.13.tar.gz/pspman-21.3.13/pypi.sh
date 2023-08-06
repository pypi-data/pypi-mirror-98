#!/bin/sh

# start from scratch
rm -rf build dist

# build
python3 -m build

# upload
twine upload \
  --skip-existing \
  --sign \
  --sign-with gpg2 \
  --identity pradyparanjpe@rediffmail.com \
  --username pradyparanjpe \
  --password "$(pass show pypi.org/pradyparanjpe)" \
  "./dist/*"
