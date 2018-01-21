

def ranking(scores):
    """
    scores is a list of the score such as:['33', '44', '55']
    Return the respective ranks of the score: [3, 2, 1]
    """
    result = []
    sorted = list(scores)
    sorted.sort(reverse=True)

    [result.append(sorted.index(s)+1) for s in scores]
    return result
