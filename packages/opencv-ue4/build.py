#!/usr/bin/env python3
import subprocess

# Query ue4cli for the UE4 version string
proc = subprocess.Popen(["ue4", "version", "short"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
(stdout, stderr) = proc.communicate(input)
if proc.returncode != 0:
    raise Exception("failed to retrieve UE4 version string")

# Build the Conan package, using the Engine version as the channel name
subprocess.call(["conan", "create", ".", "adamrehn/{}".format(stdout.strip()), "--profile", "ue4"])
