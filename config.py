#testing
import sys
import m5
from m5.objects import *
from m5.util import *

parser = argparse.ArgumentParser()
parser.add_argument("branchpredtype", help="Branch predictor type")
parser.add_argument("lsize", help="local Predictor Size")
parser.add_argument("gsize", help="global Predictor Size")
parser.add_argument("csize", help="choice Predictor Size")
parser.add_argument("exe", help="executable binary")
args = parser.parse_args()


system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('0x00000000', size='512MB')]

system.cpu = TimingSimpleCPU()
system.cpu.icache = L1Cache(size='16kB')
system.cpu.dcache = L1Cache(size='16kB')

system.membus = SystemXBar()

system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

system.cpu.icache.connectBus(system.membus)
system.cpu.dcache.connectBus(system.membus)

system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master
system.membus.slave = system.mem_ctrl.port

system.cpu.branchPred = BimodalBP(size=2048)


# Set up the branch predictor
if int(args.branchpredtype) == 0:
    system.cpu.branchPred = BiModeBP(
        globalPredictorSize = int(args.gsize),
        choicePredictorSize = int(args.csize),
    )
    

if int(args.branchpredtype) == 1:
    system.cpu.branchPred = TournamentBP(
        globalPredictorSize = int(args.gsiz),
        choicePredictorSize = int(args.csize),
        localPredictorSize = int(args.lsize),
        predictor = LocalBP(),
        predictor2 = BimodalBP()
    )
    

if int(args.branchpredtype) == 2:
    system.cpu.branchPred = LocalBP(
        localPredictorSize = int(args.lsize),
    )
# Create the process
process = Process()
process.cmd = [args.exe]
system.cpu.workload = process
system.cpu.createThreads()

# Run the simulation
root = Root(full_system=False, system=system)
m5.instantiate()

print("Beginning simulation...")
exit_event = m5.simulate()

print('Exiting @ tick', m5.curTick(), 'because', exit_event.getCause())
