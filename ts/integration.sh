#!/bin/bash

try
    docker run -itd -p 5005:5005 -p 6006:6006 --name standalone --rm gcr.io/metaxrplorer/dangell7-1-10-0-rc4-standalone:1
catch
    docker rm -f standalone
		docker run -itd -p 5005:5005 -p 6006:6006 --name standalone --rm gcr.io/metaxrplorer/dangell7-1-10-0-rc4-standalone:1
end

yarn install && yarn run test test/integration
