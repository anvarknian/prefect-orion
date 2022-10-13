import os
import uuid
from datetime import datetime

from prefect.deployments import Deployment
from prefect.filesystems import RemoteFileSystem
from prefect.infrastructure import DockerContainer

from test_flow import my_docker_flow

flow_identifier = datetime.today().strftime("%Y%m%d%H%M%S-") + str(uuid.uuid4())

bucket_name = os.environ.get("MINIO_PREFECT_FLOWS_BUCKET_NAME")
artifacts_bucket_name = os.environ.get("MINIO_PREFECT_ARTIFACTS_BUCKET_NAME")
minio_endpoint = os.environ.get("MINIO_ENDPOINT")
minio_use_ssl = os.environ.get("MINIO_USE_SSL") == "true"
minio_scheme = "https" if minio_use_ssl else "http"
minio_access_key = os.environ.get("MINIO_ACCESS_KEY")
minio_secret_key = os.environ.get("MINIO_SECRET_KEY")
endpoint_url=f"{minio_scheme}://{minio_endpoint}"

block_storage = RemoteFileSystem(
    basepath=f"s3://{bucket_name}/{flow_identifier}",
    key_type="hash",
    settings=dict(
        use_ssl=minio_use_ssl,
        key=minio_access_key,
        secret=minio_secret_key,
        client_kwargs=dict(endpoint_url=endpoint_url),
    ),
)
block_storage.save("s3-storage", overwrite=True)

deployment = Deployment.build_from_flow(
    name="docker-example",
    flow=my_docker_flow,
    storage=RemoteFileSystem.load('minio'),
    infrastructure=DockerContainer(
        image='prefect-orion:2.4.5',
        image_pull_policy='IF_NOT_PRESENT',
        networks=['prefect'],
        env={
            "USE_SSL": minio_use_ssl,
            "AWS_ACCESS_KEY_ID": minio_access_key,
            "AWS_SECRET_ACCESS_KEY": minio_secret_key,
            "ENDPOINT_URL": endpoint_url,
        }
    ),
)
deployment.apply()
