
# What this does 

This example demonstrates how to use the `OrthancForwarder` class from the `python-orthanc-tools` package (from [Orthanc Team](https://github.com/orthanc-team)) to forward all the DICOM resources from two Orthanc servers to a third destination server, through the DICOMweb protocol.

**WARNING**: this forwarder will _move_ the DICOM resources that will thus be removed from the source Orthanc servers. This is a proof of concept and should be used with caution.

# How to use this proof of concept

## Prerequisites

I will assume a Windows environment. Steps for macOS or Linux are very similar, except for the installation of the `uv` tool. See [the installation instructions](https://docs.astral.sh/uv/getting-started/installation/) for more information.

The following steps are to be done once.

First, clone this folder to your local machine: if you have git, you can use `git clone https://github.com/bgolinvaux/orthanc-forwarder-poc.git` or you can also use the "Download ZIP" button that is in the top right menu that appears when clicking on "<> Code".

You will also need to install the uv Python management tool. You can use other tools if you wish, but `uv` is simple and fast, and does not require Python to be installed first.

Open a PowerShell terminal (it does *not* need to be an elevated/administrator one) and execute:

```
powershell -c "irm https://astral.sh/uv/install.ps1 | more"
```

Then, close the terminal, open a new one (so that `uv` becomes accessible in the `PATH`) and navigate to the folder where you copied the files with:

```
cd C:\path\to\orthanc-forwarder-poc
```

Then, setup the runtime environment

```
uv venv --python 3.11
uv pip install orthanc-tools
```

## Configure the Orthanc servers

Add an entry in the source (local) Orthanc servers so that the `DicomWeb` configuration contains an entry for the remote cloud Orthanc (`cloud_orthanc`):

```json
    "DicomWeb": {
        "Servers": {
            "cloud_orthanc": [
                "http://my-orthanc-server:1234/",
                "orthanc",
                "orthanc"
            ]
        }
    },
```

Make sure to enable the `DicomWeb` server in the cloud Orthanc with:

```
    "DicomWeb" : {
        "Enable" : true
    },
```

### Notes

1) The `http` protocol is not secure and `https` is recommended. Http should only be used if you have a truly safe network connection to the cloud Orthanc server, for instance through a VPN. Configuring network access is outside the scope of this tutorial but, depending on how your cloud Orthanc is running, VPN might not be possible and you might need to perform some additional configuration to serve the cloud Orthanc on `https`. Here are some links that can help:
    - The Orthanc book explains [how Orthanc itself can be configured to serve https](https://orthanc.uclouvain.be/book/faq/https.html)
    - You can [use Nginx to serve https](https://docs.nginx.com/nginx/admin-guide/security-controls/securing-http-traffic-upstream/)
    - If you are using a cloud provider, they might have some documentation on how to serve https. 
        - [Redirect HTTP to HTTPS with Azure](https://learn.microsoft.com/en-us/azure/application-gateway/redirect-http-to-https-portal)
        - [FAQ for AWS API gateway](https://aws.amazon.com/api-gateway/faqs/)

1) I haven't tested with a cloud remote server, only a local one, and this is why all the pre-existing configuration is for local servers. As long as the network configuration is correct, it should work with any source and destination Orthanc instances.

2) You might need or want to perform more advanced DICOMweb configuration. Please visit [the Orthanc Book](https://orthanc.uclouvain.be/book/index.html) and, in particular, [the DICOMweb plugin page](https://orthanc.uclouvain.be/book/plugins/dicomweb.html) for more information.




## Configure the forwarder

Edit the `forwarder-main.py` file and modify the IP addresses and credentials to match your Orthanc servers.

## Run the forwarder

Open a PowerShell terminal and execute:

```
uv run --no-project forwarder-main.py
```

## Test the forwarder

- Add a new DICOM study/series/instance to the source Orthanc server
- Check if it is correct transferred to the remote one.

Repeat for the other source server.

## Caveats and improvements

- Error handling should at least be tested.
    - It would be nice to check what happens when the Orthanc instances are not available, because they are down or because the network is down.
- Some logging would be useful, perhaps at the study level. Some options are perhaps available through the `OrthancForwarder` class.


# Notes

Written by Benjamin Golinvaux (benjamin@golinvaux.com) on 2024-12-11.
