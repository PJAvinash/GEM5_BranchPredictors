import argparse
import subprocess
import concurrent.futures

parser = argparse.ArgumentParser()
parser.add_argument("configfile", help="Path to configuration file")
parser.add_argument("instructions", help="Number of Instruction to simulate")
args = parser.parse_args()


currentdir = "/home/010/j/jx/jxp220032/CS6304P2"
benchmarks = {'401.bzip2':currentdir + '/Project1_SPEC/401.bzip2/data/input.program','429.mcf':currentdir +'/Project1_SPEC/429.mcf/data/input.program','456.hmmer':currentdir + '/Project1_SPEC/456.hmmer/data/input.program','458.sjeng':currentdir + '/Project1_SPEC/458.sjeng/data/input.program','470.lbm':'100 output 0 1 '+ currentdir + '/Project1_SPEC/470.lbm/data/100_100_130_cf_a.of'}
gem5build = currentdir + "/gem5/build/X86/gem5.opt"
cpuparams = "--cpu-type=timing --caches --l2cache --l1d_size=128kB --l1i_size=128kB --l2_size=1MB --l1d_assoc=2 --l1i_assoc=2 --l2_assoc=4 --cacheline_size=64"
csize = 2048
lsize = 1048
gsize = 4096
branchpredictor = 0 #0,1,2

def simulateForParams(branchpredictor,lsize,gsize,csize):
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for bm in benchmarks:
            benchmarkEXE = currentdir + "/Project1_SPEC/" + bm + "/src/benchmark"
            simulationConfig = args.configfile
            benchmarkARGS = benchmarks[bm]
            outputstats = bm +"_"+str(branchpredictor)+"_"+str(lsize)+"_"+str(gsize)+"_"+str(csize)
            statsdir = currentdir + "/simstats/"+outputstats
            simulationCMD = 'time ' + gem5build + ' -d ' +statsdir+' '+simulationConfig+' --bpredictortype='+ str(branchpredictor) + ' --lsize=' +str(lsize)+' --gsize='+str(gsize)+' --csize='+str(csize)+ ' -c '+benchmarkEXE+' -o "'+benchmarkARGS+'" -I '+args.instructions+ ' '+cpuparams
            future = executor.submit(subprocess.call, simulationCMD, shell=True)
            futures.append(future)
        for future in futures:
            future.result()


#local predictor
for ls in [1024,2048,4096]:
    simulateForParams(0,ls,1024,1024)

#biModal
for gs in [1024,2048,4096]:
    for cs in [1024,2048,4096]:
        simulateForParams(1,1024,gs,cs)
#tournament
for gs in [1024,2048,4096]:
    for cs in [1024,2048,4096]:
        for ls in [1024,2048,4096]:
            simulateForParams(2,ls,gs,cs)





