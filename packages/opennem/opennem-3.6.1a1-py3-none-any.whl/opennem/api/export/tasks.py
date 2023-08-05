"""
Tasks file to expor JSON's to S3 or locally for the
opennem website

This is the most frequently accessed content that doesn't
require the API


"""

import logging
from datetime import datetime
from typing import List, Optional

from opennem.api.export.controllers import (
    demand_week,
    energy_fueltech_daily,
    energy_interconnector_emissions_region_daily,
    energy_interconnector_region_daily,
    gov_stats_cpi,
    power_flows_network_week,
    power_flows_region_week,
    power_week,
    weather_daily,
)
from opennem.api.export.map import PriorityType, StatExport, StatType, get_export_map
from opennem.api.export.utils import write_output
from opennem.api.stats.controllers import get_scada_range
from opennem.api.stats.schema import OpennemDataSet, ScadaDateRange
from opennem.api.time import human_to_interval, human_to_period
from opennem.core.network_region_bom_station_map import get_network_region_weather_station
from opennem.core.networks import network_from_network_code
from opennem.db import SessionLocal
from opennem.db.models.opennem import NetworkRegion
from opennem.diff.versions import get_network_regions
from opennem.schema.dates import TimeSeries
from opennem.schema.network import NetworkAPVI, NetworkNEM, NetworkWEM
from opennem.utils.version import get_version

logger = logging.getLogger(__name__)


def export_power(
    stats: List[StatExport] = None,
    priority: Optional[PriorityType] = None,
    latest: Optional[bool] = False,
) -> None:
    """
    Export power stats from the export map


    """
    if not stats:
        export_map = get_export_map().get_by_stat_type(StatType.power)

        if priority:
            export_map = export_map.get_by_priority(priority)

        stats = export_map.resources

    output_count: int = 0

    for power_stat in stats:
        if power_stat.stat_type != StatType.power:
            continue

        if output_count >= 1 and latest:
            return None

        date_range_networks = power_stat.networks or []

        if NetworkNEM in date_range_networks:
            date_range_networks = [NetworkNEM]

        date_range: ScadaDateRange = get_scada_range(
            network=power_stat.network, networks=date_range_networks
        )

        # Migrate to this time_series
        time_series = TimeSeries(
            start=date_range.start,
            end=date_range.end,
            network=power_stat.network,
            year=power_stat.year,
            interval=power_stat.interval,
            period=power_stat.period,
        )

        stat_set = power_week(
            time_series=time_series,
            network_region_code=power_stat.network_region_query or power_stat.network_region,
            networks_query=power_stat.networks,
        )

        if not stat_set:
            logger.info(
                "No power stat set for {} {} {}".format(
                    power_stat.period,
                    power_stat.networks,
                    power_stat.network_region,
                )
            )
            continue

        demand_set = demand_week(
            time_series=time_series,
            networks_query=power_stat.networks,
            network_region_code=power_stat.network_region_query or power_stat.network_region,
        )

        stat_set.append_set(demand_set)

        if power_stat.network_region:
            flow_set = power_flows_region_week(
                time_series=time_series,
                network_region_code=power_stat.network_region,
            )

            if flow_set:
                stat_set.append_set(flow_set)

        time_series_weather = time_series.copy()
        time_series_weather.interval = human_to_interval("30m")

        if power_stat.bom_station:
            weather_set = weather_daily(
                time_series=time_series_weather,
                station_code=power_stat.bom_station,
                network_region=power_stat.network_region,
                include_min_max=False,
                unit_name="temperature",
            )

            stat_set.append_set(weather_set)

        write_output(power_stat.path, stat_set)
        output_count += 1


def export_energy(
    stats: List[StatExport] = None,
    priority: Optional[PriorityType] = None,
    latest: Optional[bool] = False,
) -> None:
    """
    Export energy stats from the export map


    """
    if not stats:
        export_map = get_export_map().get_by_stat_type(StatType.energy)

        if priority:
            export_map = export_map.get_by_priority(priority)

        stats = export_map.resources

    CURRENT_YEAR = datetime.now().year

    for energy_stat in stats:
        if energy_stat.stat_type != StatType.energy:
            continue

        # @FIX trim to NEM since it's the one with the shortest
        # data time span.
        # @TODO find a better and more flexible way to do this in the
        # range method
        date_range_networks = energy_stat.networks or []

        if NetworkNEM in date_range_networks:
            date_range_networks = [NetworkNEM]

        date_range: ScadaDateRange = get_scada_range(
            network=energy_stat.network, networks=date_range_networks
        )

        # Migrate to this time_series
        time_series = TimeSeries(
            start=date_range.start,
            end=date_range.end,
            network=energy_stat.network,
            year=energy_stat.year,
            interval=energy_stat.interval,
            period=human_to_period("1Y"),
        )

        if energy_stat.year:

            if latest and energy_stat.year != CURRENT_YEAR:
                continue

            stat_set = energy_fueltech_daily(
                time_series=time_series,
                networks_query=energy_stat.networks,
                network_region_code=energy_stat.network_region_query or energy_stat.network_region,
            )

            if not stat_set:
                continue

            # Hard coded to NEM only atm but we'll put has_interconnectors
            # in the metadata to automate all this
            if energy_stat.network == NetworkNEM and energy_stat.network_region:
                interconnector_flows = energy_interconnector_region_daily(
                    time_series=time_series,
                    networks_query=energy_stat.networks,
                    network_region_code=energy_stat.network_region_query
                    or energy_stat.network_region,
                )
                stat_set.append_set(interconnector_flows)

                interconnector_emissions = energy_interconnector_emissions_region_daily(
                    time_series=time_series,
                    networks_query=energy_stat.networks,
                    network_region_code=energy_stat.network_region_query
                    or energy_stat.network_region,
                )
                stat_set.append_set(interconnector_emissions)

            if energy_stat.bom_station:
                weather_stats = weather_daily(
                    time_series=time_series,
                    station_code=energy_stat.bom_station,
                    network_region=energy_stat.network_region,
                )
                stat_set.append_set(weather_stats)

            write_output(energy_stat.path, stat_set)

        elif energy_stat.period and energy_stat.period.period_human == "all":
            time_series.period = human_to_period("all")
            time_series.interval = human_to_interval("1M")
            time_series.year = None

            stat_set = energy_fueltech_daily(
                time_series=time_series,
                networks_query=energy_stat.networks,
                network_region_code=energy_stat.network_region_query or energy_stat.network_region,
            )

            if not stat_set:
                continue

            # Hard coded to NEM only atm but we'll put has_interconnectors
            # in the metadata to automate all this
            if energy_stat.network == NetworkNEM and energy_stat.network_region:
                interconnector_flows = energy_interconnector_region_daily(
                    time_series=time_series,
                    networks_query=energy_stat.networks,
                    network_region_code=energy_stat.network_region_query
                    or energy_stat.network_region,
                )
                stat_set.append_set(interconnector_flows)

                interconnector_emissions = energy_interconnector_emissions_region_daily(
                    time_series=time_series,
                    networks_query=energy_stat.networks,
                    network_region_code=energy_stat.network_region_query
                    or energy_stat.network_region,
                )
                stat_set.append_set(interconnector_emissions)

            if energy_stat.bom_station:
                weather_stats = weather_daily(
                    time_series=time_series,
                    station_code=energy_stat.bom_station,
                    network_region=energy_stat.network_region,
                )
                stat_set.append_set(weather_stats)

            write_output(energy_stat.path, stat_set)


def export_all_monthly() -> None:
    session = SessionLocal()
    network_regions = session.query(NetworkRegion).all()

    all_monthly = OpennemDataSet(
        code="au", data=[], version=get_version(), created_at=datetime.now()
    )

    cpi = gov_stats_cpi()
    all_monthly.append_set(cpi)

    for network_region in network_regions:
        network = network_from_network_code(network_region.network.code)
        networks = None

        if network_region.code == "WEM":
            networks = [NetworkWEM, NetworkAPVI]

        scada_range: ScadaDateRange = get_scada_range(network=network, networks=networks)

        time_series = TimeSeries(
            start=scada_range.start,
            end=scada_range.end,
            network=network,
            interval=human_to_interval("1M"),
            period=human_to_period("all"),
        )

        stat_set = energy_fueltech_daily(
            time_series=time_series,
            networks_query=networks,
            network_region_code=network_region.code,
        )

        if not stat_set:
            continue

        if network == NetworkNEM:
            interconnector_flows = energy_interconnector_region_daily(
                time_series=time_series,
                networks_query=networks,
                network_region_code=network_region.code,
            )
            stat_set.append_set(interconnector_flows)

            interconnector_emissions = energy_interconnector_emissions_region_daily(
                time_series=time_series,
                networks_query=networks,
                network_region_code=network_region.code,
            )
            stat_set.append_set(interconnector_emissions)

        all_monthly.append_set(stat_set)

        bom_station = get_network_region_weather_station(network_region.code)

        if bom_station:
            weather_stats = weather_daily(
                time_series=time_series,
                station_code=bom_station,
                network_region=network_region.code,
            )
            all_monthly.append_set(weather_stats)

    write_output("v3/stats/au/all/monthly.json", all_monthly)


def export_all_daily() -> None:
    session = SessionLocal()
    network_regions = session.query(NetworkRegion).all()

    cpi = gov_stats_cpi()

    for network_region in network_regions:
        network = network_from_network_code(network_region.network.code)
        networks = None

        if network_region.code == "WEM":
            networks = [NetworkWEM, NetworkAPVI]

        scada_range: ScadaDateRange = get_scada_range(network=network, networks=networks)

        time_series = TimeSeries(
            start=scada_range.start,
            end=scada_range.end,
            network=network,
            interval=human_to_interval("1d"),
            period=human_to_period("all"),
        )

        stat_set = energy_fueltech_daily(
            time_series=time_series,
            networks_query=networks,
            network_region_code=network_region.code,
        )

        if not stat_set:
            continue

        # Hard coded to NEM only atm but we'll put has_interconnectors
        # in the metadata to automate all this
        if network == NetworkNEM:
            interconnector_flows = energy_interconnector_region_daily(
                time_series=time_series,
                networks_query=networks,
                network_region_code=network_region.code,
            )
            stat_set.append_set(interconnector_flows)

            interconnector_emissions = energy_interconnector_emissions_region_daily(
                time_series=time_series,
                networks_query=networks,
                network_region_code=network_region.code,
            )
            stat_set.append_set(interconnector_emissions)

        bom_station = get_network_region_weather_station(network_region.code)

        if bom_station:
            weather_stats = weather_daily(
                time_series=time_series,
                station_code=bom_station,
                network_region=network_region.code,
            )
            stat_set.append_set(weather_stats)

        if cpi:
            stat_set.append_set(cpi)

        write_output(f"v3/stats/au/{network_region.code}/daily.json", stat_set)


def export_flows() -> None:
    date_range = get_scada_range(network=NetworkNEM)

    interchange_stat = StatExport(
        stat_type=StatType.power,
        priority=PriorityType.live,
        country="au",
        date_range=date_range,
        network=NetworkNEM,
        interval=NetworkNEM.get_interval(),
        period=human_to_period("7d"),
    )

    time_series = TimeSeries(
        start=date_range.start,
        end=date_range.end,
        network=interchange_stat.network,
        interval=interchange_stat.interval,
        period=interchange_stat.period,
    )

    stat_set = power_flows_network_week(time_series=time_series)

    if stat_set:
        write_output(f"v3/stats/au/{interchange_stat.network.code}/flows/7d.json", stat_set)


def export_electricitymap() -> None:
    date_range = get_scada_range(network=NetworkNEM)

    interchange_stat = StatExport(
        stat_type=StatType.power,
        priority=PriorityType.live,
        country="au",
        date_range=date_range,
        network=NetworkNEM,
        interval=NetworkNEM.get_interval(),
        period=human_to_period("1d"),
    )

    time_series = TimeSeries(
        start=date_range.start,
        end=date_range.end,
        network=interchange_stat.network,
        interval=interchange_stat.interval,
        period=interchange_stat.period,
    )

    stat_set = power_flows_network_week(time_series=time_series)

    if not stat_set:
        raise Exception("No flow results for electricitymap export")

    for region in get_network_regions(NetworkNEM):
        power_set = power_week(
            time_series, region.code, include_capacities=True, include_code=False
        )

        if power_set:
            stat_set.append_set(power_set)

    date_range = get_scada_range(network=NetworkWEM)

    # WEM custom
    time_series = TimeSeries(
        start=date_range.start,
        end=date_range.end,
        network=NetworkWEM,
        networks=[NetworkWEM, NetworkAPVI],
        interval=NetworkWEM.get_interval(),
        period=interchange_stat.period,
    )

    power_set = power_week(
        time_series,
        "WEM",
        include_capacities=True,
        networks_query=[NetworkWEM, NetworkAPVI],
        include_code=False,
    )

    if power_set:
        stat_set.append_set(power_set)

    stat_set.type = "custom"

    write_output(f"v3/clients/em/latest.json", stat_set)


def export_metadata() -> bool:
    """
    Export metadata


    """
    _export_map_out = get_export_map()

    # this is a hack because pydantic doesn't
    # serialize properties
    for r in _export_map_out.resources:
        r.file_path = r.path

    wrote_bytes = write_output("metadata.json", _export_map_out)

    if wrote_bytes and wrote_bytes > 0:
        return True

    return False


if __name__ == "__main__":
    # export_power(priority=PriorityType.live)
    export_energy(latest=True)
