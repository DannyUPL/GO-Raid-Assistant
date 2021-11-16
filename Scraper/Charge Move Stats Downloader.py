import requests,csv

pokemon_data=[] #Init Pokémon data array.

with open('Spreadsheet.csv', 'r') as csvfile: #Open the spreadsheet created by the previous scraper.
 csvreader = csv.reader(csvfile, delimiter=',', quotechar='|') #Read the csv file.
 for row in csvreader:
    pokemon_data.append(row) #Write each row into the array of Pokémon data.
del pokemon_data[0] #Remove headings.

charge_moves=[] #Init charged moves list.
for pokemon in pokemon_data: #Loop through each Pokémon's stats.
    charge_moves_this_pokemon=pokemon[2].split("#") #Extract a list of this Pokémon's potential charged moves.
    for move in charge_moves_this_pokemon: #Loop through each move in the generated list.
        if not move in charge_moves: #If this move is not in the charged moves list. 
            charge_moves.append(move) #Add it to the charged moves list.
    
move_data={} #Init move information array.
for move in charge_moves: #Loop through each Fast Move.
    if move=="Power Up Punch": #Gamepress titled this one move incorrectly.
       url="https://pokemongo.gamepress.gg/pokemon-move/power-punch" #So I manually added this link.
    else: #For all others.
       url="https://pokemongo.gamepress.gg/pokemon-move/"+move.replace(" ","-") #The link can be automatically generated.
    
    f = requests.get(url).text #Obtain HTML from page.
    f_lines=f.splitlines() #Split HTML into lines.
    
    for a in range(0,len(f_lines)): #Loop through each line of HTML.
        if 'Move Type</th><td><span class="' in f_lines[a]: #If this line has the Move Type information.
            move_type=f_lines[a].split('Move Type</th><td><span class="')[1].split("-")[0] #Extract the Move Type.
        if '<tr><th>Base Power</th><td>' in f_lines[a]: #If this line has the Base Power information.
            base_power=f_lines[a+1].split('>')[1].split("<")[0] #Extract the Base Power.
        if '<tr><th>Move Cooldown</th><td>' in f_lines[a]: #If this line has the Move Cooldown information.
            cooldown=f_lines[a+1].split('>')[1].split("<")[0] #Extract the Move Cooldown.
        if '<td class="energy-bar">' in f_lines[a]: #If this line has the energy bar display.
            energy_requirement=f_lines[a+1].split('charge-')[1].split('"')[0]  #Read the bar display.
            if "1" in energy_requirement:  #If there is 1 bar.
               energy_requirement=100 #The energy requirement is 100 energy.
            elif "2" in energy_requirement: #If there are two bars.
               energy_requirement=50 #The energy requirement is 50 energy.
            else: #Otherwise.
               energy_requirement=33 #The energy requirement is 33 energy.
    move_data[move]=[move_type,base_power,energy_requirement,cooldown] #Record data into array.

with open('Charged Move Data.csv', 'w', newline='') as csvfile:
   csvwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL) #Init csv writer.
   for i in range(0,len(list(move_data))): #Loop through each move in the array.
      csvwriter.writerow([list(move_data)[i]]+move_data[list(move_data)[i]]) #Record in the csv file.
