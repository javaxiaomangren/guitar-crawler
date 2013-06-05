#!/usr/bin/env python
import sys
from subprocess import call
for l in sys.stdin:
    l = l[:-1]
    print './youtube-dl --proxy 127.0.0.1:8087 ' + 'https://www.youtube.com/watch?{0}&list=PL782D0D8FA14D3055 > log/{1} 2>&1  &'.format(l, l)
