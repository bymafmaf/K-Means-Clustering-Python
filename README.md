This python script takes followings as input:

1. dataFilename: corresponds to the yelp3.csv dataset that should be clustered by k-means algorithm.

2. K: the value of k to use when clustering.

3. clustering option: takes one of the following five values, 1 (use the four original attributs for clustering, which corresponds to Q2(i)), 2 (apply a log transform to reviewCount and checkins, which corresponds to Q2(ii)), 3 (use the standardized four attributes for clustering, which corresponds to Q2(iii), 4 (use the four original attributes and Manhattan distance for clustering, which corresponds to Q2(iv)), and 5 (use 3% random sample of data for clustering, which corresponds to Q2(v)).

4. plot option: takes one of the following three values, no (no plot), 1 (plot the clusters with their centroids using latitude and longitude), and 2 (plot the clusters with their centroids using reviewCount and checkins).
Four main attributes are following: `lattitude`, `longitude`, `reviewCount` and `checkins`

Example run for file named yelp3.csv, with k value of 3 using four original attributes and plotting clusters for both reviewCount and checkins

`kmeans.py yelp3.csv 3 1 2`

*Note: Script has many code duplications. It's because I was trying to submit it before the deadline.*