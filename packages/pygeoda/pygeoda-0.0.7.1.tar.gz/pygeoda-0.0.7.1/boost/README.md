# pygeoda_boost
 boost static library for pygeoda

version: 1.67.0


## OSX

'''
./bootstrap.sh
./b2 --with-thread --with-date_time --with-chrono --with-system cxxflags=-fvisibility=hidden link=static threading=multi stage
'''

## ubuntu

'''
./bootstrap.sh
./b2 --with-thread --with-date_time --with-chrono --with-system cxxflags=-fPIC cflags=-fPIC link=static threading=multi stage
'''

## windows

https://boost.teeks99.com/bin/1.69.0/

Visual C++

CPython

msvc=14.X (14.1 visual studio 2017)

3.5, 3.6, 3.7, 3.8

msvc=10.0

3.3, 3.4

msvc=9.0

2.6, 2.7, 3.0, 3.1, 3.2

