#!/usr/bin/env bash



function del_build_cacne() {
    rm -rf djmyframework.egg-info/
    rm -rf djmyframework-*/
    rm -rf build/
    rm -rf dist/
}



del_build_cacne

python setup.py sdist build
twine upload dist/* $*

read -p "delete build cache y/n?" ask
if [ $ask == "y" ] ; then
del_build_cacne
fi