# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rearq', 'rearq.api']

package_data = \
{'': ['*']}

install_requires = \
['aioredis', 'click', 'crontab', 'fastapi', 'pydantic', 'uvicorn']

entry_points = \
{'console_scripts': ['rearq = rearq.cli:main']}

setup_kwargs = {
    'name': 'rearq',
    'version': '0.2.0',
    'description': 'Rewrite arq and make improvement.',
    'long_description': '# Rearq\n\n![pypi](https://img.shields.io/pypi/v/rearq.svg?style=flat)\n\n## Introduction\n\nRearq is a distributed task queue with asyncio and redis, which rewrite from [arq](https://github.com/samuelcolvin/arq)\nand make improvement.\n\n## Install\n\nJust install from pypi:\n\n```shell\n> pip install rearq\n```\n\n## Quick Start\n\n### Task Definition\n\n```python\n# main.py\nrearq = ReArq()\n\n\n@rearq.on_shutdown\nasync def on_shutdown():\n    # you can do some clean work here like close db and so on...\n    print("shutdown")\n\n\n@rearq.on_startup\nasync def on_startup():\n    # you should do some initialization work here, such tortoise-orm init and so on...\n    print("startup")\n\n\n@rearq.task(queue="myqueue")\nasync def add(self, a, b):\n    return a + b\n\n\n@rearq.task(cron="*/5 * * * * * *")  # run task per 5 seconds\nasync def timer(self):\n    return "timer"\n```\n\n### Run rearq worker\n\n```shell\n> rearq main:rearq worker -q myqueue\n```\n\n```log\n2020-06-04 15:37:02 - rearq.worker:92 - INFO - Start worker success with queue: myqueue\n2020-06-04 15:37:02 - rearq.worker:84 - INFO - redis_version=6.0.1 mem_usage=1.47M clients_connected=25 db_keys=5\n```\n\n### Run rearq timing worker\n\nIf you have timeing task, run another command also:\n\n```shell\n> rearq main:rearq worker -t\n```\n\n```log\n2020-06-04 15:37:44 - rearq.worker:346 - INFO - Start timer worker success with queue: myqueue\n2020-06-04 15:37:44 - rearq.worker:84 - INFO - redis_version=6.0.1 mem_usage=1.47M clients_connected=25 db_keys=5\n```\n\n### Integration in FastAPI\n\n```python\napp = FastAPI()\n\n\n@app.on_event("startup")\nasync def startup() -> None:\n    await rearq.init()\n\n\n@app.on_event("shutdown")\nasync def shutdown() -> None:\n    await rearq.close()\n\n\n# then run task in view\n@app.get("/test")\nasync def test():\n    job = await add.delay(args=(1, 2))\n    return job.info()\n```\n\n## Rest API\n\nThere are several apis to control rearq.\n\n### Start server\n\n```shell\n> rearq main:rearq server\nUsage: rearq server [OPTIONS]\n\n  Start rest api server.\n\nOptions:\n  --host TEXT         Listen host.  [default: 0.0.0.0]\n  -p, --port INTEGER  Listen port.  [default: 8080]\n  -h, --help          Show this message and exit..\n```\n\n### API docs\n\nAfter server run, you can visit [https://127.0.0.1:8080/docs](https://127.0.0.1:8080/docs) to get all apis.\n\n### GET `/job`\n\nGet job information.\n\n### POST `/job`\n\nAdd a job for a task.\n\n### DELETE `/job`\n\nCancel a delay task.\n\n### GET `/job/result`\n\nGet job result.\n\n## Documentation\n\n> Writing...\n\n## ThanksTo\n\n- [arq](https://github.com/samuelcolvin/arq), Fast job queuing and RPC in python with asyncio and redis.\n\n## License\n\nThis project is licensed under the [MIT](https://github.com/long2ice/rearq/blob/master/LICENSE) License.\n',
    'author': 'long2ice',
    'author_email': 'long2ice@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/long2ice/rearq.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
