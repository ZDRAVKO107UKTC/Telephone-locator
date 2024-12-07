import phonenumbers
from phonenumbers import geocoder, timezone, carrier
from opencage.geocoder import OpenCageGeocode
import folium
import os
from colorama import init, Fore

init()

class PhoneNumberTracker:
    def __init__(self, api_key):
        self.api_key = api_key
        self.geocoder = OpenCageGeocode(api_key)
        self.location = None
        self.latitude = None
        self.longitude = None

    def process_number(self, number):
        try:
            parsed_number = phonenumbers.parse(number)
            print(f"{Fore.GREEN}[+] Attempting to track location of "
                  f"{phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}..")
            print(f"{Fore.GREEN}[+] Time Zone ID: {timezone.time_zones_for_number(parsed_number)}")

            self.location = geocoder.description_for_number(parsed_number, "en")
            if self.location:
                print(f"{Fore.GREEN}[+] Region: {self.location}")
            else:
                print(f"{Fore.RED}[-] Region: Unknown")

            service_provider = carrier.name_for_number(parsed_number, 'en')
            if service_provider:
                print(f"{Fore.GREEN}[+] Service Provider: {service_provider}")

        except Exception as e:
            print(f"{Fore.RED}[-] Error processing phone number: {e}")
            raise

    def get_approx_coordinates(self):
        try:
            if not self.location:
                raise ValueError("Location not set. Process a number first.")

            print(f"{Fore.YELLOW}[DEBUG] Geocoding query: {self.location}")
            results = self.geocoder.geocode(self.location)

            if results and len(results) > 0:
                self.latitude = results[0]['geometry']['lat']
                self.longitude = results[0]['geometry']['lng']
                print(f"[+] Latitude: {self.latitude}, Longitude: {self.longitude}")

                address = self.geocoder.reverse_geocode(self.latitude, self.longitude)
                if address:
                    print(f"{Fore.LIGHTRED_EX}[+] Approximate Location is {address[0]['formatted']}")
                else:
                    print(f"{Fore.RED}[-] No address found for the given coordinates.")
            else:
                print(f"{Fore.RED}[-] No results returned for query: {self.location}")
                raise ValueError("Geocoding failed.")

        except Exception as e:
            print(f"{Fore.RED}[-] Error getting coordinates: {e}")
            raise

    def draw_map(self, phone_number):
        try:
            if self.latitude is None or self.longitude is None:
                raise ValueError("Coordinates not set. Get coordinates first.")

            my_map = folium.Map(location=[self.latitude, self.longitude], zoom_start=9)
            folium.Marker([self.latitude, self.longitude], popup=self.location).add_to(my_map)

            cleaned_phone_number = self.clean_phone_number(phone_number)
            file_name = f"{cleaned_phone_number}.html"
            my_map.save(file_name)
            print(f"[+] See Aerial Coverage at: {os.path.abspath(file_name)}")
        except Exception as e:
            print(f"{Fore.RED}[-] Error drawing map: {e}")

    @staticmethod
    def clean_phone_number(phone_number):
        return ''.join(char for char in phone_number if char.isdigit() or char == '+')
