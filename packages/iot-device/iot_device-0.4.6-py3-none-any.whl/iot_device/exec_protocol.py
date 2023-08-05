from .eval import Output, OutputHelper, RemoteError
from .eval_rsync import EvalRsync
import os, struct, time


EOT = b'\x04'

class ExecProtocol(EvalRsync):

    def __init__(self, device):
        super().__init__(device)

    # implement abstract Exec
    def exec(self, code, output:Output=None):
        return self._remote_eval("exec", code, output)

    def softreset(self):
        # programmatic reset
        self.exec(_softreset)

    def abort(self):
        # abort program execution - now sure how to do this?
        # perhaps disconnecting?
        pass

    def _remote_eval(self, instruction, code, output):
        if not output: output = OutputHelper()
        self.device.write(f"{instruction}\x04{len(code)}\n".encode())
        self.device.write(code.encode())
        self._read_response(output)
        if isinstance(output, OutputHelper):
            if len(output.err_):
                raise RemoteError(output.err_.decode())
            return output.ans_

    def _read_response(self, output):
        # process response, format "OK _answer_ EOT _error_message_ EOT>"
        self._check_ok()
        while True:
            ans = self.device.read().split(EOT)
            if len(ans[0]): output.ans(ans[0])
            if len(ans) > 1:      # 1st EOT
                if len(ans[1]): output.err(ans[1])
                if len(ans) > 2:  # 2nd EOT
                    return
                break             # look for 2nd EOT below
        # read error message, if any
        while True:
            ans = self.device.read().split(EOT)
            if len(ans[0]): output.err(ans[0])
            if len(ans) > 1:      # 2nd EOT
                break

    # override ExecFileOps
    def fget(self, src, dst, chunk_size=1024):
        # client:  fget EOT filename \n
        # server:  OK or error message \n
        #          file size (bytes), as 4 byte int (network order)
        #          send file content (size bytes)
        self.device.write(f"fget\x04{src}\n".encode())
        size = struct.unpack('!I', self.device.read(4))[0]
        with open(dst, 'wb') as f:
            while size > 0:
                data = self.device.read(min(chunk_size, size))
                f.write(data)
                size -= len(data)

    # override ExecFileOps
    def fput(self, src, dst, chunk_size=1024):
        # client:  fput EOT filename EOT size \n
        # server:  OK or error message \n
        # client:  send file content
        # server:  OK or error message \n
        self.disable_write_protection()
        sz = os.path.getsize(src)
        self.device.write(f"fput\x04{dst}\x04{sz}\n".encode())
        with open(src, 'rb') as f:
            while True:
                data = f.read(chunk_size)
                if not data: break
                self.device.write(data)

    def _check_ok(self):
        for i in range(5):
            ok = self.device.read(2)
            if len(ok) > 0: break
            time.sleep(0.2)
        if ok != b'OK':
            msg = ok.decode() if len(ok) > 0 else "no response"
            raise RemoteError(msg)


_softreset = """\
try:
    import microcontroller
    microcontroller.reset()
except ImportError:
    import machine
    machine.reset()
"""
