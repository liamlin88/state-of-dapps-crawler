#!/bin/sh

echo "begin crawl"
DATE=$(date +%d-%m-%Y)
cd /Users/linzhitao/VscodeProjects/Sail/tutorial

#scrapy crawl mainpage_promote -o data/promote/$DATE-mainpage_promote.csv
#scrapy crawl features -o data/feature/$DATE-feature.csv
#scrapy crawl dapps -o data/dapp/$DATE-dapp.csv

scrapy crawl mainpage_promote -t csv -o - >"data/promote/$DATE-mainpage_promote.csv"
scrapy crawl features -t csv -o - >"data/feature/$DATE-feature.csv"
scrapy crawl dapps -t csv -o - >"data/dapp/$DATE-dapp.csv"
