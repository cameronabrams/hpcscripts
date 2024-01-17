# Author: Cameron F. Abrams, <cfa22@drexel.edu>
#
# NAMD restart config file generator
#
import argparse as ap 
import os
import subprocess

def get_config_val(Clines,keyword,type=int):
    has_keyword=any([l.startswith(keyword) for l in Clines])
    if has_keyword:
        value=type(configlines[[l.startswith(keyword) for l in configlines].index(True)].split()[-1])
        return value
    return None

def myfc(filename):
    return '😎' if os.path.exists(filename) else '😠'

def hhmmss(**kwargs):
    totalsec=kwargs.get('seconds',0)
    totalhours=kwargs.get('hours',0.0)
    totalminutes=kwargs.get('minutes',0.0)
    if totalsec:
        wholemin=totalsec//60
        remsec=totalsec%60
        wholehr=wholemin//60
        remmin=wholemin%60
        return f'{wholehr:02d}:{remmin:02d}:{remsec:02d}'
    else:
        return "not yet"
    
config_ignores=['#','run','set outputname'] # purge these!
config_replaces=['bincoordinates','binvelocities','extendedsystem','firsttimestep','numsteps']

if __name__=='__main__':
    parser=ap.ArgumentParser()
    parser.add_argument('-i',type=str,required=True,help='most recent namd config file')
    parser.add_argument('-l',type=str,required=True,help='namd log file from run generated from most recent namd config file')
    parser.add_argument('-o',type=str,required=True,help='new namd config file')
    parser.add_argument('--new-numsteps',type=int,help='new maximum total number of steps for this series of namd runs')
    parser.add_argument('--addsteps',type=int,help='run this many steps from the current latest checkpoint')
    parser.add_argument('--tarball',action='store_true',help='make a production tarball')
    args=parser.parse_args()
    replacements={}
    replaced={}
    with open(args.i,'r') as f:
        configlines=[x.strip() for x in f.read().split('\n') if len(x)>0]
        for i in range(len(configlines)):
            try:
                l=configlines[i].index(' ')
            except:
                raise Exception(f'bad line? [{configlines[i]}]')
            fw=configlines[i][:l].lower()
            configlines[i]=fw+' '+configlines[i][l+1:]
        print(f'{args.i}: {len(configlines)} lines')
    with open(args.l,'r') as f:
        loglines=f.read().split('\n')
        print(f'{args.l}: {len(loglines)} lines')
    
    wallsec_per_timestep=0.0
    nsamp=0
    for l in loglines:
        if l.startswith('TIMING'):
            wallsec_per_timestep+=float(l.split()[4][:-5])
            nsamp+=1
    wallsec_per_timestep/=nsamp
    outbasename,outext=os.path.splitext(args.o)

    # input config parsing
    # begin collecting necessary file names
    FILES=[]
    print(f'{args.i}:')
    for l in configlines:
        if any([l.startswith(x) for x in ['structure','coordinates','colvarsconfig','tmdfile','parameters']]):
            print(f'    extracting filename from "{l}"')
            FILES.append(l.split()[-1])
    firsttimestep=get_config_val(configlines,'firsttimestep')
    run=get_config_val(configlines,'run')
    numsteps=get_config_val(configlines,'numsteps')
    restartfreq=get_config_val(configlines,'restartfreq')
    outputname=get_config_val(configlines,'outputname',str)
    if outputname:
        if outputname.startswith('$'):
            outputname_var=outputname[1:]
            outputname=get_config_val(configlines,f'set {outputname_var}',str)

    if firsttimestep:
        print(f'    found "firsttimestep" of {firsttimestep}')
    if restartfreq:
        print(f'    found "restartfreq" of {restartfreq}')
    if run:
        print(f'    found "run" of {run}')
    if numsteps:
        print(f'    found "numsteps" of {numsteps}')
    if outputname:
        print(f'    found "outputname" of {outputname}')

    # log parsing:
    run_finished=any(['CLOSING COORDINATE DCD FILE' in l for l in loglines])
    if run_finished:
        try:
            last_write=['WRITING COORDINATES TO OUTPUT FILE AT STEP' in l for l in loglines[::-1]].index(True)
            last_write_step=int(loglines[-last_write-1].split()[-1])
        except:
            raise Exception(f'Cannot determine checkpoint from {args.l}')
    else:
        try:
            last_writeline=['WRITING COORDINATES TO RESTART FILE AT STEP' in l for l in loglines[::-1]].index(True)
            last_write_step=int(loglines[-last_writeline-1].split()[-1])
        except:
            raise Exception(f'Cannot determine checkpoint from {args.l}')
    # detect ensemble
    has_langevin_thermostat=any(['LANGEVIN DYNAMICS ACTIVE' in l for l in loglines])
    has_langevin_barostat=any(['LANGEVIN PISTON PRESSURE CONTROL ACTIVE' in l for l in loglines])
    tidx=['Info: LANGEVIN TEMPERATURE' in l for l in loglines].index(True)
    langevin_temperature=float(loglines[tidx].split()[-1])
    current_ensemble=None
    if has_langevin_thermostat:
        current_ensemble='nvt'
        if has_langevin_barostat:
            current_ensemble='npt'

    if args.new_numsteps:
        print(f'New numsteps is {args.new_numsteps}')

    if args.addsteps:
        print(f'adding {args.addsteps}')

    print(f'{args.l}:')
    print(f'             has_langevin_thermostat {has_langevin_thermostat}')
    print(f'                langevin temperature {langevin_temperature}')
    print(f'               has_langevin_barostat {has_langevin_barostat}')
    print(f'                     last_write_step {last_write_step}')
    
    if run:
        run_target_numsteps=num_steps=firsttimestep+run
    elif numsteps:
        run_target_numsteps=numsteps

    stepsleft=run_target_numsteps-last_write_step
    print(f'                          steps left {stepsleft}')
    print(f'          wall seconds per time step {wallsec_per_timestep}')
    if run_finished:
        print(f'                        run finished 😎')
    else:
        print(f'          run terminated prematurely 😠')
    stepsrequested=stepsleft
    numsteps=run_target_numsteps
    if args.new_numsteps:
        if args.new_numsteps<last_write_step:
            raise Exception(f'You have requested a maximum total number of steps ({args.new_numsteps}) that is less than the step of the last write ({last_write_step})')
        else:
            stepsrequested=args.new_numsteps-last_write_step
            numsteps=args.new_numsteps
    elif args.addsteps:
        stepsrequested=args.addsteps
        numsteps=last_write_step+stepsrequested
    
    if stepsrequested==0:
        print(f'No more steps needed or requested')
    else:
        wall_sec_requested=int(wallsec_per_timestep*stepsrequested)
        firsttimestep=last_write_step
        if run_finished:
            bincoordinates=f'{outputname}.coor'
            binvelocities =f'{outputname}.vel'
            extendedsystem=f'{outputname}.xsc'
        else:
            bincoordinates=f'{outputname}.restart.coor'
            binvelocities =f'{outputname}.restart.vel'
            extendedsystem=f'{outputname}.restart.xsc'
        FILES.extend([bincoordinates,binvelocities,extendedsystem])

        print(f'{args.o}:')
        all_files=True
        for f in FILES:
            print(f'{f:>36s} {myfc(f)}')
            if not os.path.exists(f):
                all_files=False
        if not all_files:
            raise Exception(f'One or more required files not found.')

        replacements['outputname']=outbasename
        replacements['firsttimestep']=firsttimestep
        replacements['bincoordinates']=bincoordinates
        replacements['binvelocities']=binvelocities
        replacements['extendedsystem']=extendedsystem
        replacements['numsteps']=numsteps
        replaced['outputname']=False
        replaced['firsttimestep']=False
        replaced['bincoordinates']=False
        replaced['binvelocities']=False
        replaced['extendedsystem']=False
        replaced['numsteps']=False

        print(f'                   new firsttimestep {firsttimestep}')
        print(f'                        new numsteps {numsteps}')
    
        with open(args.o,'w') as f:
            f.write(f'# restart config generated from {args.i} and {args.l}\n')
            for l in configlines:
                if not any([l.startswith(x) for x in config_ignores]):
                    hit=False
                    for k,v in replacements.items():
                        if l.startswith(k):
                            hit=True
                            replaced[k]=True
                            f.write(f'{k} {v}\n')
                            break
                    if not hit:
                        f.write(f'{l}\n')
            if not replaced['numsteps']:
                f.write(f'numsteps {numsteps}\n')
        print(f'Generated {args.o}.')
        print(f'Approx. wall hours needed: {hhmmss(seconds=wall_sec_requested)}')
        if args.tarball:
            FILES.append(args.o)
            c=f'tar zvcf {outbasename}.tgz '+' '.join(FILES)
            process=subprocess.Popen(c,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
            stdout,stderr=process.communicate()
            print(f'Generated {outbasename}.tgz')