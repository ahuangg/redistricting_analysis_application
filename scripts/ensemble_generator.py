import numpy as np

xmin = 0
xmax = 100
ymin = 0
ymax = 100
n_centroids = 30


measures = [
    ["Average African American population %",0,100.0, "%"],
    ["# of districts > 30% African American",0,14,"# Districts"],   
    ["Republican/Democrat vote share",0,100.0, "%"],
    ["# of districts over median salary",0,14, "# Districts"],
]

centroids = []
clusters = []
for i in range(n_centroids):
    point = {}
    for measure in measures:
        point[measure[0]] = np.random.uniform(measure[1], measure[2])
        point[measure[0]] = int(point[measure[0]]*100)/100
        point['units'] = measure[3]
    centroids.append(point)

# populate centroids
for i in range(n_centroids):
    centroid = centroids[i]
    n_points = np.random.randint(10, 30)
    centroids[i]['id'] = i+1+55
    centroids[i]['clusterName'] = "Cluster " + str(i+1)
    centroids[i]['numberOfPlans'] = n_points
    centroids[i]['avgDistrictPlanBoundaryID'] = 4
    points = []
    clusters.append([])
    for j in range(n_points):
        point = {}
        for measure in measures:
            point['units'] = measure[3]
            if(point['units'] == "%"):
                point[measure[0]] = np.random.uniform(centroid[measure[0]]-3, centroid[measure[0]]+3)
                point[measure[0]] = int(point[measure[0]]*100)/100
            else:
                point[measure[0]] = int(np.random.normal(centroid[measure[0]], 3))
            
        clusters[i].append(point)

planID=464
# write centroids
with open('./data/dummy1.json', 'w') as f:
    f.write('[\n')
    for i in range(n_centroids):
        f.write('\t{\n')
        f.write(f'\t\t"clusterId": {centroids[i]["id"]},\n')
        f.write(f'\t\t"clusterName": "Cluster {i+1}",\n')
        f.write(f'\t\t"numberOfPlans": {centroids[i]["numberOfPlans"]},\n')
        f.write(f'\t\t"avgDistrictPlanBoundaryID": {centroids[i]["avgDistrictPlanBoundaryID"]},\n')
        f.write('\t\t"districtPlanIDs":[')
        for plan in range(centroids[i]["numberOfPlans"]):
            if plan == centroids[i]["numberOfPlans"] - 1:
                f.write(f'{planID}],\n')
            else:
                f.write(f'{planID} ,')
            planID += 1
        f.write('\t\t"measureData":{\n')
        for index, measure in enumerate(measures):
            if index == len(measures) - 1:
                f.write(f'\t\t\t"{measure[0]}": {centroids[i][measure[0]]}\n')
                f.write('\t\t\t}\n')
            else:
                f.write(f'\t\t\t"{measure[0]}": {centroids[i][measure[0]]},\n')
        f.write('\t},\n')
    f.write(']\n')


# write clusters
planID=464
with open('./data/dummy_cluster1.json', 'w') as f:
    f.write('[\n')
    for i in range(n_centroids):
        # f.write ('\t[\n')
        for j in range(centroids[i]['numberOfPlans']):
            f.write('\t\t{\n')
            f.write(f'\t\t\t"id": {planID},\n')
            f.write(f'\t\t\t"districtPlanName": "districtPlan{planID}",\n')
            if(np.random.randint(0, 100) < 30):
                f.write(f'\t\t\t"availability": false,\n')
            else:
                f.write(f'\t\t\t"availability": true,\n')
            f.write(f'\t\t\t"boundaryID": 4,\n')
            planID += 1
            f.write('\t\t\t"measureData": {\n')
            length = len(clusters[i][j])
            ival = 0
            for k,v in clusters[i][j].items():
                # check if v is a string
                if k != "units":
                    if(isinstance(v, str)):
                        v = f'"{v}"'
                    if ival == length - 1:
                        f.write(f'\t\t\t\t\t"{k}": {v}\n')
                    else:
                        f.write(f'\t\t\t\t\t"{k}": {v},\n')
                ival += 1
            f.write('\t\t\t}\n')
            f.write('\t\t},\n')
        # f.write('\t],\n')
    f.write(']')
print("total PlanIDs: ", planID)
'''
const clusters = [
    {
        Cluster: "Cluster 1",
        "District average African American population %": 88,
        "Num of District with over 30% Average African American population": 66,
        "Cluster Size": 20,
        clusterId: 0,
    },
    {
        Cluster: "Cluster 2",
        "District average African American population %": 13,
        "Num of District with over 30% Average African American population": 23,
        "Cluster Size": 4,
        clusterId: 1,
    },
    {
        Cluster: "Cluster 3",
        "District average African American population %": 40,
        "Num of District with over 30% Average African American population": 4,
        "Cluster Size": 16,
        clusterId: 2,
    },
    {
        Cluster: "Cluster 4",
        "District average African American population %": 71,
        "Num of District with over 30% Average African American population": 31,
        "Cluster Size": 8,
        clusterId: 3,
    },
    {
        Cluster: "Cluster 5",
        "District average African American population %": 21,
        "Num of District with over 30% Average African American population": 24,
        "Cluster Size": 23,
        clusterId: 4,
    },
];

const cluster = [
    [
        {
            "District average African American population %": 15.73264745937001,
            "Num of District with over 30% Average African American population": 83.35249646459053,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 1,
        },
        {
            "District average African American population %": 69.35612338515108,
            "Num of District with over 30% Average African American population": 70.57852564301533,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 2,
        },
        {
            "District average African American population %": 42.20082783634203,
            "Num of District with over 30% Average African American population": 83.02564634650837,
            "Plan Amount": 1,
            Avaliablity: "Not Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 3,
        },
        {
            "District average African American population %": 44.2389407177032,
            y: 30.79081105735658,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 4,
        },
        {
            "District average African American population %": 35.73264745937001,
            "Num of District with over 30% Average African American population": 53.35249646459053,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 5,
        },
        {
            "District average African American population %": 69.35612338515108,
            "Num of District with over 30% Average African American population": 10.57852564301533,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 6,
        },
        {
            "District average African American population %": 52.20082783634203,
            "Num of District with over 30% Average African American population": 33.02564634650837,
            "Plan Amount": 1,
            Avaliablity: "Not Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 7,
        },
        {
            "District average African American population %": 44.2389407177032,
            "Num of District with over 30% Average African American population": 67.79081105735658,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 8,
        },
        {
            "District average African American population %": 15.73264745937001,
            "Num of District with over 30% Average African American population": 3.35249646459053,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 9,
        },
        {
            "District average African American population %": 69.35612338515108,
            "Num of District with over 30% Average African American population": 70.57852564301533,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 10,
        },
        {
            "District average African American population %": 90.20082783634203,
            "Num of District with over 30% Average African American population": 83.02564634650837,
            "Plan Amount": 1,
            Avaliablity: "Not Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 11,
        },
        {
            "District average African American population %": 44.2389407177032,
            "Num of District with over 30% Average African American population": 5.79081105735658,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 12,
        },
        {
            "District average African American population %": 44.2389407177032,
            "Num of District with over 30% Average African American population": 30.79081105735658,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 13,
        },
        {
            "District average African American population %": 15.73264745937001,
            "Num of District with over 30% Average African American population": 13.35249646459053,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 14,
        },
        {
            "District average African American population %": 69.35612338515108,
            "Num of District with over 30% Average African American population": 30.57852564301533,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 15,
        },
        {
            "District average African American population %": 42.20082783634203,
            "Num of District with over 30% Average African American population": 13.02564634650837,
            "Plan Amount": 1,
            Avaliablity: "Not Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 16,
        },
        {
            "District average African American population %": 44.2389407177032,
            "Num of District with over 30% Average African American population": 30.79081105735658,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 17,
        },
        {
            "District average African American population %": 15.73264745937001,
            "Num of District with over 30% Average African American population": 83.35249646459053,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 18,
        },
        {
            "District average African American population %": 69.35612338515108,
            "Num of District with over 30% Average African American population": 70.57852564301533,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 19,
        },
        {
            "District average African American population %": 42.20082783634203,
            "Num of District with over 30% Average African American population": 83.02564634650837,
            "Plan Amount": 1,
            Avaliablity: "Not Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 20,
        },
    ],
    [
        {
            "District average African American population %": 15.73264745937001,
            "Num of District with over 30% Average African American population": 83.35249646459053,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 21,
        },
        {
            "District average African American population %": 69.35612338515108,
            "Num of District with over 30% Average African American population": 70.57852564301533,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 22,
        },
        {
            "District average African American population %": 42.20082783634203,
            "Num of District with over 30% Average African American population": 83.02564634650837,
            "Plan Amount": 1,
            Avaliablity: "Not Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 23,
        },
        {
            "District average African American population %": 44.2389407177032,
            "Num of District with over 30% Average African American population": 30.79081105735658,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 24,
        },
    ],
    [
        {
            "District average African American population %": 15.73264745937001,
            "Num of District with over 30% Average African American population": 83.35249646459053,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 25,
        },
        {
            "District average African American population %": 69.35612338515108,
            "Num of District with over 30% Average African American population": 70.57852564301533,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 26,
        },
        {
            "District average African American population %": 42.20082783634203,
            "Num of District with over 30% Average African American population": 83.02564634650837,
            "Plan Amount": 1,
            Avaliablity: "Not Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 27,
        },
        {
            "District average African American population %": 44.2389407177032,
            y: 30.79081105735658,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 28,
        },
        {
            "District average African American population %": 35.73264745937001,
            "Num of District with over 30% Average African American population": 53.35249646459053,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 29,
        },
        {
            "District average African American population %": 69.35612338515108,
            "Num of District with over 30% Average African American population": 10.57852564301533,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 30,
        },
        {
            "District average African American population %": 52.20082783634203,
            "Num of District with over 30% Average African American population": 33.02564634650837,
            "Plan Amount": 1,
            Avaliablity: "Not Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 31,
        },
        {
            "District average African American population %": 44.2389407177032,
            "Num of District with over 30% Average African American population": 67.79081105735658,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 32,
        },
        {
            "District average African American population %": 15.73264745937001,
            "Num of District with over 30% Average African American population": 3.35249646459053,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 33,
        },
        {
            "District average African American population %": 69.35612338515108,
            "Num of District with over 30% Average African American population": 70.57852564301533,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 34,
        },
        {
            "District average African American population %": 90.20082783634203,
            "Num of District with over 30% Average African American population": 83.02564634650837,
            "Plan Amount": 1,
            Avaliablity: "Not Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 35,
        },
        {
            "District average African American population %": 44.2389407177032,
            "Num of District with over 30% Average African American population": 5.79081105735658,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 36,
        },
        {
            "District average African American population %": 15.73264745937001,
            "Num of District with over 30% Average African American population": 13.35249646459053,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 37,
        },
        {
            "District average African American population %": 69.35612338515108,
            "Num of District with over 30% Average African American population": 30.57852564301533,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 38,
        },
        {
            "District average African American population %": 42.20082783634203,
            "Num of District with over 30% Average African American population": 13.02564634650837,
            "Plan Amount": 1,
            Avaliablity: "Not Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 39,
        },
        {
            "District average African American population %": 64.2389407177032,
            "Num of District with over 30% Average African American population": 30.79081105735658,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 40,
        },
    ],
    [
        {
            "District average African American population %": 69.35612338515108,
            "Num of District with over 30% Average African American population": 70.57852564301533,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 41,
        },
        {
            "District average African American population %": 90.20082783634203,
            "Num of District with over 30% Average African American population": 83.02564634650837,
            "Plan Amount": 1,
            Avaliablity: "Not Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 42,
        },
        {
            "District average African American population %": 44.2389407177032,
            "Num of District with over 30% Average African American population": 5.79081105735658,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 43,
        },
        {
            "District average African American population %": 15.73264745937001,
            "Num of District with over 30% Average African American population": 13.35249646459053,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 44,
        },
        {
            "District average African American population %": 69.35612338515108,
            "Num of District with over 30% Average African American population": 30.57852564301533,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 45,
        },
        {
            "District average African American population %": 42.20082783634203,
            "Num of District with over 30% Average African American population": 13.02564634650837,
            "Plan Amount": 1,
            Avaliablity: "Not Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 45,
        },
        {
            "District average African American population %": 44.2389407177032,
            "Num of District with over 30% Average African American population": 30.79081105735658,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 47,
        },
        {
            "District average African American population %": 15.73264745937001,
            "Num of District with over 30% Average African American population": 83.35249646459053,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 48,
        },
    ],
    [
        {
            "District average African American population %": 15.73264745937001,
            "Num of District with over 30% Average African American population": 83.35249646459053,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 49,
        },
        {
            "District average African American population %": 69.35612338515108,
            "Num of District with over 30% Average African American population": 70.57852564301533,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 50,
        },
        {
            "District average African American population %": 42.20082783634203,
            "Num of District with over 30% Average African American population": 83.02564634650837,
            "Plan Amount": 1,
            Avaliablity: "Not Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 51,
        },
        {
            "District average African American population %": 44.2389407177032,
            y: 30.79081105735658,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 52,
        },
        {
            "District average African American population %": 35.73264745937001,
            "Num of District with over 30% Average African American population": 53.35249646459053,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 53,
        },
        {
            "District average African American population %": 69.35612338515108,
            "Num of District with over 30% Average African American population": 10.57852564301533,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 54,
        },
        {
            "District average African American population %": 52.20082783634203,
            "Num of District with over 30% Average African American population": 33.02564634650837,
            "Plan Amount": 1,
            Avaliablity: "Not Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 55,
        },
        {
            "District average African American population %": 44.2389407177032,
            "Num of District with over 30% Average African American population": 67.79081105735658,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 56,
        },
        {
            "District average African American population %": 15.73264745937001,
            "Num of District with over 30% Average African American population": 3.35249646459053,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 57,
        },
        {
            "District average African American population %": 69.35612338515108,
            "Num of District with over 30% Average African American population": 70.57852564301533,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 58,
        },
        {
            "District average African American population %": 90.20082783634203,
            "Num of District with over 30% Average African American population": 83.02564634650837,
            "Plan Amount": 1,
            Avaliablity: "Not Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 59,
        },
        {
            "District average African American population %": 44.2389407177032,
            "Num of District with over 30% Average African American population": 5.79081105735658,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 60,
        },
        {
            "District average African American population %": 15.73264745937001,
            "Num of District with over 30% Average African American population": 13.35249646459053,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 61,
        },
        {
            "District average African American population %": 69.35612338515108,
            "Num of District with over 30% Average African American population": 30.57852564301533,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 62,
        },
        {
            "District average African American population %": 42.20082783634203,
            "Num of District with over 30% Average African American population": 13.02564634650837,
            "Plan Amount": 1,
            Avaliablity: "Not Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 63,
        },
        {
            "District average African American population %": 44.2389407177032,
            "Num of District with over 30% Average African American population": 30.79081105735658,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 64,
        },
        {
            "District average African American population %": 15.73264745937001,
            "Num of District with over 30% Average African American population": 83.35249646459053,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 65,
        },
        {
            "District average African American population %": 69.35612338515108,
            "Num of District with over 30% Average African American population": 70.57852564301533,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 66,
        },
        {
            "District average African American population %": 42.20082783634203,
            "Num of District with over 30% Average African American population": 83.02564634650837,
            "Plan Amount": 1,
            Avaliablity: "Not Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 67,
        },
        {
            "District average African American population %": 44.2389407177032,
            "Num of District with over 30% Average African American population": 30.79081105735658,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 68,
        },
        {
            "District average African American population %": 19.35612338515108,
            "Num of District with over 30% Average African American population": 70.57852564301533,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 69,
        },
        {
            "District average African American population %": 42.20082783634203,
            "Num of District with over 30% Average African American population": 31.02564634650837,
            "Plan Amount": 1,
            Avaliablity: "Not Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 70,
        },
        {
            "District average African American population %": 44.2389407177032,
            "Num of District with over 30% Average African American population": 30.79081105735658,
            "Plan Amount": 1,
            Avaliablity: "Available",
            fileloc: "../data/Precinct_Merged.geojson",
            distPlanId: 71,
        },
    ],
];

'''