Backends:
--------------------------------------------------------------------------------------
Support adding more backends ... develop a normalized API for Backend engine.
NOTE: the following interface will hinder the use of Probe() debugging gate
. The backend interface should allow 
	X create a job, to include
		X initial state (like initstate, prepqubits)
		X circuit
		X # shots
	* submit job
	* async/sync wait for job to complete
	X job method to get result object

	* Result object to allow
		* get cregister values list for all shots
		* get cregister values for any specifc shot
		* number of shots results
		* get stats on cregister values across all shots
		* if simulator, get values list of all state vectors

X Support multiple Backends by defining a class with that interface, and then implement that
class for each Backend type.

X Allow looking up Backends by name, and then instantiate as the backend object to run
ckts, and get CRegister contants, and in simulator backends, also allow inspecting
state vector any time.

. QRegister and CRegister classes operations - when any list operations are performed on 
these objects of these classes, the returned object is of type 'list'
