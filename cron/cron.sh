#!/bin/bash
while true;
do

   sleep 10;
   $(wget -q http://191.232.184.136/exchange/fetchall);
 
   sleep 10;
   $(wget -q http://191.232.184.136/processor/new);

done
