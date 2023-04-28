import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("configfile", help="Path to configuration file")
parser.add_argument("instructions", help="Number of Instruction to simulate")
args = parser.parse_args()

benchmarks = {'401.bzip2':'../data/input.program','429.mcf':'../data/input.program','456.hmmer':'../data/input.program','458.sjeng':'../data/input.program','470.lbm':'100 output 0 1 ../data/100_100_130_cf_a.of'}
currentdir = "/home/010/j/jx/jxp220032/CS6304P2"
gem5build = currentdir + "/gem5/build/X86/gem5.opt"
cpuparams = "--cpu-type=timing --caches --l2cache --l1d_size=128kB --l1i_size=128kB --l2_size=1MB --l1d_assoc=2 --l1i_assoc=2 --l2_assoc=4 --cacheline_size=64"

for bm in benchmarks:
    benchmarkEXE = currentdir + "/Project1_SPEC/" + bm + "/src/benchmark"
    simulationConfig = args.configfile
    benchmarkARGS = benchmarks[bm]
    outputstats = simulationConfig +"_"+bm
    statsdir = currentdir + "/simstats/"+outputstats
    simulationCMD = f"time" + gem5build + "-d" +statsdir+" "+simulationConfig+" -c "+benchmarkEXE+" -o "+benchmarkARGS+" -I "+args.instructions+ " "+cpuparams
    subprocess.Popen(simulationCMD, shell=True)






