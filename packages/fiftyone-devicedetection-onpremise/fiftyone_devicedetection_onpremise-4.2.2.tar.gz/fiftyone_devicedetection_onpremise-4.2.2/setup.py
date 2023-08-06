#!/usr/bin/env python

# See https://docs.python.org/3/distutils/setupscript.html
# Distutils is used to orchestrate building and installation of the SWIG 
# generated Device Detection wrapper. 
# See http://www.swig.org/Doc4.0/Python.html#Python_nn6
# 
# SWIG generated files will need be built manually by a developer to control
# file version. Even though swig is support by distutils but for this reason,
# it won't be used here.
# 
# This setup script overrides the 'get_ext_filename' method in the 'build_ext' 
# distutils command to set the build directory and unify the file extension
# based on the platform currently building the extension.

"""
setup.py file for SWIG
"""
import sys
import platform
from setuptools import setup, Extension
from setuptools.command import develop
from distutils import sysconfig
from Cython.Distutils import build_ext
import os

def get_version():

    version = None
    
    # Try to get the correct version from platform.
    is_64bits = sys.maxsize > 2**32
    if is_64bits:
        if 'Windows' in platform.system():
            version = "win_64_"
        if 'Linux' in platform.system():
            version = "linux_64_"
        if 'Darwin' in platform.system():
            version = "darwin_64_"
    else:
        if 'Windows' in platform.system():
            version = "win_32_"
        if 'Linux' in platform.system():
            version = "linux_32_"
        if 'Darwin' in platform.system():
            # No 32 bit python on Mac
            version = None
            raise Exception("Sorry, No 32 bit Python on Mac")

    python_version = str(sys.version_info[0])
    return version + python_version

class NoSuffixBuilder(build_ext):
    def get_ext_filename(self, ext_name):
        filename = super().get_ext_filename(ext_name)
        suffix = sysconfig.get_config_var('EXT_SUFFIX')
        if suffix is None:
            suffix = sysconfig.get_config_var('SO')

        print("**" + filename + "**\r\n")
        print("**" + suffix + "**\r\n")
        
        # Get the version from the suffix.
        version = get_version()
 
        ext = os.path.splitext(filename)[1]

        if self.inplace:
            return "./" + filename.replace(suffix, "") + ext
        else:
            return filename.replace(suffix, "") + ext

define_macros = []
extra_compile_args = []
extra_link_args = []
# Extra compilation flags for C library
cflags = []

if sys.platform != "win32":
    extra_compile_args.extend([
        '-fPIC',
        '-std=gnu++11',
        '-Wall',
        '-Werror'
    ])
    cflags.extend([
        '-std=gnu11',
        '-Wall',
        '-Werror',
        '-Wno-strict-prototypes',
        '-Wno-unused-variable',
        '-Wno-missing-braces',
        '-Wno-strict-aliasing'
    ])


if sys.platform == "win32":
    extra_compile_args.extend([
        '/D_CRT_SECURE_NO_WARNINGS',
        '/D_UNICODE',
        '/DUNICODE',
        '/W4',
        '/WX',
        '/wd"4127"',
        '/wd"4456"',
        '/wd"4701"',
        '/wd"4703"',
        '/wd"4706"'
    ])
    cflags.extend([
        '/D_CRT_SECURE_NO_WARNINGS',
        '/D_UNICODE',
        '/DUNICODE',
        '/W4',
        '/WX'
    ])
    extra_link_args.extend([
        '/WX'
    ])

if sys.platform == 'darwin':
    extra_compile_args.extend([
        '-DGCC_ENABLE_CPP_EXCEPTIONS=YES',
    ])

DeviceDetectionHashEngineModule = Extension('_DeviceDetectionHashEngineModule',
        sources=[
        # Python Wrapper
        # "fiftyone_devicedetection_onpremise/hash_python.i"
        "fiftyone_devicedetection_onpremise/hash_python_wrap.cxx"
        ],
        define_macros=define_macros,
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
        language='c++',
    )

cpplib = ('cpplib', {
        'sources': [
            # Common C++
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/CollectionConfig.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/ComponentMetaData.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/ConfigBase.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/Date.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/EngineBase.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/EvidenceBase.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/Exceptions.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/MetaData.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/ProfileMetaData.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/PropertyMetaData.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/RequiredPropertiesConfig.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/ResultsBase.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/ValueMetaData.cpp",
            # Device Detection C++
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/ConfigDeviceDetection.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/EngineDeviceDetection.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/EvidenceDeviceDetection.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/ResultsDeviceDetection.cpp",
            # Hash C++
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/hash/ComponentMetaDataBuilderHash.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/hash/ComponentMetaDataCollectionHash.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/hash/ConfigHash.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/hash/EngineHash.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/hash/MetaDataHash.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/hash/ProfileMetaDataBuilderHash.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/hash/ProfileMetaDataCollectionHash.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/hash/PropertyMetaDataBuilderHash.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/hash/PropertyMetaDataCollectionForComponentHash.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/hash/PropertyMetaDataCollectionForPropertyHash.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/hash/PropertyMetaDataCollectionHash.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/hash/ResultsHash.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/hash/ValueMetaDataBuilderHash.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/hash/ValueMetaDataCollectionBaseHash.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/hash/ValueMetaDataCollectionForProfileHash.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/hash/ValueMetaDataCollectionForPropertyHash.cpp",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/hash/ValueMetaDataCollectionHash.cpp",
            ],
        'cflags': extra_compile_args
    })

clib = ('clib', {
        'sources': [
            # Common C
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/cache.c",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/collection.c",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/component.c",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/data.c",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/dataset.c",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/evidence.c",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/exceptionsc.c",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/file.c",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/float.c",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/headers.c",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/ip.c",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/list.c",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/memory.c",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/overrides.c",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/pool.c",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/profile.c",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/properties.c",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/property.c",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/pseudoheader.c",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/resource.c",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/results.c",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/status.c",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/string.c",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/textfile.c",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/threading.c",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/tree.c",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/common-cxx/value.c",
            # Device Detection C
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/dataset-dd.c",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/results-dd.c",
            # Hash C
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/hash/graph.c",
            "fiftyone_devicedetection_onpremise/device-detection-cxx/src/hash/hash.c",
        ],
        'cflags': cflags
    })

setup (cmdclass={'build_ext': NoSuffixBuilder},
        name = 'fiftyone_devicedetection_onpremise',
        version = '4.2.2',
        author      = '51Degrees.com',
        author_email='support@51degrees.com',
        description = """51Degrees Device Detection On-Premise Wrapper""",
        long_description ="This project contains 51Degrees Device Detection engines that can be used with the Pipeline API.The Pipeline is a generic web request intelligence and data processing solution with the ability to add a range of 51Degrees and/or custom plug ins (Engines)",
        license='EUPL-1.2',
        libraries=[cpplib, clib],
        ext_package = 'fiftyone_devicedetection_onpremise',
        ext_modules = [DeviceDetectionHashEngineModule],
        py_modules = ['fiftyone_devicedetection_onpremise'],
        packages=["fiftyone_devicedetection_onpremise"],
        install_requires=["fiftyone_devicedetection_shared"],
    )
