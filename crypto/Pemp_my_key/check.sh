#!/bin/bash

target="/jeannedhackctf/"
keyfile=${1}

if [[ -z $keyfile ]]; then
	echo "Usage: $0 <keyfile>"
	exit 1
fi

rsa_check=$(openssl rsa -check -in ${keyfile} -noout)
if [[ $rsa_check == "RSA key ok" ]]; then
	echo "[+] $rsa_check"
else
	echo "[-] $rsa_check"
	exit 1
fi

key_content=$(openssl rsa -in ${keyfile} -traditional 2>/dev/null | tr -d '\n')
if [[ $target == $(echo "${key_content}" | grep -o ${target}) ]]; then
	echo "[+] Key contains pattern"
else
	echo "[-] Key doesn't contain pattern"
	exit 1
fi
