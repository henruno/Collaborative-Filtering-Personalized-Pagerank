# Collaborative filtering (item-item)
___

![alt text](https://miro.medium.com/max/1200/0*YpFJOPIoUdGZLWV9.jpg)

Item-Item collaborative filtering implementation and creation of a recommendation/prediction method using the **Topic-Specific-PageRank** method. Moreover, evaluation of the the quality of the provided method is performed, by using the **R-Precision** metric. The goal is to design and implement a recommendation method that is able to predict new user-item interactions by considering the ones provided by the bipartite graph. 

For achieving the goal, we work on the Projected-Item-Item-Graph associated to the original bipartite graph (see the data). The Projected-Item-Item-Graph is an undirected-weighted graph which the set of nodes is the set of items in the original bipartite graph, and where two items are connected by an edge if there is at least one user that interacted with both items. The weight of an edge connecting two items is equal to the number of users that interacted with both items.

To recommend new items to a user we use the Topic-Specific-PageRank algorithm considering as “topic” all items connected to the user in the original bipartite-graph, using a dumping_factor of 0.1 .

***

# Personalized Pagerank

In the second part of the project we want to recommend items to users having only data about User-Item interactions exactly as in the previous part, with the only exception that we don't construct the Projected-Item-Item graph because we have only a little portion of the original Bipartite-Graph, even if we have a complete information for each user.

Moreover, instead of the Projected-Item-Item graph, we compute the **Personalized-PageRank** vector associated to each item in the complete Projected-Item-Item graph. 

By using the information about the user-item interactions and the Personalized-PageRank vectors, we are able to recommend new items to a user. The output is the same that you would obtain if we have ran the Topic-Sensitive-PageRank algorithm on the Projected-Item-Item-Graph.

***

# Files

* ***part1.py***: python module with exemplary executable main. Responsible of the creation of the first recommandation method.

* ***part2.py***: python module with exemplary executable main. Responsible of the creation of the second recommandation method.

* ***User_Item_BIPARTITE_GRAPH___UserID__ItemID.tsv***: tsv file that stores a bipartite graph representing the User-Item interactions: each line in the file represents an edge, of the bipartite graph, that connects a user (first column) with an item (second column).

* ***Ground_Truth___UserID__ItemID.tsv***: Ground truth file used to test the quality of the recommendation/prediction method.

* ***Base_Set___UserID__ItemID__PART_2_2.tsv***: User-item interaction tsv file.

* ***ItemID__PersonalizedPageRank_Vector.tsv***: each line is related to a single item_id and contains the item_id itself, that is stored in the first column, and the Personalized-Pagerank-Vector associated to it, in the second column, represented as a list of couples (item_id, PersonalizedPageRankValue).

* ***Ground_Truth___UserID__ItemID__PART_2_2.tsv***: Ground truth file used to test the quality of the recommendation/prediction method for the second part.
