import csv

def generate_declare_and_regex_function(directlyFollowSet):
    print(f"Inside generate_declare_and_regex_function and length of directlyFollowSet: ",len(directlyFollowSet))
    firstElementMatching=set()
    secondElementMatching=set()
    soloTuple=set()
    for tuple in directlyFollowSet:
        findSimilarFirstElement = {t[1] for t in directlyFollowSet if t[0] == tuple[0]}
        if len(findSimilarFirstElement) >1:
            firstElementMatching.add((tuple[0], frozenset(findSimilarFirstElement)))
        else:
            findSimilarSecondElement = {t[0] for t in directlyFollowSet if t[1] == tuple[1]}
            if len(findSimilarSecondElement)>1:
                secondElementMatching.add((frozenset(findSimilarSecondElement),tuple[1]))
            else:
                soloTuple.add(tuple)
    declarativeConstraints=[]
    regularExpressions=[]
    # Regex for AlternateResponse(A,B): [ˆA]*(A[ˆA]*B[ˆA]*)* as cited here [1].
    # 1. De Smedt, J., Vanden Broucke, S., De Weerdt, J., & Vanthienen, J. (2015). A full R/I-net construct lexicon for declare constraints. Available at SSRN 2572869. 
    #print("firstElementMatching: ",len(firstElementMatching))
    for value in firstElementMatching:
        formatted_elements = ", ".join(value[1])  # Convert frozenset to a comma-separated string
        formatted_elements_regex = "| ".join(value[1])  # Convert frozenset to a OR string
        constraint=f"AlternateResponse({value[0]}, {{{formatted_elements}}})"
        declarativeConstraints.append(constraint)
        regex="[ˆ"+value[0]+"]*("+value[0]+"[ˆ"+value[0]+"]*("+formatted_elements_regex+")[ˆ"+value[0]+"]*)*"
        regularExpressions.append(regex)
    #print("secondElementMatching: ",len(secondElementMatching))
    for value in secondElementMatching:
        formatted_elements = ", ".join(value[0])  # Convert frozenset to a comma-separated string
        formatted_elements_regex = "|".join(value[0])  # Convert frozenset to a OR string
        constraint=f"AlternateResponse({{{formatted_elements}}},{value[1]})"
        declarativeConstraints.append(constraint)
        regex="[ˆ("+formatted_elements_regex+")]*(("+formatted_elements_regex+")[ˆ("+formatted_elements_regex+")]*"+value[1]+"[ˆ("+formatted_elements_regex+")]*)*"
        regularExpressions.append(regex)
    #print("soloTuple: ",len(soloTuple))
    for value in soloTuple:
        constraint=f"AlternateResponse({value})"
        regex="[ˆ"+value[0]+"]*("+value[0]+"[ˆ"+value[0]+"]*("+value[1]+")[ˆ"+value[0]+"]*)*"
        regularExpressions.append(regex)
    
    # Save declarativeConstraints and regularExpressions to a CSV file
    with open("output\\translated_resulting_df_relations.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Declarative Constraints", "Regular Expressions"])  # Header row

        # Write rows for each constraint and regex
        for constraint, regex in zip(declarativeConstraints, regularExpressions):
            writer.writerow([constraint, regex])

    print("Declarative Constraints and Regular Expressions saved to 'output\\translated_resulting_df_relations.csv'")

    