# [CSE291 Virtualization] Live Process Migration


### To achieve live process migration, we follow an iterative dumping pattern, along with the customizable checkpoint and restoration components.

This a course project about process migration. For more information, **please request the technical report**. 



The checkpoint and restoration utility are adopted from [David Wang](https://github.com/zq-david-wang/linux-tools/tree/main/drivers/mremap). Thank you. Also, we use his open-sourced mremap patch to the kernel, so now a process can reset the memory layout of another one. 

Basically, 

`app` contains the testing number recorder app, where we used for evaluation. 

To compile the app, `g++ napp.cpp -o napp`. We also provided a Dockerfile to containerize the app. We have successfully migrated the container version on the same machine (yet not M1 to M2).

In `src`, 

* `jdiff081` is a binary diff utility we use for iterative dumping for our live migration.
* `mremap_midware` is the very midware/device interface (using `ioctl` on it) to trigger the mremap command from one process to the other. Prerequisite: you need to apply the `kernel-mremap-pid-patch-6.0.0.diff` patch to kernel. Compile and load this kernel module.
* `extract.cpp` is the checkpoint component. `g++ extract.cpp -o extract`.
* `inject.cpp` is the restoration component. `g++ inject.cpp -o inject`.
* `jdff` and `jptch` are binary diff utility from `jdiff081` we will use for our live migration.
* `live_migration.py` contains our interfaces as well as the assembled program to do the live migrations. Run it on source machine, after you set up the restorer server (`restorer_rpc_server.py`) on the destination machine.
* `restorer_rpc_server.py` is the RPC server that provides remotely callable process restoration functuonalities.  
* `kernel-mremap-pid-patch-6.0.0.diff` is the very patch to apply the mremap upgrade to the kernel, so your system can have one process do mremap for the other process. (don't apply onto your work machine!)

Therefore, have everything compiled, apply the kernel patch (and recompile it), load the middleware, have the test app (or your own) running, and apply the live migration to see all the output!

`Evaluation` contains the raw output of our test.