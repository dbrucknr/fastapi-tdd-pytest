from os import path

from aiodocker import Docker
from aiodocker.containers import DockerContainer

# https://forums.docker.com/t/containers-not-showing-in-docker-desktop/135015


async def start_testing_database(docker: Docker) -> DockerContainer:
    scripts_dir = path.abspath("./scripts")
    container: DockerContainer = await docker.containers.create_or_replace(
        name="test-db",
        config={
            "Image": "postgres:16.4-alpine3.20",
            "Env": ["POSTGRES_USER=postgres", "POSTGRES_PASSWORD=password"],
            "ExposedPorts": {"5432/tcp": {}},
            "HostConfig": {"PortBindings": {"5432/tcp": [{"HostPort": "5434"}]}},
            # "Volumes": [
            #     f"{scripts_dir}:/docker-entrypoint-initdb.d",
            # ],
            # "NetworkMode": "fastapi-tdd-pytest_dev-network",
        },
    )
    await container.start()
    logs = await container.log(stdout=True)
    print("".join(logs))
    # await container.delete(force=True)
    return container


if __name__ == "__main__":
    import asyncio

    async def main():
        # docker = Docker()
        # await start_testing_database(docker)
        # await docker.close()
        print("======================================")
        async with Docker() as docker:
            container = await docker.containers.create_or_replace(
                name="test-db",
                config={
                    "Cmd": ["/bin/ash", "-c", 'echo "hello world"'],
                    "Image": "postgres:16.4-alpine3.20",
                },
            )
            await container.start()
            logs = await container.log(stdout=True)
            print(logs)

            # container = await start_testing_database(docker)
            # print(f"Container {container} started.")

    asyncio.run(main())
