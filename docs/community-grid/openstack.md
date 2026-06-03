# OpenStack

!!! note "Source"
    Mirrored from [OpenStack](https://dallasmakerspace.org/wiki/OpenStack) on the Dallas Makerspace wiki (CC BY-SA 3.0).

[OpenStack](http://openstack.org/) is open source software to build private and public clouds. There are three main components:

- OpenStack [Compute](http://openstack.org/projects/compute/) (nova): Provision and manage large networks of virtual machines
- OpenStack [Object Store](http://openstack.org/projects/storage/) (swift): Create petabytes of secure, reliable storage using standard hardware
- OpenStack [Image Service](http://openstack.org/projects/image-service/) (glance): Catalog and manage massive libraries of server images

## Project Goal

To build small, production ready (or near production ready) OpenStack compute and storage clusters using low cost, off-the-shelf hardware. Initially the project will have only one availability zone, but should be designed with future expansion in mind.

## Members

This project currently involves the following members:

- [Andrew LeCody](https://dallasmakerspace.org/wiki/User:Aceat64)
- Bryan Martin
- [Dwight S](https://dallasmakerspace.org/wiki/User:Denzuko)

## Design

The design is currently in a state of flux, please contact Andrew or Bryan for more info. The general idea is to fit 2 to 4 small (micro ATX or mini ITX) systems in 2u cases. For networking we will primarily use gigabit ethernet due to cost, however some parts of the infrastructure may use bonded GigE NICs. Our currently philosophy on redundancy is to protect objects stored in swift at all costs, as it will be used for static data and VM backups/images. While live migration and automatic failover of VMs between compute-nodes would be ideal, our requirements are that a given VM can be restored from a backup stored on the swift cluster in the event of a compute-node or compute-cluster failure.

## Resources

- [OpenStack Documentation](http://docs.openstack.org/)
- [StackOps Distro Documentation](http://docs.stackops.org/display/documentation/Home)
- <http://blog.stackops.com/2011/06/13/understanding-stackops-openstack-nova-networking-configuration/>
- <http://docs.stackops.org/display/documentation/Global+Network+Requirements>
