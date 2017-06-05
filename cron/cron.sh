#!/bin/bash
while true;
do

  sleep 3;
   $(wget http://191.232.184.136/exchange/fetchall &> /dev/null);

   sleep 3;
   $(wget http://191.232.184.136/processor/new &> /dev/null);

done
