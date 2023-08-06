# Flattened Device Tree Python Module 

[![Build Status](https://travis-ci.org/molejar/pyFDT.svg?branch=master)](https://travis-ci.org/molejar/pyFDT)
[![Coverage Status](https://coveralls.io/repos/github/molejar/pyFDT/badge.svg)](https://coveralls.io/github/molejar/pyFDT)
[![PyPI Status](https://img.shields.io/pypi/v/fdt.svg)](https://pypi.python.org/pypi/fdt)
[![Python Version](https://img.shields.io/pypi/pyversions/fdt.svg)](https://www.python.org)

This python module is usable for manipulation with [Device Tree Data](https://www.devicetree.org/) and primary was 
created for [imxsb tool](https://github.com/molejar/imxsb)

> Some parts in this module have been inspired from: https://github.com/superna9999/pyfdt project.

## Installation

```bash
pip install fdt
```

To install the latest version from master branch execute in shell following command:

```bash
pip install -U https://github.com/molejar/pyFDT/archive/master.zip
```

In case of development, install it from cloned sources:

```bash
git clone https://github.com/molejar/pyFDT.git
cd pyFDT
pip install -U -e .
```

**NOTE:** You may run into a permissions issues running these commands. Here are a few options how to fix it:

1. Run with `sudo` to install `fdt` and dependencies globally
2. Specify the `--user` option to install locally into your home directory (export "~/.local/bin" into PATH variable if haven't).
3. Run the command in a [virtualenv](https://virtualenv.pypa.io/en/latest/) local to a specific project working set.

## Usage

**fdt** module has intuitive and self describing API, what is presented in following example. Many of general requirements 
for manipulation with FDT Nodes, Properties and dts/dtb files are already implemented.

```python
  import fdt
  
  #-----------------------------------------------
  # convert *.dtb to *.dts
  # ----------------------------------------------
  with open("example.dtb", "rb") as f:
      dtb_data = f.read()

  dt1 = fdt.parse_dtb(dtb_data)
  
  with open("example.dts", "w") as f:
      f.write(dt1.to_dts())

  #-----------------------------------------------
  # convert *.dts to *.dtb
  # ----------------------------------------------
  with open("example.dts", "r") as f:
      dts_text = f.read()

  dt2 = fdt.parse_dts(dts_text)
  
  with open("example.dtb", "wb") as f:
      f.write(dt2.to_dtb(version=17))

  #-----------------------------------------------
  # add new Node into dt2
  # ----------------------------------------------
  # create node instance
  node = fdt.Node('test_node1')
  
  # add properties
  node.append(fdt.Property('basic_property'))
  node.append(fdt.PropStrings('string_property', 'value1', 'value2'))
  node.append(fdt.PropWords('words_property', 0x80000000))
  node.append(fdt.PropBytes('bytes_property', 0x00, 0x01, 0x02))
  
  # PropBytes constructor take also complex data object as bytes() or bytearray()
  node.append(fdt.PropBytes('bytes_property2', data=b"\x00\x01\x02"))
  
  # add created node into root path of dt2
  dt2.add_item(node)
  
  # use set_property method to update or create new property
  dt2.set_property('words_property', [0, 1], path='/test_node1')
  dt2.set_property('bytes_property', b"\x00\x01", path='/test_node1')
  dt2.set_property('string_property', ['value1', 'value2', 'value3'], path='/test_node1')  
  
  # use search method for find all string properties and then update it
  items = dt2.search("", itype=fdt.ItemType.PROP_STRINGS, path="/test_node1")
  for item in items:
    item.data = ['value1', 'value2']
  
  #-----------------------------------------------
  # merge dt2 into dt1
  # ----------------------------------------------
  dt1.merge(dt2)

  with open("merged.dtb", "wb") as f:
      f.write(dt1.to_dtb(version=17))

  #-----------------------------------------------
  # diff two fdt objects
  # ----------------------------------------------
  out = fdt.diff(dt1, dt2)
  
  print(out[0]) # same in dt1 and dt2
  print(out[1]) # specific for dt1
  print(out[2]) # specific for dt2
```

## [ pydtc ] Tool

The python device tree converter **pydtc** is a tool for conversion *.dts to *.dtb and vice versa. Is distributed
together with **fdt** module. This tool can be in some cases used as replacement of [device tree compiler](https://git.kernel.org/pub/scm/utils/dtc/dtc.git).  

```bash
  $ pydtc -h

usage: pydtc [-h] [-v] {pack,unpack,merge,diff} ...

Flat Device Tree (FDT) tool for manipulation with *.dtb and *.dts files

positional arguments:
  {pack,unpack,merge,diff}
    pack                Pack *.dts into binary blob (*.dtb)
    unpack              Unpack *.dtb into readable format (*.dts)
    merge               Merge more files in *.dtb or *.dts format
    diff                Compare two files in *.dtb or *.dts format

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

```

#### $ pydtc unpack [-h] [-s TAB_SIZE] [-o DTS_FILE] dtb_file

Unpack Device Tree from binary blob *.dtb into readable text file *.dts

**dtb_file** - Single DTB file with `dtb` extension

##### optional arguments:
* **-h, --help** - Show this help message and exit
* **-s TAB_SIZE** - Tabulator Size
* **-o DTS_FILE** - Output path/file name (*.dts)

##### Example:

```bash
pydtc unpack test.dtb
    
DTS saved as: test.dts
```

#### $ pydtc pack [-h] [-v VERSION] [-l LC_VERSION] [-c CPU_ID] [-p] [-o DTB_FILE] dts_file


Pack Device Tree from readable text file *.dts into binary blob *.dtb

**dts_file** - Single DTS file as *.dts

##### optional arguments:
* **-h, --help** - Show this help message and exit
* **-v VERSION** - DTB Version
* **-l LC_VERSION** - DTB Last Compatible Version
* **-c CPU_ID** - Boot CPU ID
* **-p** - Update phandle
* **-o DTB_FILE** - Output path/file name (*.dtb)

##### Example:

``` bash
pydtc pack -v 17 test.dts
  
DTB saved as: test.dtb
```

#### $ pydtc merge [-h] [-t {auto,dts,dtb}] [-s TAB_SIZE] out_file in_files [in_files ...]


Merge two and more *.dtb or *.dts files into one *.dts file

**out_file** - The output file name with *.dts extension <br>
**in_files** - Two or more input files with *.dtb or *.dts extension

##### optional arguments:
* **-h, --help** - Show this help message and exit
* **-t {auto,dts,dtb}** - Input file type: 'auto', 'dts', 'dtb' (default: auto)
* **-s TAB_SIZE** - Tabulator Size

##### Example:

```bash
pydtc merge out.dts test1.dtb test2.dtb
    
Output saved as: out.dts
```

#### $ pydtc diff [-h] [-t {auto,dts,dtb}] [-o OUT_DIR] in_file1 in_file2

Compare two dtb/dts files and generate 3 dts files (same in 1 and 2, specific for 1, specific for 2)

**in_file1** - Input file 1 <br>
**in_file2** - Input file 2

##### optional arguments:
* **-h, --help** - Show this help message and exit
* **-t {auto,dts,dtb}** - Input file type: 'auto', 'dts', 'dtb' (default: auto)
* **-o OUT_DIR** - Output directory (default: diff_out)

##### Example:

```bash
pydtc diff test1.dtb test2.dtb
    
Output saved into: diff_out
```
