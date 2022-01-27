"""
Module: earthquake_clusters

A program to create and visualize clusters of earthquakes.

Authors:
1) Garrett - gcarney@sandiego.edu
2) Natalie - natalienguyen@sandiego.edu
"""

import sys
import math
import matplotlib.pyplot as pp
import imageio
import csv


def euclidean_distance(point1, point2):
    """
    Returns the euclidean distance between point1 and point2.
    point1 and point2 are tuples of length 2.
    """
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    result = ((((x2 - x1 )**2) + ((y2-y1)**2) )**0.5)
    return result


def get_close_points(p, epsilon, data):
    """
    Returns a list of all the points in the dataset data 
    that are the within epsilon of p.
	"""
    points = list()
    for point in data:
        distance = euclidean_distance(p, point)
        if distance < epsilon and point != p:
            points.append(point)
    return points

def add_to_cluster(points, cluster_num, data, epsilon, min_pts):
    """
    Loops through given points to see if they can be added to the cluster wiht number cluster_num. If the point is 
    unassigned or an outlier, it can be added to the new cluster. 
    """
    for point in points: #iterates to points list
        if data[point] == None or data[point] == -1:
            data[point] = cluster_num #adds point to cluster if it is unassigned or an outlier
            neighbors = get_close_points(point, epsilon, data) #list of neighbors
            if len(neighbors) >= min_pts:
                add_to_cluster(neighbors, cluster_num, data, epsilon, min_pts) #repeats process for each neighbor

       
def dbscan(data, epsilon, min_pts):
    """
    Puts points into clusters and returns the number of clusters created. 
    """
    cluster_num = 0
    for p in data:
        if data[p] == -1 or data[p] != None:
            pass
        else:
            neighbors = get_close_points(p, epsilon, data)
            if len(neighbors) < min_pts:
                data[p] = -1
            else:
                data[p] = cluster_num
                add_to_cluster(neighbors, cluster_num, data, epsilon, min_pts)
                cluster_num +=1
    return cluster_num


def get_clusters(data, num_clusters):
    """
    Gets a list of all the clusters from data and returns this list of clusters.
    """
    clusters = []
    for i in range(num_clusters):
        clusters.append([])
    for point in data:
        if data[point]!=-1:
            clusters[data[point]].append(point)
    return clusters


def plot_clusters(clusters):
    """
    Creates a scatter plot for each cluster within clusters.
    Gets all the x cordinates and y cordinates to plug in
    """

    for cluster in clusters:
        x_cords = [x for x,y in cluster]
        y_cords = [y for x,y in cluster]
        pp.scatter(x_cords, y_cords)
    pp.show()


def get_eq_locations(filename):
    """
    Reads the file and returns the latitude and longitude (an x,y point)
    Returns a list of points
    """

    f = open(filename)
    csv_reader = csv.reader(f, delimiter = ",", quotechar = '"')
    next(csv_reader)
    locations = []
    for line in csv_reader:
        lat = float(line[1])
        long = float(line[2])
        locations.append((long,lat))
    return locations

    

def initialize_database(locations):
    """
    Creates a dictionary of points and initializes their values to None so they can be edited later. 
    The values will end up being cluster numbers.
    """
    database_dict = {}
    for point in locations:
        database_dict[point] = None
    return database_dict


def plot_earthquakes(filename):
    """
    Creates clusters of earthquakes from the data contained in filename and
    displays them on a world map.
    Utilizes all the earlier written functions to get the data and present is on the world map.
    """

    print("Creating and visualizing clusters from file: %s" % filename)

    # To Do: Use the functions you wrote above to complete the following 5
    # steps. Delete this comment when you are done.

    # Step 1: Gets a list of all of the earthquake locations.
    # Step 2: Initializes the data dictionary.
    # Step 3: Use dbscan to create clusters.
    # Step 4: Get the list of created clusters.
    # Step 5: Plot the clusters.

    # Set the image background to be a world-map
    # Don't change anything after this point.
    epsilon = 2.0
    min_points = 4
    
    img = imageio.imread("world-map-full.jpg")
    pp.imshow(img, zorder=0, extent=[-180, 180, -90, 90])
    pp.axis('off')
    

    locations = get_eq_locations(filename)
    data = initialize_database(locations)
    clusters = dbscan(data, epsilon, min_points)
    clusters_list = get_clusters(data, clusters)
    plot_clusters(clusters_list)
   

if __name__ == "__main__":
    # Choose the input file
    choice = input("Enter 1 (for eq_day.csv) or 2 (for eq_week.csv): ")

    # Create the clusters and plot the data.
    if choice == '1':
        plot_earthquakes("eq_day.csv")
    elif choice == '2':
        plot_earthquakes("eq_week.csv")
    else:
        print("Invalid choice")




