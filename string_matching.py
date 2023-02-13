def match_string(string_super,string_sub):
    i = 0
    j = 0

    best_matches = []

    while i < len(string_super):
        current_score = 0

        while j < len(string_sub):
            if i + j > len(string_super) - 1:
                j = 0
                best_matches.append([string_sub[:j],j / len(string_sub)])

                break

            elif string_super[i + j] == string_sub[j]:
                current_score += 1
        
            j += 1
        
        best_matches.append([string_sub[:j],current_score / len(string_sub)])
        j = 0

        i += 1

    return max(best_matches,key = lambda x:x[1])
