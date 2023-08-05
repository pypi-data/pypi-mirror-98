# Example
Author(s):  Daan van den Bergh<br>
Copyright:  © 2020 Daan van den Bergh All Rights Reserved<br>
<br>
<br>
<p align="center">
  <img src="https://raw.githubusercontent.com/vandenberghinc/public-storage/master/vandenberghinc/icon/icon.png" alt="Bergh-Encryption" width="50"/>
</p>

## Installation
	pip3 install example

## CLI:
	Usage: example <mode> <options> 
	Modes:
	    -h / --help : Show the documentation.
	Options:
	Author: Daan van den Bergh 
	Copyright: © Daan van den Bergh 2020. All rights reserved.

## Python Examples.

Initialize the encryption class (Leave the passphrase None if you require no passphrase).
```python
# initialize the encryption class.
encryption = Encryption(
	key='mykey/',
	passphrase='MyPassphrase123!')
```
