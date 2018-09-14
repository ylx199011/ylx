#!/usr/bin/env python
# encoding: utf-8

from os import listdir, walk, makedirs, devnull
from os.path import isdir, isfile, join, splitext
from shutil import copy, rmtree
from ntpath import basename
from itertools import izip_longest as izl
import csv
import time
import numpy
import sys
import re
import subprocess as sp


homework_path="homework"   # Where to find homework files
name='name.csv'            # List of No and names. Fill it by hand then leave it alone
grade='grade.csv'          # List of grades


def collect_files():
    for d in [homework_path, 'img', 'backup', 'code']:
        if (d in ['img','code']) and isdir(d):  # Clear images and codes of last time
            rmtree(d)
        if not isdir(d):
            makedirs(d)

    if not listdir(homework_path):
        print 'Please unzip homework into directory '+homework_path+'!'
        exit()

    for f in [grade,'run_results.txt']:
        if isfile(f):            # Backup grade file of last time
            fs=f.split('.')
            copy(f, 'backup/'+fs[0]+'_'+
                    time.strftime("%y-%m-%d_%H-%M-%S", time.localtime())+'.'+fs[1])

    codefiles=[]; imgfiles=[]    # Collect codes and images, copy to code/ and img/
    for root, dirs, files in walk(homework_path):
        for f in files:
            if f.lower().endswith(('.png', '.jpg', '.jpeg', 'docx')):
                imgf=join(root,f)
                imgfiles.append(imgf)
                copy(imgf,"img")
            elif f.lower().endswith(('.c', '.cpp')):
                codef=join(root,f)
                codefiles.append(codef)
                copy(codef,"code")

    return codefiles, imgfiles


def csv_write(names, grades):
    nt=map(list, zip(*names))[0]
    a = numpy.asarray(list(izl(nt, grades)))
    numpy.transpose(a)
    numpy.savetxt(grade, a, fmt='%s', delimiter=",")


def csv_read():
    with open(name, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        return map(tuple, reader)


def get_basename(f):
    bn=''; w=0
    bn=splitext(basename(f))[0]
    try:
        w=int(re.sub('[a-z]', '', bn[-2:]))
    except ValueError:
        pass
    return bn, w


def void2int(code):
    return re.sub('void +main', 'int main', code, flags=re.M)


def dos2unix(filename):
    data = open(filename, "rb").read()
    code = data.replace("\r\n", "\n")
    newdata=void2int(code)
    if newdata != data:
        f = open(filename, "wb")
        f.write(newdata)
        f.close()


def exec_code(code, bn):
    dos2unix(code)
    cmd="g++ -o code/"+bn+" "+code
    with open(devnull, 'w') as shutup:
        return sp.call(cmd, shell=True, stdout=shutup, stderr=shutup)


def rate():
    codefiles, imgfiles = collect_files()
    grades=[]
    names=csv_read()

    for n in names:   # One student at a time
        no=n[0][-2:]  # student ID
        f_num=[0,0]   # count number of codes and images

        for cf in codefiles:     # find codes for current student
            bn, w=get_basename(cf)
            if bn[:2]==no:       # got it
                f_num[0]+=1
                code='code/'+basename(cf)  # Switch to code directory
                returned_value=exec_code(code, bn)
                if returned_value==0:      # compile success
                    if f_num[0]==1:        # first compile rate C
                        grades.append('C')
                else:                      # compile failure
                    if f_num[0]==1:
                        grades.append('D') # first compile rate D
                    print n[0], "compile failure!"
        if f_num[0]==0:
            grades.append('F')
            print n[0], "didn't deliver codes. "

        for imf in imgfiles:     # find images for current student
            bn, w=get_basename(imf)
            if bn[:2]==no:       # got it
                f_num[1]+=1
                if grades[-1]=='C':
                    grades[-1]='A'   # codes success plus images rate A
                elif grades[-1]=='D':
                    grades[-1]='B'   # codes failure plus images rate B
                elif grades[-1]=='F':
                    grades[-1]='E'   # no codes plus images rate E
                else:
                    print n[0], "codes didn't rate C, D or F!"
            if f_num[1]>0:
                break    # only check the existence of one image
        if f_num[1]==0:
            print n[0], "didn't deliver images. "

    csv_write(names, grades)



rate()
