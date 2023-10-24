
##This script creates a Flask api that generates a list of profiles containing the parameters:
# name, occupation, purchase, address1, address2, city, coordinates, postalCode, state
# These parameters are randomly generated using the following modules
# Personal details = faker
# Purchase details = faker_commerce
# Address = random_address

#A route is defined for the URL path '/api/profiles' with an HTTP GET method, which calls generate_fake_profile()
#Example GET request 
#response = requests.get(f'http://127.0.0.1:5000/api/profiles?count={number_of_profiles}')
#Generate_fake_profile returns a dictionary of x number of profiles, or a default list of 1 profile

#This script must be ran as the main program to start the web application

#Example
{'Name': 'Nicole Nolan',
  'Occupation': 'Manufacturing engineer',
  'Purchase': 'Automotive',
  'address1': '1030 Lake Claire Drive',
  'address2': '',
  'city': 'Annapolis',
  'coordinates': {'lat': 39.048603, 'lng': -76.448911},
  'postalCode': '21409',
  'state': 'MD'}




from flask import Flask, jsonify, request
from faker import Faker
import faker_commerce
from random_address import real_random_address
app = Flask(__name__)
fake = Faker()
fake.add_provider(faker_commerce.Provider)


@app.route('/api/profiles', methods=['GET'])
def generate_fake_profile():
    num_profiles = request.args.get('count', default=1, type=int)
    
    profile_list = {
        "profiles": {}
    }
    for i in range(num_profiles):
        address = real_random_address()
        name = fake.name()
        profile = {
            "Occupation":fake.job(),
            "Purchase":fake.ecommerce_category()
        }
        profile |=address #concatanate the address and profile dictionaries
        profile_list["profiles"][name] = profile
        
    return jsonify(profile_list)

if __name__ == '__main__':
    app.run()