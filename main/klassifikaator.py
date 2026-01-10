import requests
import aiohttp
import asyncio

"""
https://term.tehik.ee/fhir/CodeSystem/$lookup?system=https://fhir.ee/CodeSystem/rfk&code=d
"""
BASE_URL = "https://term.tehik.ee/fhir/CodeSystem/$lookup"
params = {
    'system': "https://fhir.ee/CodeSystem/rfk",
    'code': "d"
}
headers = {
    # "accept": "application/json; charset=utf-8",
    "content-type": "application/json",
    # "user-agent": "G-RAC",
}

async def main():

    # async with aiohttp.ClientSession() as session:
    #     async with session.get('http://python.org') as response:

    #         print("Status:", response.status)
    #         print("Content-type:", response.headers['content-type'])

    #         html = await response.text()
    #         print("Body:", html[:15], "...")
    
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, params=params, headers=headers) as response:
            print(str(response.url))
            expect = 'https://term.tehik.ee/fhir/CodeSystem/$lookup?system=https://fhir.ee/CodeSystem/rfk&code=d'
            assert str(response.url) == expect

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])


if __name__ == "__main__":
    asyncio.run(main())

def lookup_rfk_code(code):
    """
    Looks up an RFK code in the TEHIK FHIR terminology server.

    Args:
        code: The RFK code to look up.

    Returns:
        The JSON response from the server, or None if an error occurs.
    """
    fhir_server_url = "https://term.tehik.ee/fhir"
    valueset_url = "https://fhir.ee/ValueSet/rfk"
    
    # The FHIR API query to expand the ValueSet and filter by the specific code
    query_params = {
        "url": valueset_url,
        "filter": code,
        "_format": "json"
    }
    
    try:
        response = requests.get(f"{fhir_server_url}/ValueSet/$expand", params=query_params)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Example usage:
rfk_code_to_find = "d450"
result = lookup_rfk_code(rfk_code_to_find)
print(result)
    
