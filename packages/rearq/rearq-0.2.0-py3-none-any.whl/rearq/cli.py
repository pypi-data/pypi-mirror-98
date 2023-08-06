import asyncio
import importlib
import sys
from functools import wraps

import click
import uvicorn
from click import BadArgumentUsage, Context

from rearq.api.app import app
from rearq.log import init_logging
from rearq.version import VERSION
from rearq.worker import TimerWorker, Worker


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(f(*args, **kwargs))

    return wrapper


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(VERSION, "-v", "--version")
@click.option("--verbose", default=False, is_flag=True, help="Enable verbose output.")
@click.argument("rearq", required=True)
@click.pass_context
@coro
async def cli(ctx: Context, rearq: str, verbose):
    init_logging(verbose)
    splits = rearq.split(":")
    rearq_path = splits[0]
    rearq = splits[1]
    try:
        module = importlib.import_module(rearq_path)
        rearq = getattr(module, rearq, None)

        ctx.ensure_object(dict)
        ctx.obj["rearq"] = rearq
        ctx.obj["verbose"] = verbose

    except (ModuleNotFoundError, AttributeError) as e:
        raise BadArgumentUsage(ctx=ctx, message=f"Init rearq error, {e}.")


@cli.command(help="Start rearq worker.")
@click.option("-q", "--queue", required=False, help="Queue to consume.")
@click.option("-t", "--timer", default=False, is_flag=True, help="Start a timer worker.")
@click.pass_context
@coro
async def worker(ctx: Context, queue: str, timer: bool):
    rearq = ctx.obj["rearq"]
    await rearq.init()
    if timer:
        w = TimerWorker(rearq, queue=queue, )
    else:
        w = Worker(rearq, queue=queue)
    await w.async_run()


@cli.command(help="Start rest api server.")
@click.option("--host", default="0.0.0.0", show_default=True, help="Listen host.")
@click.option("-p", "--port", default=8080, show_default=True, help="Listen port.")
@click.pass_context
def server(ctx: Context, host: str, port: int):
    rearq = ctx.obj["rearq"]
    app.rearq = rearq

    verbose = ctx.obj["verbose"]

    @app.on_event("startup")
    async def startup():
        await rearq.init()

    @app.on_event("shutdown")
    async def shutdown():
        await rearq.close()

    uvicorn.run(app=app, host=host, port=port, debug=verbose)


def main():
    sys.path.insert(0, ".")
    cli()


if __name__ == '__main__':
    main()
