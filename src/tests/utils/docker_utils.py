import time

from docker import from_env
from docker.errors import NotFound


def is_container_ready(container):
    print("Checking if container is ready...")
    container.reload()
    return container.status == "running"


def wait_for_stable_status(container, stable_duration=3, interval=1):
    print("Waiting for stable status...")
    start_time = time.time()
    stable_count = 0
    while time.time() - start_time < stable_duration:
        if is_container_ready(container):
            stable_count += 1
        else:
            stable_count = 0
        if stable_count >= stable_duration / interval:
            return True
        time.sleep(interval)
    return False


# I needed to add myself to the docker group to run this script
# sudo gpasswd -a <system_user> docker
# sudo su <system_user>
def start_database_container():
    client = from_env()
    container_name = "test-db"
    try:
        existing_container = client.containers.get(container_name)
        print(f"Container {container_name} already exists, stopping and removing...")
        existing_container.stop()
        existing_container.remove()
        print(f"Container {container_name} stopped and removed.")
    except NotFound:
        print(f"Container {container_name} not found, creating...")
        # TODO: Switch to env variables
        container_config = {
            "name": container_name,
            "image": "postgres:16.4-alpine3.20",
            "detach": False,
            "ports": {"5432": "5434"},
            "environment": {
                "POSTGRES_USER": "postgres",
                "POSTGRES_PASSWORD": "password",
            },
        }
        print("---------")
        container = client.containers.run(
            name=container_config["name"],
            image=container_config["image"],
            environment=container_config["environment"],
            detach=True,
            ports=container_config["ports"],
        )
        print("---------")
        while not is_container_ready(container):
            print(f"Waiting for container {container_name} to be ready...")
            time.sleep(1)

        if not wait_for_stable_status(container):
            raise RuntimeError(f"Container {container_name} did not stabilize in time.")
        return container
