import subprocess
import time

def execute(command):
    '''
    Exectutes the given command as a subprocess, waits for it finish and then returns (retCode, stdout, stderr) as 3-tuple
    :param command: array containing shell command to be run.
    :return: (retCode, stdout, stderr) as 3-tuple
    '''
    # Open a subprocess with stdout and stderr redirected to pipes. This is useful for recording output of process.
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Wait until process terminates
    while p.poll() is None:
        time.sleep(0.5) # sleep to give CPU some breathing space.
    # Read stdout and stderr
    stdout, stderr = p.communicate()
    # return returncode, stdout, stderr as a 3-tuple.
    return (p.returncode, stdout, stderr)
