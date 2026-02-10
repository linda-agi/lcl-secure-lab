#!/bin/bash
# LCL Secure Lab - Isolated Execution Wrapper
# Uses nsjail to create a hardened sandbox for running untrusted AI scripts/models.

set -e

COMMAND=$@

if [ -z "$COMMAND" ]; then
    echo "Usage: $0 <command>"
    exit 1
fi

# NSJail Configuration
# - Mo: Local directory mapping
# - Mo: Read-only system paths
# - N: No network
# - P: Max processes
# - T: Max execution time
# - H: Hostname

echo "[LSL] Launching isolated process: $COMMAND"

# Note: Requires nsjail to be installed and executable by the user.
# Using sudo as a placeholder if system-level namespaces are restricted.
sudo nsjail -Mo \
    --chroot / \
    --rw \
    --user 99999 --group 99999 \
    --hostname lcl-secure-lab \
    --cwd $(pwd) \
    --time_limit 300 \
    --max_cpus 1 \
    --rlimit_as 2048 \
    --disable_proc \
    --proc_rw \
    --proc_path /proc \
    --bindmount_ro /lib:/lib \
    --bindmount_ro /lib64:/lib64 \
    --bindmount_ro /usr:/usr \
    --bindmount_ro /bin:/bin \
    --bindmount_ro /sbin:/sbin \
    --bindmount /tmp \
    --env PATH=$PATH \
    --disable_network \
    --clone_newnet \
    --clone_newuser \
    --clone_newns \
    --clone_newpid \
    --clone_newipc \
    --clone_newuts \
    -- $COMMAND

echo "[LSL] Execution finished."
