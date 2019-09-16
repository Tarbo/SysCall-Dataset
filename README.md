SysCall Dataset

# Design Notes
#Overview

- Everything executes in one Docker container.

- Within this Docker container is an instrumented version of the Bochs
CPU emulator

- The instrumentation works in such a way that syscall logging begins
when the VM user executes the Linux command `mkdir FlightBegin` and
logging ends when the user executes the Linux command `mkdir FlightEnd`.

- Therefore to log all CPU syscalls that occur when a process is
running, `mkdir FlightBegin; ./program; mkdir FlightEnd`


#Drone Physics Simulation

- Taking the ideas from the WVU AtLAS project I created a simple physics
model of a drone simulating:
	- 3 throttles (X axis, Y axis, Z axis)
	- Gravity of 9.81m/s^2
	- Aerodynamic drag

- This drone model connects to a virtual serial port and can be
interfaced with through the following commands:
	- TODO

- This drone is connected to the virtual serial port (using a Linux PTY)
of the Bochs VM.


#Auto-Piloting The Virtual Serial Port Drone

- A Python script running within the Bochs VM controls the drone
- The controller goes through the following states:
	- Take off:
		- Apply Z-axis throttle to move up to crusing altitude
	
	- Crusing:
		- Adjust Z-axis throttle to counteract gravity
		- Adjust X-axis and Y-axis throttles to move at a constant velocity to the destination
	
	- Landing:
		- Turn off X-axis and Y-axis throttles
		- Lower Z-axis throttle so that drone lowers smoothly
	
	- Landed:
		- Drone is on the ground and Python script exits

- I have generated data logs from three scenerios:
	1. Normal operation
	2. Random delay - the controller randomly lags behind due to computationally expensive operations
	3. Random syscall - to test anomaly detection the controller sometimes sends random UDP data to a port on 127.0.0.1


#The Results

- 001_NORMAL_Flight.txt: Runs properly, no code to interfere with performance

- 002_BUSYDELAY_Flight.txt: Time is sometimes spent in code used to factor large numbers
	this results in too slow polling of the drone's sensors and consequentially the drone
	flies too high before it comes down and crashes. It does not reach its destination.

- 003: 003_SOCKETS_Flight.txt: During crusing mode UDP packets are sent to random
	localhost ports. The flight proceeds properly, but there should be new syscalls
	mixed in.

# Raw Dataset Format
For entries with SYSCALL (left to right)
----------------------------------------

- Timestamp
- "SYSCALL"
- RAX (this is usually the name of the syscall, see: https://filippo.io/linux-syscall-table/)
- RDI (optional syscall argument)
- RSI (optional syscall argument)
- RDX (optional syscall argument)
- R10 (optional syscall argument)
- R8 (optional syscall argument)
- R9 (optional syscall argument)
- CR3 (process page table pointer which called this syscall)


For entries with SYSRET
-----------------------

- Timestamp
- CR3 (process page table pointer which called this syscall)

# Processed Dataset Format
From left to right
------------------
Ti-Ti-1 (Difference between current timestamp and previous timestamp values)
SysCall ID