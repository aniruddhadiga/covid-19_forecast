#!/bin/bash
st_list="../input/st_list.txt"
#input_cnty="../input/va_cnty_list.txt"
input_hrzn="../input/hrzn_list_curr.txt"
while IFS= read -r st
do
        #echo $cnty $hrzn
    sbatch stjob.sbatch $st $cnty $input_hrzn
            #qreg
done < $st_list

#while IFS= read -r st
#do
#    while IFS= read -r cnty
#    do
#        echo $st $cnty
#        sbatch job.sbatch $st $cnty $input_hrzn
#    done < "$st"
#done < "$st_list"
