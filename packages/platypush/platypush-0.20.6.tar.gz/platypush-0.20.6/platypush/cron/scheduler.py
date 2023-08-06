import datetime
import enum
import logging
import threading

import croniter
from dateutil.tz import gettz

from platypush.procedure import Procedure
from platypush.utils import is_functional_cron

logger = logging.getLogger('platypush:cron')


class CronjobState(enum.IntEnum):
    IDLE = 0
    WAIT = 1
    RUNNING = 2
    DONE = 3
    ERROR = 4


class Cronjob(threading.Thread):
    def __init__(self, name, cron_expression, actions):
        super().__init__()
        self.cron_expression = cron_expression
        self.name = name
        self.state = CronjobState.IDLE
        self._should_stop = threading.Event()

        if isinstance(actions, dict) or isinstance(actions, list):
            self.actions = Procedure.build(name=name + '__Cron', _async=False, requests=actions)
        else:
            self.actions = actions

    def run(self):
        self.state = CronjobState.WAIT
        self.wait()
        if self.should_stop():
            return

        self.state = CronjobState.RUNNING

        try:
            logger.info('Running cronjob {}'.format(self.name))
            context = {}

            if isinstance(self.actions, Procedure):
                response = self.actions.execute(_async=False, **context)
            else:
                response = self.actions(**context)

            logger.info('Response from cronjob {}: {}'.format(self.name, response))
            self.state = CronjobState.DONE
        except Exception as e:
            logger.exception(e)
            self.state = CronjobState.ERROR

    def wait(self):
        now = datetime.datetime.now().replace(tzinfo=gettz())
        cron = croniter.croniter(self.cron_expression, now)
        next_run = cron.get_next()
        self._should_stop.wait(next_run - now.timestamp())

    def stop(self):
        self._should_stop.set()

    def should_stop(self):
        return self._should_stop.is_set()


class CronScheduler(threading.Thread):
    def __init__(self, jobs):
        super().__init__()
        self.jobs_config = jobs
        self._jobs = {}
        self._should_stop = threading.Event()
        logger.info('Cron scheduler initialized with {} jobs'.
                    format(len(self.jobs_config.keys())))

    def _get_job(self, name, config):
        job = self._jobs.get(name)
        if job and job.state not in [CronjobState.DONE, CronjobState.ERROR]:
            return job

        if isinstance(config, dict):
            self._jobs[name] = Cronjob(name=name, cron_expression=config['cron_expression'],
                                       actions=config['actions'])
        elif is_functional_cron(config):
            self._jobs[name] = Cronjob(name=name, cron_expression=config.cron_expression,
                                       actions=config)
        else:
            raise AssertionError('Expected type dict or function for cron {}, got {}'.format(
                name, type(config)))

        return self._jobs[name]

    def stop(self):
        for job in self._jobs.values():
            job.stop()
        self._should_stop.set()

    def should_stop(self):
        return self._should_stop.is_set()

    def run(self):
        logger.info('Running cron scheduler')

        while not self.should_stop():
            for (job_name, job_config) in self.jobs_config.items():
                job = self._get_job(name=job_name, config=job_config)
                if job.state == CronjobState.IDLE:
                    job.start()

            self._should_stop.wait(timeout=0.5)

        logger.info('Terminating cron scheduler')


# vim:sw=4:ts=4:et:
