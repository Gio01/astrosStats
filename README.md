TODO:
have the home page be the current stats.

each player will have a link that will take them to each players own page 
which would then give us more info, with some graphs to show their stats over time


------
Each time i was making a refresh i was making api calls which was going to take forever 
so instead i have created a simple sqlite table that holds the roster of players from the 
astros and then based on that I can then at least get rid of the roster call to get the list 
of players.
- next: I will do the same to create a table for the player stats so that I can use the data i have!
However at the very least by having my own basic table i do not need to keep on making so many api 
calls get the data that i want as that will create a lot of overhang and cause for latency issues 
when trying to access the page!


------
References:
- I used Kodestan's css for the visual aesthetic of the site: https://kodestan.com/ 
