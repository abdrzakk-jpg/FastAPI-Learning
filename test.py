
scores = [
    {
    "name":"omar",
    "score":90
    },    
    {
    "name":"ali",
    "score":1
    },
    {
    "name":"zamer",
    "score":30
    }
]
scores.sort(key=lambda player: player["score"], reverse=True)
print(scores)