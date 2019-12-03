#!/bin/bash

if [ -d bin ]; then
    git submodule update --init --recursive -- bin
    cd bin
    git fetch --all --recurse-submodules
    git checkout origin/dev --detach
    cd ..
fi
