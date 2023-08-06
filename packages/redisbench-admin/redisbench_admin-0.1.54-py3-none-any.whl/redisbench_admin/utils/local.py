import logging
import os
import subprocess
import tempfile
import time
from shutil import copyfile

import redis


def checkDatasetLocalRequirements(benchmark_config, redis_tmp_dir, dirname="."):
    for k in benchmark_config["dbconfig"]:
        if "dataset" in k:
            dataset = k["dataset"]
    if dataset is not None:
        logging.info("Copying rdb {}/{} to {}/dump.rdb".format(dirname, dataset, redis_tmp_dir))
        copyfile("{}/{}".format(dirname, dataset), "{}/dump.rdb".format(redis_tmp_dir))


def waitForConn(conn, retries=20, command="PING", shouldBe=True):
    """Wait until a given Redis connection is ready"""
    result = False
    err1 = ""
    while retries > 0 and result is False:
        try:
            if conn.execute_command(command) == shouldBe:
                result = True
        except redis.exceptions.BusyLoadingError:
            time.sleep(0.1)  # give extra 100msec in case of RDB loading
        except redis.ConnectionError as err:
            err1 = str(err)
        except redis.ResponseError as err:
            err1 = str(err)
            if not err1.startswith("DENIED"):
                raise
        time.sleep(0.1)
        retries -= 1
        logging.debug("Waiting for Redis")
    return result


def spinUpLocalRedis(
        benchmark_config,
        port,
        local_module_file,
        dirname=".",
):
    # copy the rdb to DB machine
    dataset = None
    temporary_dir = tempfile.mkdtemp()
    logging.info(
        "Using local temporary dir to spin up Redis Instance. Path: {}".format(
            temporary_dir
        )
    )
    checkDatasetLocalRequirements(benchmark_config, temporary_dir, dirname)

    # start redis-server
    command = [
        "redis-server",
        "--save",
        '""',
        "--port",
        "{}".format(port),
        "--dir",
        temporary_dir,
        "--loadmodule",
        os.path.abspath(local_module_file),
    ]
    logging.info(
        "Running local redis-server with the following args: {}".format(
            " ".join(command)
        )
    )
    redis_process = subprocess.Popen(command)
    result = waitForConn(redis.StrictRedis())
    if result is True:
        logging.info("Redis available")
    return redis_process


def isProcessAlive(process):
    if not process:
        return False
    # Check if child process has terminated. Set and return returncode
    # attribute
    if process.poll() is None:
        return True
    return False


def getLocalRunFullFilename(
        start_time_str,
        github_branch,
        test_name,
):
    benchmark_output_filename = (
        "{start_time_str}-{github_branch}-{test_name}.json".format(
            start_time_str=start_time_str,
            github_branch=github_branch,
            test_name=test_name,
        )
    )
    return benchmark_output_filename
