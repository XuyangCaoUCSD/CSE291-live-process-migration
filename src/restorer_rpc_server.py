import subprocess
import rpyc

class DumpeeService(rpyc.Service):
    def on_connect(self, conn):
        pass

    def on_disconnect(self, conn):
        pass

    def exposed_apply_checkpoint_patch_on_m2(self):
        p = subprocess.call(["./jptch", "spirity.binary", "binary_diff", "new.binary"], shell=False)
        p = subprocess.call(["./jptch", "spirity.header", "header_diff", "new.header"], shell=False)
        p = subprocess.call(["mv", "new.binary", "spirity.binary"], shell=False)
        p = subprocess.call(["mv", "new.header", "spirity.header"], shell=False)
        print("patch applied")

    def exposed_inject_on_m2(self):
        dumpee_pid = subprocess.check_output(["pidof","./napp"]).decode("utf-8").strip("\n")
        p = subprocess.call(["./inject", dumpee_pid], shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        print("done injection")

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    print("start dumpee rpc server...")
    ThreadedServer(DumpeeService, port=5000).start()