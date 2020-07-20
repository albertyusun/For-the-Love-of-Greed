# Initialize empty list of cosine similarities
# For each csv:
# Randomly select documents from csv.
#       Use row index as key. Get number of rows (pd command)
#       Create list of indices, np.random.choice to get set of indices. range(n)
#       np.asarray() to convert list to np vector/array.
#       Retrieve texts corresponding to randomly selected indices. Convert to list of texts
#           For each index, grab the text at that row. Append to list.
#       Tokenize the list of texts
# Create 300 dimensional word embedding of tokenized sample.
#       Create keyed vectors file also (automatic with load_models)
# Extract desired statistics
#       Get cosine similarity between 'consume' and 'luxury' and for 'consume' and 'disease'
#       Add cosine similarity to a list
#       Add list to csv
# Delete word embedding. os.remove()
#


