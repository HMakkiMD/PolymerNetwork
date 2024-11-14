#!/bin/bash
mkdir analysis
start=0
end=5000
max_end=43000

counter=1

while [ $end -le $max_end ]; do
  echo 22 | gmx energy -f tg_3.edr -s tg_3.tpr -o analysis_p/density-$counter.xvg -b $start -e $end
  start=$end
  end=$((end + 2000))
  counter=$((counter + 1))
done
