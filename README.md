# router_upgrade_single_controller

This is a python-based script that automatically upgrades a router having a single controller card

## How it works
1. Logs in to the router by creating an SSH channel
2. Fetches the router platform type
3. Checks for the presence of the new software file locally based on the route platform type
4. Fetches the active and inactive bank details from the router that contain the software file
5. Deletes the software file from the inactive bank
6. Transfers th new software file from external server to the inactive bank of the router
7. Verifies that file transfer has completed successfully and that the router recognizes the new software in the inactive bank
8. Performs pre-upgrade test from the router CLI
9. If the pre-upgrade test succeeds, proceeds with the new software activation
