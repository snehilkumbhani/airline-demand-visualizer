def parse_flight_data(raw_data):
    route_stats = {}
    airline_stats = {}
    status_stats = {}

    for item in raw_data.get("data", []):
        try:
            origin = item["departure"]["airport"]
            destination = item["arrival"]["airport"]
            airline_name = item["airline"]["name"]
            flight_status = item["flight_status"]

            route_key = f"{origin} ➝ {destination}"

            route_stats[route_key] = route_stats.get(route_key, 0) + 1
            airline_stats[airline_name] = airline_stats.get(airline_name, 0) + 1
            status_stats[flight_status] = status_stats.get(flight_status, 0) + 1

        except KeyError:
            continue  # skip if any field is missing

    return {
        "top_routes": sorted(route_stats.items(), key=lambda x: x[1], reverse=True),
        "top_airlines": sorted(airline_stats.items(), key=lambda x: x[1], reverse=True),
        "flight_statuses": status_stats
    }
