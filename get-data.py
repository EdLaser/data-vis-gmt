import requests
from collections import defaultdict


def liter_of_galosine_consumed(co2_emissions: float) -> float:
    """Returns the amount of gasoline consumed in liters based on the amount of CO2 emissions in kg"""
    # Source: https://www.epa.gov/energy/greenhouse-gas-equivalencies-calculator
    return (co2_emissions / 8.89e-3) * 3.79

# def kilometers_driven_by_car(co2_emissions: float) -> float:
#     """Returns the distance driven by a car in kilometers based on the amount of CO2 emissions in kg"""
#     # Source: https://www.epa.gov/energy/greenhouse-gas-equivalencies-calculator
#     return 3.90e-4 * co2_emissions 

def get_data_from_api(run_id):
    API_ENDPOINT = f"https://api.green-coding.berlin/v1/phase_stats/single/{run_id}"
    PHASES = [
        "[BASELINE]",
        "[INSTALLATION]",
        "[BOOT]",
        "[IDLE]",
        "[RUNTIME]",
        "[REMOVE]",
    ]
    COMPONENTS = [
        "phase_time_syscall_system",
        "psu_co2_ac_mcp_machine",
        "network_energy_formula_global",
        "psu_power_ac_mcp_machine",
        "psu_energy_ac_mcp_machine",
    ]

    try:
        response = requests.get(API_ENDPOINT)
        response.raise_for_status()  # This will raise an exception if the request is unsuccessful
        all_data = response.json()["data"]
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return (
            {}
        )  # or handle the error in a way that's appropriate for your application

    extracted_data = defaultdict(lambda: defaultdict(dict))
    for phase in PHASES:
        for component in COMPONENTS:
            component_data = all_data.get("data", {}).get(phase, {}).get(component)

            if component_data:
                component_info = {
                    "type": component_data.get("type"),
                    "unit": component_data.get("unit"),
                    # Extracting mean value might be more complex based on the data structure; this is a simplified approach
                    "value": next(
                        iter(component_data.get("data", {}).values()), {}
                    ).get("mean"),
                }
                extracted_data[phase][component] = component_info
            else:
                extracted_data[phase][component] = {"error": "No data available"}

    return extracted_data


def main():
    # Use your actual run_id
    run_id = ""
    result = get_data_from_api(run_id)

    # Pretty print the result
    import json

    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
