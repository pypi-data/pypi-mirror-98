#!/bin/bash

C() {
    echo -e "\033[0;30m\033[46m$1\033[0m"
}

INFO() { 
    echo
    C "# $1"
    echo
} 
