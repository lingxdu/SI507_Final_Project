import json
import requests

####################
###### Step 1 ######
####################
# Create functions for storing data from APIs

# Define save cache function
def save_cache(cache_dict):
    ''' saves the current state of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
         The dictionary to save
    
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    cache_file = open(CACHE_FILENAME, "w")
    cache_file.write(dumped_json_cache)
    cache_file.close()


####################
###### Step 2 ######
####################
# Build functions for getting data from Yelp Fusion API and Google Place API

CACHE_FILENAME = "cache.json"

# Create a dictionary with one list of 8 universities in Michigan and one of 6 types of cuisines
university_cuisine = {"university": ["Central Michigan University", "Eastern Michigan University", "Michigan State University", "Michigan Technological University", "Oakland University", "University of Michigan", "Wayne State University", "Western Michigan University"],
                      "cuisine": ["American", "Chinese", "Italian", "Japanese", "Mexican", "Thai"]}


# Find the top 30 best match restaurants for each of the 6 cuisines from Yelp Fusion API
def yelp_api_function(university_each, cuisine_each):
    baseurl = "https://api.yelp.com/v3/businesses/search"
    params = {"location": university_each, "term": cuisine_each, "categories": "restaurants", "sort_by": "best_match", "limit": 30}
    yelp_api_key = "P0fru-uRT9KiJ9bX2b6U49W9qRLQIeKsfCFynAUj51Y1wlpyTN9doZ-puS4UcIwK4YXVfQ-s8gA4DcZ12_62AYQ458_VQSqRHtYVYby-ncnWpekUyMb_WN3r-5qSY3Yx"
    headers = {'Authorization': 'Bearer %s' % yelp_api_key}

    response_json = requests.get(url=baseurl, params=params, headers=headers)
    response_dict = json.loads(response_json.text)
    return response_dict["businesses"]


# Get raw data from the Google Place API for parks with a radius of 1500 meters from each restaurant
def google_api_function(coordinates):
    baseurl = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    google_api_key = "AIzaSyAuXCfY8bCc_xSoyrm2M4FMnM5zXIxaDSA"
    params = {"location": coordinates, "radius": 1500, "types": "park", "key": google_api_key}
    
    response_json = requests.get(baseurl, params=params)
    response_dict = json.loads(response_json.text)
    return response_dict["results"]


# Extract the place name, place rating, place type, user ratings total, and vicinity categories 
# from the original data obtained by Google Place API
def nearby_function(google_api):
    list_n = []
    for cc in google_api:
        dict_n = {}    
        dict_n["Place name"] = cc["name"]
        # rating category
        if "rating" in cc.keys():
            dict_n["Place rating"] = cc["rating"]
        else:
            dict_n["Place rating"] = "No rating"
        dict_n["Place type"] = cc["types"][0]
        # User ratings total category
        if "user_ratings_total" in cc.keys():
            dict_n["User ratings total"] = cc["user_ratings_total"]
        else:
            dict_n["User ratings total"] = "No user ratings number"
        dict_n["Vicinity"] = cc["vicinity"]
        list_n.append(dict_n)
    return list_n[:3]


# Define a function for creating a dictionary of 6 types of cuisine for a university.
# There are 8 categories in the dictinary: Name: name of a restaurant
#                                          Price: 4 categories of lower, low, high and higher
#                                          Rating: rating of a restaurant
#                                          Distance: distance from this university, and 3 categories are recommended: walking, taking bus and driving
#                                          Location: address of this restaurant
#                                          Phone: phone number of of this restaurant
#                                          Coordinates: latitude and longitude coordinates of this restaurant
#                                          Nearby parks: 3 closest parks to this restaurant
def cuisine_each_function(university_each):   
    dict_1 = {}
    for cuisine_each in university_cuisine["cuisine"]:
        list_2 = []
        list_3 = yelp_api_function(university_each, cuisine_each)
        for item in list_3:
            dict_2 = {}
            dict_2["Name"] = item["name"]
            # Pricing levels to filter the search result with: 1 = $, 2 = $$, 3 = $$$, 4 = $$$$
            if "price" in item.keys():
                if item["price"] == "$":
                    dict_2["Price"] = "lower"
                elif item["price"] == "$$":
                    dict_2["Price"] = "low"
                elif item["price"] == "$$$":
                    dict_2["Price"] = "high"
                elif item["price"] == "$$$$":
                    dict_2["Price"] = "higher"
            dict_2["Rating"] = item["rating"]
            # Distance levels: < 1500 meters == on foot, >=1500 meters and < 5000 meters == by bus, >= 5000 meters == by car
            if "distance" in item.keys():
                if item["distance"] <= 1500:
                    dict_2["Distance"] = "near (recommend: go on foot)"
                elif (1500 < item["distance"]) and (item["distance"] <= 5000):
                    dict_2["Distance"] = "far (recommend: go by bus)"
                elif item["distance"] > 5000:
                    dict_2["Distance"] = "faraway (recommend: go by car)"
            dict_2["Address"] = ", ".join(item["location"]["display_address"])
            dict_2["Phone"] = item["display_phone"]
            dict_2["Coordinates"] = item["coordinates"]["latitude"], item["coordinates"]["longitude"]
            # Find the nearby park in gooogle Places API by using the latitude and longtitude attained in Yelp Fusion API. 
            coordinates_each = ",".join(str(i) for i in dict_2["Coordinates"])
            coordinates_each_aa = google_api_function(coordinates_each)
            nearby_park = nearby_function(coordinates_each_aa)
            dict_2["Nearby parks"] = nearby_park
            list_2.append(dict_2)
            dict_1[cuisine_each] = list_2
    return dict_1


####################
###### Step 3 ######
####################

# Creat a dictionary of 6 cuisines for 8 universities in Michigan, 
# form like: {"Central Michigan University": [{"American": [{"Name": ...}], "Chinese": [{"Name": ...}],...}], 
#             "Eastern Michigan University": [{"American": [{"Name": ...}], "Chinese": [{"Name": ...}],...}],
#              ...
#             }
dict_3 = {}
for university_each in university_cuisine["university"]:
    list_4 = []
    dict_4 = cuisine_each_function(university_each)
    list_4.append(dict_4)
    dict_3[university_each] = list_4
save_cache(dict_3)