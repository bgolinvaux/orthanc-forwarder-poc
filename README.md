
# What this does 

This example demonstrates how to use the `OrthancForwarder` class from the `python-orthanc-tools` package (from Orthanc Team) to forward all the DICOM resources from two Orthanc servers to a third destination server, through the DICOMweb protocol.

**WARNING**: this forwarder will _move_ the DICOM resources that will thus be removed from the source Orthanc servers. This is a proof of concept and should be used with caution.

# How to use this proof of concept

## Prerequisites

I will assume a Windows environments. Steps for macOS or Linux are similar.

The following steps are to be done once.

First, copy this folder to your local machine.

You'll first need to install the uv Python management tool

Open a PowerShell terminal and execute:

```
cd C:\path\to\forwarder\folder
```

```
powershell -c "irm https://astral.sh/uv/install.ps1 | more"
```

Then, close the terminal, open a new one and navigate to the folder where you copied the files with:

```
cd C:\path\to\forwarder\folder
```

Then, setup the runtime environment

```
uv venv --python 3.11
uv pip install orthanc-tools
```

## Configure the Orthanc servers

- make sure that the IP and user/password pairs are known for both source Orthanc servers

add an entry in the `OrthancPeers` configuration for `cloud_orthanc`:

```json
...
    "DicomWeb": {
        "Servers": {
            "cloud_orthanc": [
                "http://my-orthanc-server:1234/",
                "orthanc",
                "orthanc"
            ]
        }
    },
...
```

### Important note

The `http` protocol is not secure and `https` is recommended. Http should only be used if you have a truly safe network connection to the cloud Orthanc server, for instance through a VPN. Configuring network access is outside the scope of this tutorial but, depending on how your cloud Orthanc is running, VPN might not be possible and you might need to run a reverse proxy to serve the cloud Orthanc on `https`.

## Configure the forwarder

Edit the `forwarder-main.py` file and modify the IP addresses and credentials to match your Orthanc servers.

## Run the forwarder

Open a PowerShell terminal and execute:

```
uv run --no-project forwarder-main.py
```

## Test the forwarder

- Add a new DICOM study/series/instance to the source Orthanc server
- Check if it's transferred to the remote one

Repeat for the other source server.


# Notes

Written by Benjamin Golinvaux (benjamin@golinvaux.com) on 2024-12-11.
