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

    # People can run this from the path where plugin.json is located, or one path up
    # Check if we are where plugin.json is located, and use one directory up if that is the case
    build_dir = Path().absolute()
    if Path("plugin.json") in list(Path().iterdir()):
        build_dir = build_dir.parents[0]

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
