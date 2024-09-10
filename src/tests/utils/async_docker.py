from asyncio import sleep
from os import path

from aiodocker import Docker, DockerError
from aiodocker.containers import DockerContainer
from aiodocker.images import DockerImages


# https://forums.docker.com/t/containers-not-showing-in-docker-desktop/135015
async def wait_for_container_ready(container: DockerContainer, timeout: int = 60):
    """Wait for the container to be ready by checking its status."""
    elapsed_time = 0
    check_interval = 2  # Time in seconds between each status check

    while elapsed_time < timeout:
        # Fetch the container's current status
        container_info = await container.show()
        status = container_info["State"]["Status"]

        # Check if the container is running
        if status == "running":
            # Optionally, check if a health check is configured and passed
            health_status = (
                container_info["State"].get("Health", {}).get("Status", "healthy")
            )
            if health_status == "healthy":
                print(f"Container {container.id} is ready.")
                return True

        # If not running or healthy, wait for the next interval
        await sleep(check_interval)
        elapsed_time += check_interval

    raise TimeoutError(
        f"Container {container.id} did not become ready within {timeout} seconds."
    )


async def start_testing_database(docker: Docker) -> DockerContainer:
    """Start a PostgreSQL database container for testing."""
    try:
        scripts_dir = path.abspath("./scripts")
        images = DockerImages(docker=docker)
        await images.pull(from_image="postgres:16.4-alpine3.20")
        container: DockerContainer = await docker.containers.create_or_replace(
            name="test-db",
            config={
                "Image": "postgres:16.4-alpine3.20",
                "Env": [
                    "POSTGRES_USER=postgres",
                    "POSTGRES_PASSWORD=postgres",
                    "POSTGRES_DB=inventory",
                ],
                "ExposedPorts": {"5432/tcp": {}},
                "HostConfig": {
                    "PortBindings": {"5432/tcp": [{"HostPort": "5434"}]},
                    "Binds": [
                        f"{scripts_dir}:/docker-entrypoint-initdb.d"
                    ],  # Volume Binding
                    "NetworkMode": "fastapi-tdd-pytest_dev-network",  # Network Mode
                },
            },
        )
        return container
    except DockerError as e:
        print(f"Failed to start the database container: {e}")
