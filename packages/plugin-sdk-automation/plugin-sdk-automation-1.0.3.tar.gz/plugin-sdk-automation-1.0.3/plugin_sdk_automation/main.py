import logging
import docker
import time

from pathlib import Path


def main():
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    st = logging.StreamHandler()
    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)d - %(message)s")
    st.setFormatter(fmt)
    log.addHandler(st)

    client = docker.from_env()

    log.info(f"Pulling the image")
    for log_line in client.api.pull("dlopes7/plugin_sdk", stream=True):
        log.info(log_line.decode().rstrip())

    # Check if we are where plugin.json is located
    build_dir = Path().absolute()
    if not Path("plugin.json") in list(Path().iterdir()):
        raise Exception("The command must be run from where plugin.json is located")

    # Convert path to windows/kitematic format
    # C:\Users\user > /c/Users/user
    build_dir = f"{build_dir.as_posix()}"
    if ":" in build_dir:
        build_dir = build_dir.replace(":", "")
        if not build_dir.startswith("/"):
            build_dir = f"/{build_dir}"

    volumes = {build_dir: {'bind': '/data', 'mode': 'rw'}}
    log.info(f"Will mount volumes: {volumes}")
    log.info(f"Starting docker container")

    start_time = time.time()

    container = client.containers.run("dlopes7/plugin_sdk", volumes=volumes, remove=True, detach=True)
    for log_line in container.logs(stdout=True, stderr=True, stream=True, follow=True):
        log.info(log_line.decode().rstrip())

    log.info(f"Docker container build finished after {time.time() - start_time:.2f}s")


if __name__ == '__main__':
    main()
