#!/bin/bash
#
# Job script submitter for 
# umbrella sampling MD runs
#
# expects a directory structure like
# `-- US2
#    |-- delta
#    |   |-- rep1
#    |   |   `-- runfiles
#    |   |-- rep2
#    |   |   `-- runfiles
#    |   |-- rep3
#    |   |   `-- runfiles
#    |   |-- rep4
#    |   |   `-- runfiles
#    |   `-- rep5
#    |       `-- runfiles
#    `-- wt
#        |-- rep1
#        |   `-- runfiles
#        |-- rep2
#        |   `-- runfiles
#        |-- rep3
#        |   `-- runfiles
#        |-- rep4
#        |   `-- runfiles
#        `-- rep5
#            `-- runfiles
#
# Each 'runfiles' directory has all necessary NAMD input files
# for a series of MD simulations, each one signaled by a *.namd file
# with a name in the form *_frm[0-9]*.namd
#
# us.sh is a template job script
#
OWD=`pwd`
for t in US2/wt US2/delta; do
    cd $t
    T=${t##*/}
    for d in rep?; do
	R=${d##*rep}
        cd $d/runfiles
	for r in `echo *_frm[0-9]*namd`; do
            n=`grep -c structure $r`
	    if [[ $n > 0 ]]; then
	       PREF=${r%.namd}
	       echo "Will run on $t/$d/runfiles/$r"
	       cat $OWD/us.sh | sed s/%CONFIG%/$r/ \
	   	              | sed s/%LOG%/${PREF}.log/ \
			      | sed s/%T%/$T/ \
			      | sed s/%R%/$R/ \
			      | sed s/%PREF%/$PREF/ > us-${PREF}.sh
	       echo "Generated jobscript us-${PREF}.sh"
	       qsub us-${PREF}.sh
	       sleep 1
	    else
	       echo "$r is a bad namd file."
	    fi
	done
	cd ../..
    done
    cd $OWD
done

