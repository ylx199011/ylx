#!/bin/bash

cd "code"

for f in *.c *.cpp
do
    sed -i 's/void +main/int main/g' "$f"        # void2int
    sed -i 's/\r\n/\n/g' "$f"                    # dos2unix
    a=$(basename "$(basename "$f" ".c")" ".cpp") # basename
    echo "--------Checking $f !---------------------------------------------"
    if g++ -o "$a" "$f"; then
        echo "--------$f compile success!---------------------------------------"
        chmod 777 "$a"
        if ./"$a"; then
            echo;echo "--------$f execute success!---------------------------------------"
        else
            echo;echo "--------$f execute failure!---------------------------------------"
        fi
    else
        echo "--------$f compile failure!---------------------------------------"
    fi
    printf "\n\n\n"
done
