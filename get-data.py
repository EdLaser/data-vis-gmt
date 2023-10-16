import requests


def get_data_from_api(run_id):
    # Endpoint URL
    url = f"https://api.green-coding.berlin/v1/phase_stats/single/{run_id}"

    # Request data from the API
    response = requests.get(url)
    data = response.json()["data"]

    # Define the keys to extract
    phases = ["[BASELINE]", "[INSTALLATION]", "[BOOT]", "[IDLE]", "[RUNTIME]", "[REMOVE]"]

    components = [
        "phase_time_syscall_system",
        "psu_co2_ac_mcp_machine",
        "network_energy_formula_global",
        "psu_power_ac_mcp_machine",
        "psu_energy_ac_mcp_machine",
    ]

    # Extract and print the relevant information
    extracted_data = {}
    for phase in phases:
        extracted_data[phase] = {}
        for component in components:
            try:
                component_data = data["data"][phase][component]
            except KeyError:
                extracted_data[phase][component] = {"error": "No data available"}
            component_type = component_data["type"]
            component_unit = component_data["unit"]

            for package, package_data in component_data["data"].items():
                for mean_data in package_data["data"].values():
                    mean_value = mean_data["mean"]

                    extracted_data[phase][component] = {
                        "type": component_type,
                        "unit": component_unit,
                        "value": mean_value,
                    }

    return extracted_data


run_id = ""  # Replace this with your actual run_id
result = get_data_from_api(run_id)
print(result)
