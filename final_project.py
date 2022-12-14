import json
import numpy as np
import itertools
from flask import Flask, render_template, request
import plotly.graph_objects as go
import plotly.express as px

####################
###### Step 1 ######
####################
# Create functions for getting data from cache

CACHE_FILENAME = "cache.json"

# Define open cache function
def open_cache():
    ''' opens the cache file if it exists and loads the JSON into
    the FIB_CACHE dictionary.

    if the cache file doesn't exist, creates a new cache dictionary
 
    Parameters
    ----------
    None

    Returns
    -------
    The opened cache
    '''
    try:
        cache_file = open(CACHE_FILENAME, "r")
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

cache_data_raw = open_cache()


####################
###### Step 2 ######
####################
# define funtions to get the useful info in cache, and prepare data for using in Flask

# Create a dictionary with one list of 8 universities in Michigan and one of 6 types of cuisines
university_cuisine = {"university": ["Central Michigan University", "Eastern Michigan University", "Michigan State University", "Michigan Technological University", "Oakland University", "University of Michigan", "Wayne State University", "Western Michigan University"],
                      "cuisine": ["American", "Chinese", "Italian", "Japanese", "Mexican", "Thai"]}


def sort_tuple(vvv, reverse):
    """
    sort a list of tuples, key is set to sort using second element of sublist lambda has been used

    Parameters
    ----------
    a list of tuples: vvv
    reverse = None(default) (Sorts in ascending order)

    Returns
    -------
    a list of sorted tuples
    """    
    vvv.sort(key = lambda x: x[1], reverse=reverse)
    return vvv


def get_name_rating_info(university_each, cuisine_each):
    """
    Get the name amd rating of restaurants information from raw data

    Parameters
    ----------
    str: a name of an university
    str: a name of one type of cuisine

    Returns
    -------
    a list of tuples, with name(str) as the first one and rating(float) as the second one
    [("name", rating), ("name", rating), ...]
    """   
    basic_info_raw = cache_data_raw[university_each]
    list_1 = []
    i = 1
    for item in basic_info_raw:
        for aa in item[cuisine_each]:
            cc = (aa["Name"], aa["Rating"])
            list_1.append(cc)
            i += 1
    return list_1


def get_name_price_info(university_each, cuisine_each):
    """
    Get the name amd price of restaurants information from raw data

    Parameters
    ----------
    str: a name of an university
    str: a name of one type of cuisine

    Returns
    -------
    a list of tuples, with name(str) as the first one and price(int) as the second one, 
    [("name", price), ("name", price), ...]
    lower==1, low==2, high==3, higher==4, price==5 if there is no price info.
    """   
    basic_info_raw = cache_data_raw[university_each]
    list_1 = []
    i = 1
    for item in basic_info_raw:
        for aa in item[cuisine_each]:
            if "Price" in aa.keys():
                if aa["Price"] == "lower":
                    cc = (aa["Name"], 1)
                elif aa["Price"] == "low":
                    cc = (aa["Name"], 2)
                elif aa["Price"] == "high":
                    cc = (aa["Name"], 3)
                elif aa["Price"] == "higher":
                    cc = (aa["Name"], 4)
            else:
                cc = (aa["Name"], 5)
            list_1.append(cc)
            i += 1
    return list_1


def get_name_distance_info(university_each, cuisine_each):
    """
    Get the name and distance of restaurant from a near univeristy

    Parameters
    ----------
    str: a name of an university
    str: a name of one type of cuisine

    Returns
    -------
    a list of tuples, with name(str) as the first one and distance(int) as the second one
    near==1, far==2, faraway==3, distance==5 if there is no distance info.
    """   
    basic_info_raw = cache_data_raw[university_each]
    list_1 = []
    i = 1
    for item in basic_info_raw:
        for aa in item[cuisine_each]:
            if "Distance" in aa.keys():
                if aa["Distance"] == "near (recommend: go on foot)":
                    cc = (aa["Name"], 1)
                elif aa["Distance"] == "far (recommend: go by bus)":
                    cc = (aa["Name"], 2)
                elif aa["Distance"] == "faraway (recommend: go by car)":
                    cc = (aa["Name"], 3)
            else:
                cc = (aa["Name"], 5)
            list_1.append(cc)
            i += 1
    return list_1


def get_sort_by(university_each, cuisine_each, sort_by, sort_order):
    """
    If users choose to sort by rating, return a list of tuples as in the order of rating, 
    or return a list sorted by price when choosing to sort by price, or return sorted by proximity.
    The reserve is determined by whether the user chooses ascending or descending order.

    Parameters
    ----------
    str: a name of an university
    str: a name of one type of cuisine
    str: two variable users select in a form. sort by mean chose whether sort in the order of 
    rating, price, or distance. There are two direction in the sort order: high to low, and low to high.

    Returns
    -------
    a list of sorted tuples
    """       
    if sort_by == "rating":
        vvv = get_name_rating_info(university_each, cuisine_each)
        if sort_order == "descending":
            reverse=True
        else:
            reverse=False
        return sort_tuple(vvv,reverse)
    elif sort_by == "price":
        vvv = get_name_price_info(university_each, cuisine_each)
        if sort_order == "descending":
            reverse=True
        else:
            reverse=False
        return sort_tuple(vvv,reverse)
    elif sort_by == "distance":
        vvv = get_name_distance_info(university_each, cuisine_each)
        if sort_order == "descending":
            reverse=True
        else:
            reverse=False
        return sort_tuple(vvv,reverse)


# creat function for calculate the mean rating 
def get_cuisine_each_rating():
    """
    Get the total rating for the 6 cuisines in 8 universities

    Parameters
    ----------
    None

    Returns
    -------
    a list of lists with 48 rating(float). 
    [[num, num, num], [num, num, num], ...]
    """   
    list_1 = []
    list_2 = []
    for aa in university_cuisine["university"]:
        for bb in cache_data_raw[aa]:
            for cc in university_cuisine["cuisine"]:
                dd = bb[cc]
                list_2 = [gg["Rating"] for gg in dd]                        
                list_1.append(list_2)           
    return list_1


def get_cuisine_each_mean_rating():
    """
    Get an overall average rating for the 6 cuisines in 8 universities

    Parameters
    ----------
    None

    Returns
    -------
    a list with 6 rating(float). 
    [num, num, num, num, num, num]
    """
    i = 0
    list_4 = []
    list_5 = []
    for i in range(len(university_cuisine["cuisine"])):
        list_3 = list(itertools.chain.from_iterable(get_cuisine_each_rating()[(i)::6]))
        list_4 = round(float(np.mean(list_3)), 3)
        list_5.append(list_4)
        i +=1
    return list_5 # [3.82, 3.494, 3.767, 3.801, 3.797, 3.648]
list_cuisine_each_mean_rating = get_cuisine_each_mean_rating()


def get_cuisine_each_median_rating():
    """
    Get an overall median rating for the 6 cuisines in 8 universities

    Parameters
    ----------
    None

    Returns
    -------
    a list with 6 rating(float). 
    [num, num, num, num, num, num]
    """  
    i = 0
    list_7 = []
    list_8 = []
    for i in range(len(university_cuisine["cuisine"])):
        list_6 = list(itertools.chain.from_iterable(get_cuisine_each_rating()[(i)::6]))
        list_7 = np.median(list_6)
        list_8.append(list_7)
        i +=1
    return list_8 # [4.0, 3.5, 4.0, 4.0, 4.0, 4.0]
list_cuisine_each_median_rating = get_cuisine_each_median_rating()


# calculate average price and average distance
def price_data():
    """
    Get an overall average price for the 6 cuisines in 8 universities.
    reclassify the price into 3 levels: lower==1, low==2, high and higher==3.

    Parameters
    ----------
    None

    Returns
    -------
    a float. 
    """  
    list_1 = []
    list_2 = []
    list_3 = []
    for aa in university_cuisine["university"]:
        for bb in cache_data_raw[aa]:
            for cc in university_cuisine["cuisine"]:
                dd = bb[cc]
                for gg in dd:
                    if "Price" in gg.keys():
                        list_1.append(gg["Price"])
    for element in list_1:
        if element == "lower":
            list_2.append(1)
        elif element == "low":
            list_2.append(2)
        elif element == "high" or element == "higher":
            list_2.append(3)
        list_3 = np.mean(list_2)               
    return list_3


def distance_data():
    """
    Get an overall average distance for the 6 cuisines in 8 universities.
    reclassify the distance into 3 levels: near==1, far==2, faraway==3.

    Parameters
    ----------
    None

    Returns
    -------
    a float. 
    """  
    list_4 = []
    list_5 = []
    list_6 = []
    for aa in university_cuisine["university"]:
        for bb in cache_data_raw[aa]:
            for cc in university_cuisine["cuisine"]:
                dd = bb[cc]
                for gg in dd:
                    if "Distance" in gg.keys():
                        list_4.append(gg["Distance"])
    for element in list_4:
        if element == "near (recommend: go on foot)":
            list_5.append(1)
        elif element == "far (recommend: go by bus)":
            list_5.append(2)
        elif element == "faraway (recommend: go by car)":
            list_5.append(3)
        list_6 = np.mean(list_5)           
    return list_6


# get the list of restarurants corresponding to 4 price levels or 3 distance levels.
def get_price_list(university_each, cuisine_each):
    """
    Get 4 list of restarurants corresponding to 4 price levels.

    Parameters
    ----------
    str: a name of an university
    str: a name of one type of cuisine

    Returns
    -------
    4 list corresponding to four price levels.
    """ 
    basic_info_raw = cache_data_raw[university_each]
    list_price_lower_name = []
    list_price_low_name = []
    list_price_high_name = []
    list_price_higher_name = []

    for item in basic_info_raw:
        for aa in item[cuisine_each]:
            if "Price" in aa.keys():
                if aa["Price"] == "lower":
                    list_price_lower_name.append(aa["Name"])
                elif aa["Price"] == "low":
                    list_price_low_name.append(aa["Name"])
                elif aa["Price"] == "high":
                    list_price_high_name.append(aa["Name"])
                elif aa["Price"] == "higher":
                    list_price_higher_name.append(aa["Name"])

    return list_price_lower_name, list_price_low_name, list_price_high_name, list_price_higher_name


def get_price_flask(university_each, cuisine_each, price_level):
    """
    Determine which cuisine, university and price level the user has chosen.

    Parameters
    ----------
    str: a name of an university
    str: a name of one type of cuisine
    str: a level of price the user has chosen

    Returns
    -------
    a list corresponding to the price level the user has chosen.
    """ 
    list_price_lower_name, list_price_low_name, list_price_high_name, list_price_higher_name = get_price_list(university_each, cuisine_each)
    if price_level == "low":
        return list_price_low_name
    elif price_level == "lower":
        return list_price_lower_name
    elif price_level == "high":
        return list_price_high_name
    elif price_level == "higher": 
        return list_price_higher_name


def price_list_num(university_each, cuisine_each, price_level):
    """
    Give the number of restaurants corresponding to the user's chosen.

    Parameters
    ----------
    str: a name of an university
    str: a name of one type of cuisine
    str: a level of price the user has chosen

    Returns
    -------
    num: the number of restaurants corresponding to the user's chosen.
    """ 
    aa = len(get_price_flask(university_each, cuisine_each, price_level))
    return aa


def get_distance_list(university_each, cuisine_each):
    """
    Get 3 list of restarurants corresponding to 3 distance levels.

    Parameters
    ----------
    str: a name of an university
    str: a name of one type of cuisine

    Returns
    -------
    3 list corresponding to 3 distance levels.
    """ 
    basic_info_raw = cache_data_raw[university_each]
    list_distance_near_name = []
    list_distance_far_name = []
    list_distance_faraway_name = []

    for item in basic_info_raw:
        for aa in item[cuisine_each]:
            if "Distance" in aa.keys():
                if aa["Distance"] == "near (recommend: go on foot)":
                    list_distance_near_name.append(aa["Name"])
                elif aa["Distance"] == "far (recommend: go by bus)":
                    list_distance_far_name.append(aa["Name"])
                elif aa["Distance"] == "faraway (recommend: go by car)":
                    list_distance_faraway_name.append(aa["Name"])

    return list_distance_near_name, list_distance_far_name, list_distance_faraway_name


def get_distance_flask(university_each, cuisine_each, distance_level):
    """
    Determine which cuisine, university and distance level the user has chosen.

    Parameters
    ----------
    str: a name of an university
    str: a name of one type of cuisine
    str: a level of distance the user has chosen

    Returns
    -------
    a list corresponding to the distance level the user has chosen.
    """ 
    list_distance_near_name, list_distance_far_name, list_distance_faraway_name = get_distance_list(university_each, cuisine_each)
    if distance_level in "near (recommend: go on foot)":
        return list_distance_near_name
    elif distance_level in "far (recommend: go by bus)":
        return list_distance_far_name
    elif distance_level in "faraway (recommend: go by car)":
        return list_distance_faraway_name


def distance_list_num(university_each, cuisine_each, price_level):
    """
    Give the number of restaurants corresponding to the user's chosen.

    Parameters
    ----------
    str: a name of an university
    str: a name of one type of cuisine
    str: a level of distance the user has chosen

    Returns
    -------
    num: the number of restaurants corresponding to the user's chosen.
    """ 
    aa = len(get_distance_flask(university_each, cuisine_each, price_level))
    return aa


####################
###### Step 3 ######
####################
# use Flask App
app = Flask(__name__)

# a filter form
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def index_1():
    return render_template('index.html')

@app.route('/form', methods=['POST'])
def results():
    university_select = request.form['university']
    cuisine_select = request.form['cuisine']
    sort_by = request.form['sort']
    sort_order = request.form['dir']
    results = get_sort_by(university_select, cuisine_select, sort_by, sort_order)
    return render_template('form.html', 
                            sort=sort_by, 
                            dir=sort_order,
                            university_select=university_select,
                            cuisine_select=cuisine_select,
                            results=results)


# a scatter chart: mean rating and median rating for 6 cuisines
@app.route('/rating')
def rating():
    cuisine = ["American", "Chinese", "Italian", "Japanese", "Mexican", "Thai"]
    rating_mean = list_cuisine_each_mean_rating
    rating_median = list_cuisine_each_median_rating

    fig_raw = px.scatter(x=rating_mean, y=rating_median, color=cuisine,
                    labels={
                        "x": "The mean rating of cuisine in 8 univeristies",           
                        "y": "The median rating of cuisine in 8 univeristies",
                        "color": "Types of cuisine"
                    },
                    title = "Mean Rating vs Median Rating")
    fig = fig_raw.to_html(full_html=False)

    return render_template('rating.html', 
                            fig=fig)

@app.route('/rating.html')
def rating_1():
    cuisine = ["American", "Chinese", "Italian", "Japanese", "Mexican", "Thai"]
    rating_mean = list_cuisine_each_mean_rating
    rating_median = list_cuisine_each_median_rating

    fig_raw = px.scatter(x=rating_mean, y=rating_median, color=cuisine,
                    labels={
                        "x": "The mean rating of cuisine in 8 univeristies",           
                        "y": "The median rating of cuisine in 8 univeristies",
                        "color": "Types of cuisine"
                    },
                    title = "Mean Rating vs Median Rating")
    fig = fig_raw.to_html(full_html=False)

    return render_template('rating.html', 
                            fig=fig)


# a graph: total mean price VS total mean distance
@app.route('/mean')
def mean():
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=['Mean Price', 'Mean Distance'],
        x=[price_data(), distance_data()],
        name='Total Mean Price VS Total Mean Distance',
        orientation='h',
        marker=dict(
            color='#9E2F7B',
            line=dict(color='white', width=3)
        )
    ))
    fig = fig.to_html(full_html=False)

    return render_template('mean.html', 
                            fig=fig)

@app.route('/mean.html')
def mean_1():
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=['Mean Price', 'Mean Distance'],
        x=[price_data(), distance_data()],
        name='Total Mean Price VS Total Mean Distance',
        orientation='h',
        marker=dict(
            color='#9E2F7B',
            line=dict(color='white', width=3)
        )
    ))
    fig = fig.to_html(full_html=False)

    return render_template('mean.html', 
                            fig=fig)
                

# a form: get the list of restaurants with a certain price level
@app.route('/price')
def price():
    return render_template('price.html')

@app.route('/price.html')
def price_1():
    return render_template('price.html')

@app.route('/price_results', methods=['POST'])
def price_results():
    university_select = request.form['university']
    cuisine_select = request.form['cuisine']
    price_level = request.form['price_level']
    price_results = get_price_flask(university_select, cuisine_select, price_level)
    num = price_list_num(university_select, cuisine_select, price_level)
    return render_template('price_results.html', 
                            num=num, 
                            level=price_level,     
                            university_select=university_select,                       
                            cuisine_select=cuisine_select, 
                            price_results=price_results)


# a form: get the list of restaurants with a certain distance level
@app.route('/distance')
def distance():
    return render_template('distance.html')

@app.route('/distance.html')
def distance_1():
    return render_template('distance.html')

@app.route('/distance_results', methods=['POST'])
def distance_results():
    university_select = request.form['university']
    cuisine_select = request.form['cuisine']
    distance_level = request.form['distance_level']
    distance_results = get_distance_flask(university_select, cuisine_select, distance_level)
    num = distance_list_num(university_select, cuisine_select, distance_level)
    return render_template('distance_results.html', 
                            num=num, 
                            level=distance_level,     
                            university_select=university_select,                       
                            cuisine_select=cuisine_select, 
                            distance_results=distance_results)


if __name__ == '__main__':
    app.run(debug=True)