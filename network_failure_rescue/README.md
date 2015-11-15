The internal swift-cluster architecture depends on a permanent communication between its storage nodes. 
So in case of network failure, like the one we have faces today, the binding IPs in configuration files on all nodes 
needs to be changes to the new @IPs, for that th automation of that task is very important to decrease the failure downtime 
of the swift cluster.  