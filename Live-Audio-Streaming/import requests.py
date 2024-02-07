import requests

def get_location_by_ip():
    ip_address = requests.get('https://api.ipify.org').text  # Get public IP address
    geolocation_api = 'https://api.ipgeolocation.io/ipgeo?apiKey=AIzaSyDMhmSaP4G9p1-dKzeHDbg8HsbrZ1LKps4&ip='
    response = requests.get(geolocation_api + ip_address)
    data = response.json()

    if 'status' in data and data['status'] == 'success':
        area = data['city'] + ', ' + data['region'] + ', ' + data['country_name']
        pincode = data['zip']
        return area, pincode
    else:
        return None, None

area, pincode = get_location_by_ip()

if area and pincode:
    print(f"Area: {area}")
    print(f"Pincode: {pincode}")
else:
    print("Unable to determine location.")
