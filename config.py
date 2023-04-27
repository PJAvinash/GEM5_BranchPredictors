#testing

import m5
from m5.objects import *
from m5.util import *

# Parse options
parser = argparse.ArgumentParser()
parser.add_argument('config', help='configuration file')
args = parser.parse_args()

# Load the configuration file/s
system = System()
system.read_config(args.config)

# Create the memory system
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('0x00000000', size=system.mem_size)]

# Create the CPU
system.cpu = TimingSimpleCPU()

# Create the cache hierarchy
system.cpu.icache = L1Cache()
system.cpu.dcache = L1Cache()

# Connect the CPU to the memory system
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)
system.cpu.icache.connectBus(system.membus)
system.cpu.dcache.connectBus(system.membus)

# Create the memory controller and connect it to the memory bus
system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master
system.membus.slave = system.mem_ctrl.port

# Set up the branch predictor
system.cpu.branchPred = BimodalBP(size=2048)

# Create the process
process = Process()
process.cmd = ['hello']
system.cpu.workload = process
system.cpu.createThreads()

# Run the simulation
root = Root(full_system=False, system=system)
m5.instantiate()

print("Beginning simulation...")
exit_event = m5.simulate()

print('Exiting @ tick', m5.curTick(), 'because', exit_event.getCause())
