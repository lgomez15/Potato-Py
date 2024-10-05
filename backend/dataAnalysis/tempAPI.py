import requests as r
import getpass, pprint, time, os, cgi

def fetch_data(longitude, latitude, region, startDate, endDate):
    api = 'https://appeears.earthdatacloud.nasa.gov/api/'   # Set the AρρEEARS API to a variable

    user = "Radul003"      # Input NASA Earthdata Login Username
    password = "PotatoPy2024!"  # Input NASA Earthdata Login Password

    token_response = r.post('{}login'.format(api), auth=(user, password)).json() # Insert API URL, call login service, provide credentials & return json
    del user, password                                                           # Remove user and password information
    print(token_response)                                                        # Print response

    product_response = r.get('{}product'.format(api)).json()                         # request all products in the product service
    print('AρρEEARS currently supports {} products.'.format(len(product_response)))  # Print no. products available in AρρEEARS

    products = {p['ProductAndVersion']: p for p in product_response} # Create a dictionary indexed by product name & version
    print(products['MOD11A1.061'])                                   # Print information 

    prods = ['MOD11A1.061']     # Start a list for products to be requested, beginning with MCD15A3H.006
    print(prods)

    lst_response = r.get('{}product/{}'.format(api, prods[0])).json()  # Request layers for the 2nd product (index 1) in the list: MOD11A2.061
    print(list(lst_response.keys()))

    print(lst_response['LST_Day_1km']) # Print layer response

    layers = [(prods[0], 'LST_Day_1km')] # Create a list of tuples for the product and layer

    prodLayer = []
    for l in layers:
        prodLayer.append({
                "layer": l[1],
                "product": l[0]
            })
    prodLayer

    token = token_response['token']                      # Save login token to a variable
    head = {'Authorization': 'Bearer {}'.format(token)}  # Create a header to store token information, needed to submit request

    task_type = ['point','area']        # Type of task, area or  point
    recurring = False             # Specify True for a recurring date range

    coordinates = [{
            "id": "0",
            "longitude": longitude,
            "latitude": latitude,
            "category": region
            }]

    task = {
        'task_type': task_type[0],
        'task_name': "LST_Request",
        'params': {
            'dates': [
            {
                'startDate': startDate,
                'endDate': endDate
            }],
            'layers': prodLayer,
            'coordinates': coordinates
        }
    }
    pprint.pprint(task)

    task_response = r.post('{}task'.format(api), json=task, headers=head).json()  # Post json to API task service, return response as json
    print("Task Response:" + str(task_response))                                                                 # Print task response

    params = {'limit': 2, 'pretty': True} # Limit API response to 2 most recent entries, return as pretty json

    tasks_response = r.get('{}task'.format(api),params = params, headers=head).json() # Query task service setting params & header
    print(tasks_response)                                                             # Print tasks response

    task_id = task_response['task_id']                                               # Set task id from request submission
    status_response = r.get('{}status/{}'.format(api, task_id), headers=head).json() # Call status service w/ specific task ID & username
    print(status_response)                                                               # Print response

    # Ping API until request is complete, then continue to Section 4
    starttime = time.time()
    while r.get('{}task/{}'.format(api, task_id), headers=head).json()['status'] != 'done':
        print(r.get('{}task/{}'.format(api, task_id), headers=head).json()['status'])
        time.sleep(20.0 - ((time.time() - starttime) % 20.0))
    print(r.get('{}task/{}'.format(api, task_id), headers=head).json()['status'])

    bundle = r.get('{}bundle/{}'.format(api,task_id), headers=head).json()  # Call API and return bundle contents for the task_id as json
    print(bundle)                                                            # Print bundle contents

    files = {}                                                       # Create empty dictionary
    for f in bundle['files']: files[f['file_id']] = f['file_name']   # Fill dictionary with file_id as keys and file_name as values
    print(files)                                                         # Print dictionary

    for f in files:
        dl = r.get('{}bundle/{}/{}'.format(api, task_id, f), headers=head, stream=True, allow_redirects = "TRUE")  # Get a stream to the bundle file
        if files[f].endswith('.tif'):
            filename = files[f].split('/')[1]
        else:
            filename = files[f]
        filepath = os.path.join("./", filename)                                            # Create output file path
        with open(filepath, 'wb') as f:                                                       # Write file to dest dir
            for data in dl.iter_content(chunk_size=8192): f.write(data) 
    print('Downloaded files can be found')