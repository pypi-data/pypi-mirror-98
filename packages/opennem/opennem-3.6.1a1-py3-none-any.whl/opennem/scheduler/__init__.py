# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
# pylint: disable=no-member
import platform

from huey import PriorityRedisHuey, crontab

from opennem.api.export.map import PriorityType
from opennem.api.export.tasks import (
    export_all_daily,
    export_all_monthly,
    export_electricitymap,
    export_energy,
    export_flows,
    export_metadata,
    export_power,
)
from opennem.exporter.geojson import export_facility_geojson
from opennem.monitors.aemo_intervals import aemo_wem_live_interval
from opennem.monitors.emissions import alert_missing_emission_factors
from opennem.monitors.opennem import check_opennem_interval_delays
from opennem.monitors.opennem_metadata import check_metadata_status
from opennem.notifications.slack import slack_message
from opennem.settings import settings

# Py 3.8 on MacOS changed the default multiprocessing model
if platform.system() == "Darwin":
    import multiprocessing

    try:
        multiprocessing.set_start_method("fork")
    except RuntimeError:
        # sometimes it has already been set by
        # other libs
        pass

redis_host = None

if settings.cache_url:
    redis_host = settings.cache_url.host

huey = PriorityRedisHuey("opennem.scheduler", host=redis_host)
# export tasks


@huey.periodic_task(crontab(minute="*/3"), priority=90)
@huey.lock_task("schedule_live_tasks")
def schedule_live_tasks() -> None:
    if settings.workers_run:
        export_power(priority=PriorityType.live)
        export_flows()


@huey.periodic_task(crontab(minute="*/15"), priority=90)
@huey.lock_task("schedule_custom_tasks")
def schedule_custom_tasks() -> None:
    if settings.workers_run:
        export_electricitymap()


@huey.periodic_task(crontab(hour="*/12"))
@huey.lock_task("schedule_power_weeklies")
def schedule_power_weeklies() -> None:
    """
    Run weekly power outputs
    """
    if settings.workers_run:
        export_power(priority=PriorityType.history, latest=True)


@huey.periodic_task(crontab(minute="15", hour="12"))
@huey.lock_task("schedule_power_weeklies_archive")
def schedule_power_weeklies_archive() -> None:
    """
    Run weekly power outputs entire archive
    """
    # export_power(priority=PriorityType.history)
    pass


@huey.periodic_task(crontab(hour="/12"), priority=50)
@huey.lock_task("schedule_export_all_daily")
def schedule_export_all_daily() -> None:
    if settings.workers_run:
        export_all_daily()
        slack_message("Finished running export_all_daily")


@huey.periodic_task(crontab(hour="/12"), priority=50)
@huey.lock_task("schedule_export_all_monthly")
def schedule_export_all_monthly() -> None:
    if settings.workers_run:
        export_all_monthly()
        slack_message("Finished running export_all_monthly")


@huey.periodic_task(crontab(hour="*/1", minute="45"), priority=50)
@huey.lock_task("schedule_hourly_tasks")
def schedule_hourly_tasks() -> None:
    if settings.workers_run:
        export_energy(priority=PriorityType.daily, latest=True)


@huey.periodic_task(crontab(hour="*/2", minute="15"))
@huey.lock_task("schedule_daily_tasks")
def schedule_daily_tasks() -> None:
    if settings.workers_run:
        export_energy(priority=PriorityType.daily)
        slack_message("Finished running energy dailies")


@huey.periodic_task(crontab(hour="*/2"), priority=30)
@huey.lock_task("schedule_energy_monthlies")
def schedule_energy_monthlies() -> None:
    if settings.workers_run:
        export_energy(priority=PriorityType.monthly)
        slack_message("Finished running energy_monthlies")


# geojson maps
@huey.periodic_task(crontab(minute="*/30"), priority=50)
@huey.lock_task("schedule_export_geojson")
def schedule_export_geojson() -> None:
    if settings.workers_run:
        export_facility_geojson()


# metadata
@huey.periodic_task(crontab(minute="*/30"), priority=30)
@huey.lock_task("schedule_export_metadata")
def schedule_export_metadata() -> None:
    if settings.workers_run:
        export_metadata()


# monitoring tasks
@huey.periodic_task(crontab(minute="*/15"), priority=80)
@huey.lock_task("monitor_opennem_intervals")
def monitor_opennem_intervals() -> None:
    for network_code in ["NEM", "WEM"]:
        check_opennem_interval_delays(network_code)


@huey.periodic_task(crontab(minute="*/15"), priority=50)
@huey.lock_task("monitor_wem_interval")
def monitor_wem_interval() -> None:
    aemo_wem_live_interval()


@huey.periodic_task(crontab(hour="*/12"), priority=10)
@huey.lock_task("monitor_metadata_status")
def monitor_metadata_status() -> None:
    if settings.workers_run:
        check_metadata_status()


@huey.periodic_task(crontab(hour="/12"), priority=10)
@huey.lock_task("monitor_emission_factors")
def monitor_emission_factors() -> None:
    if settings.workers_run:
        alert_missing_emission_factors()
