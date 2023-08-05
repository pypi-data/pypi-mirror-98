"""
    Create stations on NEM for import/export series
    and facility for one each of import/export
"""

import logging
from datetime import datetime

from opennem.core.dispatch_type import DispatchType
from opennem.core.flows import FlowDirection, generated_flow_station_id
from opennem.core.networks import get_network_region_schema, state_from_network_region
from opennem.db import SessionLocal
from opennem.db.models.opennem import Facility, Location, Station
from opennem.schema.network import NetworkNEM, NetworkSchema

logger = logging.getLogger("opennem.importer.trading_flows")

IMPORTER_NAME = "opennem.importer.trading_flows"


def setup_network_flow_stations(network: NetworkSchema = NetworkNEM) -> None:
    """Creats a station for each network region and a facility for each of imports
    exports so that energy values in facility_scada can be matched up per-region"""

    session = SessionLocal()

    network_regions = get_network_region_schema(network)

    for network_region in network_regions:
        logger.info(f"Setting up for network {network.code} and region: {network_region.code}")

        flow_station_id = generated_flow_station_id(network, network_region)

        flow_station = (
            session.query(Station)
            .filter_by(code=flow_station_id)
            .filter_by(network_code=flow_station_id)
            .one_or_none()
        )

        if not flow_station:
            flow_station = Station(code=flow_station_id, network_code=flow_station_id)

        flow_station.approved = True
        flow_station.approved_by = IMPORTER_NAME
        flow_station.created_by = IMPORTER_NAME

        if not flow_station.location:
            flow_station.location = Location(state=state_from_network_region(network_region.code))

        flow_station.name = "Flows for {} state {}".format(
            network.code.upper(), state_from_network_region(network_region.code.upper())
        )

        flow_facilities = [
            (i, generated_flow_station_id(network, network_region, i)) for i in FlowDirection
        ]

        for (flow_direction, flow_facility_id) in flow_facilities:
            flow_facility_model = (
                session.query(Facility)
                .filter_by(code=flow_facility_id)
                .filter_by(dispatch_type=DispatchType.GENERATOR)
                .filter_by(network_id=network.code)
                .filter_by(network_region=network_region.code)
                .one_or_none()
            )

            if not flow_facility_model:
                flow_facility_model = Facility(  # type: ignore
                    code=flow_facility_id,
                    dispatch_type=DispatchType.GENERATOR,
                    network_id=network.code,
                    network_region=network_region.code,
                )

            flow_facility_model.status_id = "operating"
            flow_facility_model.approved = True
            flow_facility_model.approved_by = IMPORTER_NAME
            flow_facility_model.created_by = IMPORTER_NAME
            flow_facility_model.fueltech_id = flow_direction.value
            flow_facility_model.updated_at = datetime.now()

            flow_station.facilities.append(flow_facility_model)

            session.add(flow_station)

            logger.info(
                "Created network trading flow station facility: {}".format(flow_facility_id)
            )

    session.commit()

    return None


if __name__ == "__main__":
    setup_network_flow_stations()
