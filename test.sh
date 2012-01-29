#!/bin/bash
# small test script as post call script for sicksubs
for i in $*
do
	touch "$i"".works"
done
