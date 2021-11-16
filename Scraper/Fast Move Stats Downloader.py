import requests,csv

pokemon_data=[] #Init Pokémon data array.

with open('Spreadsheet.csv', 'r') as csvfile: #Open the spreadsheet created by the previous scraper.
 csvreader = csv.reader(csvfile, delimiter=',', quotechar='|') #Read the csv file.
 for row in csvreader:
    pokemon_data.append(row) #Write each row into the array of Pokémon data.
del pokemon_data[0]

fast_moves=[] #Init fast moves list.
for pokemon in pokemon_data: #Loop through each Pokémon's stats.
    fast_moves_this_pokemon=pokemon[3].split("#") #Extract a list of this Pokémon's potential fast moves.
    for move in fast_moves_this_pokemon: #Loop through each move in the generated list.
        if not move in fast_moves: #If this move is not in the fast moves list. 
            fast_moves.append(move) #Add it to the fast moves list.
    
move_data={} #Init move information array.
for move in fast_moves: #Loop through each Fast Move.
    url="https://pokemongo.gamepress.gg/pokemon-move/"+move.replace(" ","-") #Create link to check.
    
    f = requests.get(url).text #Obtain HTML from page.
    f_lines=f.splitlines() #Split HTML into lines.
    
    for a in range(0,len(f_lines)): #Loop through each line of HTML.
        if 'Move Type</th><td><span class="' in f_lines[a]: #If this line has the Move Type information.
            move_type=f_lines[a].split('Move Type</th><td><span class="')[1].split("-")[0] #Extract the Move Type.
        if '<tr><th>Base Power</th><td>' in f_lines[a]: #If this line has the Base Power information.
            base_power=f_lines[a+1].split('>')[1].split("<")[0] #Extract the Base Power.
        if '<tr><th>Energy Delta</th><td>' in f_lines[a]: #If this line has the Energy Delta information.
            energy_delta=f_lines[a+1].split('>')[1].split("<")[0] #Extract the Energy Delta.
        if '<tr><th>Move Cooldown</th><td>' in f_lines[a]: #If this line has the Move Cooldown information.
            cooldown=f_lines[a+1].split('>')[1].split("<")[0] #Extract the Move Cooldown.

    move_data[move]=[move_type,base_power,energy_delta,cooldown] #Record data into array.

with open('Fast Move Data.csv', 'w', newline='') as csvfile:
   csvwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL) #Init csv writer.
   for i in range(0,len(list(move_data))): #Loop through each move in the array.
      csvwriter.writerow([list(move_data)[i]]+move_data[list(move_data)[i]]) #Record in the csv file.
