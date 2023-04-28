#testing
import argparse
import sys
import m5
from m5.objects import *
from m5.util import *
from caches import *


system = System()
# Set the clock frequency of the system (and all of its children)
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()
# Set up the system
system.mem_mode = "timing"  # Use timing accesses
system.mem_ranges = [AddrRange("512MB")]  # Create an address range
# Create a simple CPU
system.cpu = BaseSimpleCPU()
# Create an L1 instruction and data cache
system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()
# Connect the instruction and data caches to the CPU
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)
# Create a memory bus, a coherent crossbar, in this case
system.l2bus = L2XBar()
# Hook the CPU ports up to the l2bus
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)
# Create an L2 cache and connect it to the l2bus
system.l2cache = L2Cache()
system.l2cache.connectCPUSideBus(system.l2bus)
# Create a memory bus
system.membus = SystemXBar()
# Connect the L2 cache to the membus
system.l2cache.connectMemSideBus(system.membus)
# create the interrupt controller for the CPU
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports
# Connect the system up to the membus
system.system_port = system.membus.cpu_side_ports
# Create a DDR3 memory controller
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports


parser = argparse.ArgumentParser()
parser.add_argument("branchpredtype", help="Branch predictor type")
parser.add_argument("lsize", help="local Predictor Size")
parser.add_argument("gsize", help="global Predictor Size")
parser.add_argument("csize", help="choice Predictor Size")
parser.add_argument("exe", help="executable binary")
args = parser.parse_args()

system.cpu.branchPred = BimodalBP(size=2048)

system.max_insts_any_thread = 100000
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
process.cmd = args.exe.split(":")
system.cpu.workload = process
system.cpu.createThreads()

# Run the simulation
root = Root(full_system=False, system=system)
m5.instantiate()

print("Beginning simulation...")
exit_event = m5.simulate()

print('Exiting @ tick', m5.curTick(), 'because', exit_event.getCause())
