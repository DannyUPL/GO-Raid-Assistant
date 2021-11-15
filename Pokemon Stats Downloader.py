import requests,csv

link = "https://pokemon.gameinfo.io/en/pokemon/" #Link to be used to find data.
pokedex=[] #Init array of Pokémon information.

for i in range(1,5):#721): #Loop through each Pokémon that exists.

    species_link=(link+str(i)) #Generate a link for this Pokémon species.
    f = requests.get(species_link).text #Retrieve HTML content of page.

    try: #Some Pokémon have multiple forms (different variants of the same species). This section deals with a Pokémon that has multiple forms.
        forms=f.split('<select id="forms">')[1].split('</select>')[0].split('</option>') #Find different forms.
        del forms[-1] #Remove irrelevant data.
        for x in range(0,len(forms)): #Cycle through different forms
            forms[x]=forms[x].split(">")[1].replace(" ","-")
        if "Shadow" in forms: #Remove Shadow form as it is fundamentally identical to the default form.
            forms.remove("Shadow")
        if "Purified" in forms: #Remove Purified form as it is fundamentally identical to the default form.
            forms.remove("Purified")
    except Exception as e: #If no forms can be found.
        forms=["Normal"]

    if forms==[]: #If no forms are found.
        forms=["Normal"]
        
    for form in forms: #For each form in the list of forms.

        form_link=(link+str(i)+'/'+form.lower()) #Generate a link for this form
        f = requests.get(form_link).text #Retrieve HTML content of page.

        f = f.replace('Farfetch&#039;d',"Farfetch'd") #The species known as Farfetch'd has an odd character which should be replaced for compatibility reasons.
        pokemon_name=f.split('<meta property="og:title" 		content="')[1].split(" (")[0] #Extract the species name.
        pokemon_image=f.split('<meta property="og:image" 		content="')[1].split('"')[0] #Extract the image link.
        pokemon_name=pokemon_name.replace(" - Normal","") #If the Pokémon is in its standard form, there is no need to specify this.

        try:
            evolution=f.split("evolves into ")[1].split(".")[0] #Extract evolution information if possible.
            evolution=evolution.replace("♀","-F") #Replace certain characters for compatibility reasons.
            evolution=evolution.replace("♂","-M") #Replace certain characters for compatibility reasons.
            evolution=evolution.replace("(Normal)","") #If the Pokémon is in its standard form, there is no need to specify this.
            evolution=evolution.replace(" Form","") #If the Pokémon is in an alternate form, there is no need for the word "Form" at the end.
            if "- " in evolution: #Reformat alternate forms with brackets instead of hypens.
                evolution=evolution.replace("- ","(")+")"
        except:
            evolution="None"

        pokemon_type_text=f.split('<article class="pokemon-type">')[1].split('class="large-type">')[1].splitlines() #Extract Pokémon type text.

        pokemon_types=[] #Create list of Pokémon types.
        pokemon_type_text=pokemon_type_text[1:] #Remove irrelevant data.
        types_obtained=False #Init loop value.
        for line in pokemon_type_text: #For each line in the extracted Pokémon type text.
            if types_obtained==False and "type large" in line and "POKEMON_TYPE_" in line: #If this line is relevant to the Pokémon's typing.
                pokemon_types.append(line.split(">")[1].split("</div")[0]) #Add it to the list of types.
            else: #If this line is not relevant to the Pokémon's typing.
                types_obtained=True #End the loop.

        move_tables=f.split('<table class="moves">') #Extract move tables.
        del move_tables[0] #Remove irrelevant data.
        move_tables[-1]=move_tables[-1].split("</table")[0] #Remove irrelevant data.
        fast_moves=[] #Initialise fast move list. 
        charged_moves=[] #Initialise charged move list.
        for move_table in move_tables: #For each move table on the page.
            moves_to_add=[] #Init list of moves.
            for z in range(0,len(move_table.splitlines())): #For each move in the table.
                if "en/move/" in move_table.splitlines()[z]:
                    moves_to_add.append(move_table.splitlines()[z+1]) #Extract move table entry.
            for item in moves_to_add: #For each move in the list of move table entries.
                if "Quick move" in move_table: #If the entry is from the fast moves table.
                    fast_moves.append(item.replace("\t","").replace("-"," ")) #Add the move name to the list of fast moves.
                else: #Otherwise, if it is from the charged moves table.
                    charged_moves.append(item.replace("\t","").replace("-"," ")) #Add the move name to the list of charged moves.

        f_lines=f.splitlines() #Split the HTML content into a list of lines.
        for a in range(0,len(f_lines)): #Loop through each line to find the stats.
            if '<div class="bar sta">' in f_lines[a]: #If this line features the stamina icon.
                stamina=f_lines[a+4].split(">")[1].split("<")[0] #The stamina number will be featured on the line four lines ahead, so extract it from there.
            if '<div class="bar def">' in f_lines[a]: #If this line features the defense icon.
                defense=f_lines[a+4].split(">")[1].split("<")[0] #The defense number will be featured on the line four lines ahead, so extract it from there.
            if '<div class="bar att">' in f_lines[a]: #If this line features the attack icon.
                attack=f_lines[a+4].split(">")[1].split("<")[0] #The attack number will be featured on the line four lines ahead, so extract it from there.
            
        pokemon_name=pokemon_name.replace("♀","-F") #Replace certain characters for compatibility reasons.
        pokemon_name=pokemon_name.replace("♂","-M") #Replace certain characters for compatibility reasons.
        pokemon_name=pokemon_name.replace("(Normal)","") #If the Pokémon is in its standard form, there is no need to specify this.
        pokemon_name=pokemon_name.replace(" Form","") #If the Pokémon is in an alternate form, there is no need for the word "Form" at the end.
        if "- " in pokemon_name: #Reformat alternate forms with brackets instead of hypens.
            pokemon_name=pokemon_name.replace("- ","(")+")"

        number=str(i)
        print(pokemon_name)
        
        pokedex.append({"pokemon_name":pokemon_name,"pokemon_types":pokemon_types,"charged_moves":charged_moves,"fast_moves":fast_moves,"evolution":evolution,"attack":attack,"defense":defense,"stamina":stamina,"number":str(i),"pokemon_image":pokemon_image}) #Add the acquired data to the array.

with open('Spreadsheet.csv', 'w', newline='') as csvfile: #Open a new csv spreadsheet file.
    csvwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL) #Initialise csv writer.
    csvwriter.writerow(["Name","Type","Charge Moves","Fast Moves","Evolution","Attack","Defense","Stamina","National Dex No","Image"]) #Write the initial title row.
    for pokemon in pokedex: #For each dictionary entry in the array.
        csvwriter.writerow([pokemon["pokemon_name"],"#".join(pokemon["pokemon_types"]),"#".join(pokemon["charged_moves"]),"#".join(pokemon["fast_moves"]),pokemon["evolution"],pokemon["attack"],pokemon["defense"],pokemon["stamina"],pokemon["number"],pokemon["pokemon_image"]]) #Write into csv file.
