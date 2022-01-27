"""
Name: movie_recommendations.py
Date: 
Author: 
Description: 
"""

import math
import csv
from scipy.special.orthogonal import jacobi
from scipy.stats import pearsonr

class BadInputError(Exception):
    pass

class Movie_Recommendations:
    # Constructor

    def __init__(self, movie_filename, training_ratings_filename):
        """
        Initializes the Movie_Recommendations object from 
        the files containing movie names and training ratings.  
        The following instance variables should be initialized:
        self.movie_dict - A dictionary that maps a movie id to
               a movie objects (objects the class Movie)
        self.user_dict - A dictionary that maps user id's to a 
               a dictionary that maps a movie id to the rating
               that the user gave to the movie.    
        """
        # Open files
        self.movie_file = open(movie_filename, encoding = "utf-8")
        self.ratings_file = open(training_ratings_filename)

        # movie_dict is a dictionary for movie objects with the keys being the ids for the movies
        # user_dict is a dictionary for all the movies that a user has rated with the keys being the user ids
        self.movie_dict = dict()
        self.user_dict = dict()

        self.movie_csv_reader = csv.reader(self.movie_file, delimiter = ',', quotechar = '"')
        self.movie_file.readline()

        self.rating_csv_reader = csv.reader(self.ratings_file, delimiter = ',', quotechar = '"')
        self.ratings_file.readline()

        # go through the movie file and add the movie to the movie_dict
        for line in self.movie_csv_reader:
            self.movie_dict[int(line[0])] = Movie(int(line[0]), line[1])

        # rating_dict contains movies and their ratings for the specific user
        # temp_user_id is used to help iterate through the ratings file
        self.rating_dict = dict()
        self.temp_user_id = 1

        # user_movie_dict has the users as its keys and the values are the list of movies the user has rated
        self.user_movie_dict = dict()
        self.movie_list = list()
        
        # iterate through the ratings file and if the temp_user_id doesn't match the user id in the current line of the file,
        # set the temp_user_id to id in the current line and assign the rating_dict to the previous user id in user_dict
        # reset rating_dict and movie_list, otherwise continue adding ratings to rating_dict for that user and adding movies to
        # the movie list
        for line in self.rating_csv_reader:
            self.user_movie_dict[self.temp_user_id] = self.movie_list
            if self.temp_user_id != int(line[0]):
                self.user_dict[self.temp_user_id] = self.rating_dict
                self.rating_dict = dict()
                self.movie_list = list()
                self.temp_user_id += 1
            
            self.rating_dict[int(line[1])] = float(line[2])
            self.movie_list.append(int(line[1]))

        # add rating_dict to the last user
        self.user_dict[self.temp_user_id] = self.rating_dict

        # this is a list of users who have rated a particular movie
        self.user_list = list()

        # iterate through the dictionary of movies and check if a user has seen that particular movie; if so, add that user to the user list
        # add user_list to the user list for the movie object in movie_dict and reset the user list for the next movie
        for key in self.movie_dict.keys():
            for users in self.user_movie_dict:
                if key in self.user_movie_dict[users] and users not in self.user_list:
                    self.user_list.append(users)
            self.movie_dict[key].users = self.user_list
            self.user_list = list()

    def predict_rating(self, user_id, movie_id):
        """
        Returns the predicted rating that user_id will give to the
        movie whose id is movie_id.
        If user_id has already rated movie_id, return
        that rating.
        If either user_id or movie_id is not in the database,
        then BadInputError is raised.
        """
        sim_sum = 0
        sum = 0
        for other_movie in self.movie_dict[movie_id].similarities:
            try:
                if other_movie not in self.user_dict[user_id]:
                    sum = sum + (self.movie_dict[movie_id].similarities[other_movie] * self.user_dict[user_id][other_movie])
                    sim_sum = sim_sum + self.movie_dict[movie_id].similarities[other_movie]
                else:
                    return self.user_dict[user_id][movie_id]
            except BadInputError:
                raise BadInputError
        if sim_sum == 0:
            return 2.5
        predicted_rating = sum/sim_sum
        return predicted_rating

    def predict_ratings(self, test_ratings_filename):
        """
        Returns a list of tuples, one tuple for each rating in the
        test ratings file.
        The tuple should contain
        (user id, movie title, predicted rating, actual rating)
        """
        # open file and csv reader
        f = open(test_ratings_filename, 'r')
        f.readline()
        rating_list = []
        for line in f:
            split = line.split() 
            # append tuple to list
            rating_list.append((split[0],split[1], self.predict_rating(split[0],split[1]), split[2]))
        f.close()
        return rating_list


    def correlation(self, predicted_ratings, actual_ratings):
        """
        Returns the correlation between the values in the list predicted_ratings
        and the list actual_ratings.  The lengths of predicted_ratings and
        actual_ratings must be the same.
        """
        return pearsonr(predicted_ratings, actual_ratings)[0]
        
class Movie: 
    """
    Represents a movie from the movie database.
    """
    def __init__(self, id, title):
        """ 
        Constructor.
        Initializes the following instances variables.  You
        must use exactly the same names for your instance 
        variables.  (For testing purposes.)
        id: the id of the movie
        title: the title of the movie
        users: list of the id's of the users who have
            rated this movie.  Initially, this is
            an empty list, but will be filled in
            as the training ratings file is read.
        similarities: a dictionary where the key is the
            id of another movie, and the value is the similarity
            between the "self" movie and the movie with that id.
            This dictionary is initially empty.  It is filled
            in "on demand", as the file containing test ratings
            is read, and ratings predictions are made.
        """
        # users list is a list containing the users who have rated this specific movie
        # similarities is a dictionary whose keys are other movies and the values are the similarities between the other movie and this specific movie
        self.id = id
        self.title = title
        self.users = []
        self.similarities = dict()
    
    def __str__(self):
        """
        Returns string representation of the movie object.
        Handy for debugging.
        """
        
        return str(self.id) + ", " + str(self.title) 

    def __repr__(self):
        """
        Returns string representation of the movie object.
        """

        #print(str(self.id) + ", " + str(self.title) + ", " + self.users + ", " + self.similarities)
        return str(self.id) + ", " + str(self.title) + ", " + self.users + ", " + self.similarities #id, title, list of users, and the similarity dictionary

    def get_similarity(self, other_movie_id, movie_dict, user_dict):
        """ 
        Returns the similarity between the movie that 
        called the method (self), and another movie whose
        id is other_movie_id.  (Uses movie_dict and user_dict)
        If the similarity has already been computed, return it.
        If not, compute the similarity (using the compute_similarity
        method), and store it in both
        the "self" movie object, and the other_movie_id movie object.
        Then return that computed similarity.
        If other_movie_id is not valid, raise BadInputError exception.
        """
        # check if the movie_id corresponds to an actual movie in the movie list/csv file
        try:
            if other_movie_id not in movie_dict:
                raise BadInputError

            # check to see if other movie's id is a key in the similarities dictionary; if so use the value that is already in the dictionary
            # same thing for the id of the self movie
            if other_movie_id in self.similarities and self.id in movie_dict[other_movie_id].similarities:
                return self.similarities[other_movie_id]
            else:
                # compute the similarity for two movies if there is no value in the similarity dictionary for both the movies
                return self.compute_similarity(other_movie_id, movie_dict, user_dict)
        except BadInputError:
            pass

    def compute_similarity(self, other_movie_id, movie_dict, user_dict):
        """ 
        Computes and returns the similarity between the movie that 
        called the method (self), and another movie whose
        id is other_movie_id. (Uses movie_dict and user_dict)
        """
        
        self.avg_diff = 0
        count = 0

        # count increases when user has rated the self.id movie and other_movie_id movie
        # and add difference between self.id rating and other_movie_id rating to avg_diff
        for user in movie_dict[self.id].users:
            if user in movie_dict[other_movie_id].users:
                self.avg_diff = self.avg_diff + abs(user_dict[user][self.id] - user_dict[user][other_movie_id])
                count += 1

        # count is 0 when no user has rated both movies (self.id and other_movie_id movies), return 0 for similarity
        if count == 0:
            return 0

        # quantity from for loop divided by the number of users that rated both movies
        self.avg_diff = self.avg_diff / count

        # store the similarity value in the similarity dictionary of both the self and other movie and return similarity value
        self.similarities[other_movie_id] = 1 - (self.avg_diff / 4.5)
        movie_dict[other_movie_id].similarities[self.id] = 1 - (self.avg_diff / 4.5)
        return self.similarities[other_movie_id]

if __name__ == "__main__":
    # Create movie recommendations object.
    movie_recs = Movie_Recommendations("dummy_movies.csv", "dummy_test_ratings.csv")

    # Predict ratings for user/movie combinations
    rating_predictions = movie_recs.predict_ratings("test_ratings.csv")
    print("Rating predictions: ")
    for prediction in rating_predictions:
        print(prediction)
    predicted = [rating[2] for rating in rating_predictions]
    actual = [rating[3] for rating in rating_predictions]
    correlation = movie_recs.correlation(predicted, actual)
    print(f"Correlation: {correlation}")