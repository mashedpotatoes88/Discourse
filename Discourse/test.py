results = [(1, "eric", 1, 1, 0)]
for result in results:
    for i in range(len(result)):
        if type(result[i]) == int:
            result[i] = str(result[i])
        else:
            continue
print(results)