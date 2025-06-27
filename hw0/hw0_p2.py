def load_movie_data(file_path):
    with open(file_path, "r" ) as file:
        lines = file.readlines()  # Read all lines in the file
        # Split the first line to get the headers (column names)
        headers = lines[0].strip().split(',')
        # Process each row after the headers
        data = []               
        for line in lines[1:]:
            values = line.strip().split(',')
            movie = {headers[i]: values[i] for i in range(len(headers))}  # Create a dictionary for each movie
            data.append(movie)
    return data


def top_3_movies_2016(data):
    movies_2016 = [movie for movie in data if movie['Year'] == '2016']    # Filter movies by year 2016
    sorted_movies = sorted(movies_2016, key=lambda x: float(x['Rating']), reverse=True)     # Sort by Rating
    top3 = sorted_movies[:3]    # Atop three
    top3title = []              # Show title
    for i in range(3):
        top3title.append(top3[i]['Title'])
    return top3title


#直接把revenue當成每個演員的收入做計算（每個演員都收了相同的金額）
def actor_with_highest_avg_revenue(data):
    actor_revenue = {}
    for movie in data:
        actors = movie['Actors'].split('|')
        revenue = float(movie['Revenue (Millions)']) if movie['Revenue (Millions)'] else 0
        for actor in actors:
            if actor in actor_revenue:
                actor_revenue[actor].append(revenue)
            else:
                actor_revenue[actor] = [revenue]
        avg_revenue = {actor: sum(revenues) / len(revenues) for actor, revenues in actor_revenue.items() if len(revenues) > 0}
    max_avg_revenue = max(avg_revenue.values())
    highest_avg_actors = [actor for actor, avg in avg_revenue.items() if avg == max_avg_revenue]
    return highest_avg_actors 


def avg_rating_emma_watson(data):
    emma_movies = [movie for movie in data if 'Emma Watson' in movie['Actors']]
    ratings = [float(movie['Rating']) for movie in emma_movies]
    return sum(ratings) / len(ratings)


def top3_directors_with_most_actors(data):
    director_actors = {}
    for movie in data:
        director = movie['Director']
        actors = movie['Actors'].split('|') 
        if director in director_actors:
            director_actors[director].update(actors)
        else:
            director_actors[director] = set(actors)  # Initialize with a set of actors
    # Create a list of directors sorted by the number of unique actors, in descending order
    sorted_directors = sorted(director_actors.items(), key=lambda item: len(item[1]), reverse=True)
    # Get the top 3 directors with the most unique actors
    top_3 = sorted_directors[:3]
    # Return the top 3 directors and their actor counts
    return [(director) for director, actors in top_3]


def top2_actor_in_genres(data):
    actor_genres = {}
    for movie in data:
        actors = movie['Actors'].split('|') 
        genres = movie['Genre'].split('|') 
        # For each actor, add the genres of the movie to their genre set
        for actor in actors:
            if actor in actor_genres:
                actor_genres[actor].update(genres)  # Update with new genres
            else:
                actor_genres[actor] = set(genres)   # Initialize with a set of genres
    sorted_actors = sorted(actor_genres.items(), key=lambda item: len(item[1]), reverse=True)
    # Find the number of genres for the first and second highest actors
    if len(sorted_actors) > 0:
        max_genre_count = len(sorted_actors[0][1])  # The most genres
    if len(sorted_actors) > 1:
        second_max_genre_count = len(sorted_actors[1][1])  # The second most genres
    else:
        second_max_genre_count = 0  # If there's only one actor, there's no second max
    # Collect all actors with the max and second max genre count
    top_actors = [actor for actor, genres in sorted_actors if len(genres) == max_genre_count or len(genres) == second_max_genre_count]
    # Return the top actors and their genre counts
    return [(actor) for actor in top_actors]


def largest_gap(data):
    actor_years = {}
    for movie in data:
        actors = movie['Actors'].split('|')
        year = int(movie['Year'])
        for actor in actors:
            if actor in actor_years:
                actor_years[actor].append(year)
            else:
                actor_years[actor] = [year]
    
    max_gap = {actor: max(years) - min(years) for actor, years in actor_years.items()}
    sorted_actors = sorted(max_gap.items(), key=lambda x: x[1], reverse=True)
    if len(sorted_actors) >= 3:
        third_highest_gap = sorted_actors[2][1]
    else:
        third_highest_gap = sorted_actors[-1][1]  # If fewer than 3 actors, use the last actor's gap
    # Collect all actors whose gap is equal to or greater than the third-highest gap
    result = [(actor) for actor, gap in sorted_actors if gap >= third_highest_gap]  
    return result


def actors_collaborating_with_johnny_depp(data):
    # Step 1: Build a collaboration graph where each actor is connected to actors they've worked with
    collaborations = {}   
    for movie in data:
        actors = movie['Actors'].split('|')  # Assuming actors are separated by '|'
        for actor in actors:
            if actor not in collaborations:
                collaborations[actor] = set()
            collaborations[actor].update(actors)  # Add all actors from the same movie as collaborators
            collaborations[actor].remove(actor)  # Remove self-collaboration
    # Step 2: Use BFS or DFS to find all actors who are connected to Johnny Depp
    def find_collaborators(start_actor):
        visited = set()  # Keep track of visited actors
        to_visit = [start_actor]  # Start with Johnny Depp
        
        while to_visit:
            current_actor = to_visit.pop(0)
            if current_actor not in visited:
                visited.add(current_actor)
                # Add all collaborators of the current actor to the list of actors to visit
                for collaborator in collaborations.get(current_actor, []):
                    if collaborator not in visited:
                        to_visit.append(collaborator)        
        return visited
    
    # Step 3: Get all collaborators of Johnny Depp, excluding Johnny Depp himself
    collaborators_of_johnny_depp = find_collaborators('Johnny Depp') - {'Johnny Depp'}
    #print(len(collaborators_of_johnny_depp))
    return collaborators_of_johnny_depp




file_path = "/Users/chiao/Desktop/IMDB-Movie-Data.csv"
data = load_movie_data(file_path)
print('(1)', top_3_movies_2016(data))
print('(2)', actor_with_highest_avg_revenue(data))
print('(3)', avg_rating_emma_watson(data))
print('(4)', top3_directors_with_most_actors(data))
print('(5)', top2_actor_in_genres(data))
print('(6)', largest_gap(data))
print('(7)', actors_collaborating_with_johnny_depp(data))


