#!/bin/bash
set -evx

mkdir ~/.moondexcore

# safety check
if [ ! -f ~/.moondexcore/.moondex.conf ]; then
  cp share/moondex.conf.example ~/.moondexcore/moondex.conf
fi
