
from dataclasses import dataclass
import time
from typing import List
from orthanc_tools import OrthancForwarder, ForwarderDestination, ForwarderMode, ChangeType

from orthanc_api_client import OrthancApiClient

@dataclass
class OrthancSourceConfig:
    source_url: str
    source_user: str
    source_pwd: str

def get_api_client(config: OrthancSourceConfig) -> OrthancApiClient:
    return OrthancApiClient(config.source_url, user=config.source_user, pwd=config.source_pwd)

SOURCE_CONFIGS = [
    OrthancSourceConfig(
        source_url='http://localhost:8051',
        source_user='orthanc',
        source_pwd='orthanc'
    ),
    OrthancSourceConfig(
        source_url='http://localhost:8052',
        source_user='orthanc',
        source_pwd='orthanc'
    )
]

DESTINATION_CONFIG = ForwarderDestination(
    destination='cloud_orthanc',
    forwarder_mode=ForwarderMode.DICOM_WEB
)

THREAD_COUNT = 4
POLLING_INTERVAL_SECS = 2

def main():
    """
    Creates and runs OrthancForwarder instances for each source Orthanc instance.
    """
    forwarders: List[OrthancForwarder] = []
    
    for source_config in SOURCE_CONFIGS:
        api_client = get_api_client(source_config)
        forwarder = OrthancForwarder(
            api_client,
            destinations=[DESTINATION_CONFIG],
            trigger=ChangeType.STABLE_STUDY,
            worker_threads_count=THREAD_COUNT
        )
        forwarders.append(forwarder)

    # wait for the source Orthanc instances to be up 
    # (this is optional: the forwarder will retry in case of errors)
    for forwarder in forwarders:
        forwarder.wait_orthanc_started()

    while True:
        for forwarder in forwarders:
            forwarder.handle_all_content()
        time.sleep(POLLING_INTERVAL_SECS)

if __name__ == '__main__':
    main()
