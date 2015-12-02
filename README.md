## pyRuntable
#### Distributed Python runtime via distributed hash tables.

A distributed runtime system is one which uses more than one machine to run a system, in this case, a Python runtime.
It has native support for parallel computing, which efficiently utilizes machines to reach a common goal.

In this runtime system, I introduce a system capable of scaling dynamically, master nodes capable of executing code
on the network, and worker nodes, which share the computational load to reach the goal put out by the master node.