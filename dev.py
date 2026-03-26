import subprocess
import signal
import time

dst = "build"

print("[dev] starting HTTP server and generator in watch mode")
serverp = subprocess.Popen(["python", "-m", "http.server", "-d", dst, "8000"])
generatorp = subprocess.Popen(["python", "./generator/main.py", "--watch"])

def shutdown(sig, frame):
    print("[dev] received signal, shutting down")
    generatorp.terminate()
    serverp.terminate()
    generatorp.wait()
    serverp.wait()
    raise SystemExit(0)

signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)

while serverp.poll() is None and generatorp.poll() is None:
    time.sleep(0.5)

print("[dev] terminating server and generator")
serverp.terminate()
generatorp.terminate()
serverp.wait()
generatorp.wait()

print("[dev] all terminated, bye!")