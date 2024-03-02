
for x in $(ls -d ./genome*); do
       pushd $x
       rep=${x#./}
       for distance in 0.01 0.05 0.07 0.1 0.15; do
               mkdir "./mut_${rep}"
               mkdir "./mut_${rep}/${distance}/"
               python ../make_genomes.py existing --existing-dir "./genome/" \
                       --out-dir "./mut_${rep}/${distance}/" \
                       --mutation-prob "${distance}" &
       done
       wait
       popd
done
