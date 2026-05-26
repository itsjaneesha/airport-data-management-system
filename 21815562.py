"""
****************************************************************************
Additional info
 1. I declare that my work contins no examples of misconduct, such as
 plagiarism, or collusion.
 2. Any code taken from other sources is referenced within my code solution.
 3. Student ID: 21815562
 4. Date: 23/11/2025
****************************************************************************

"""
from graphics import *
import csv
import math

data_list = []   # An empty list to load and hold data from csv file

def load_csv(CSV_chosen):
    """
    This function loads any csv file by name (set by the variable 'selected_data_file') into the list "data_list"
    YOU DO NOT NEED TO CHANGE THIS BLOCK OF CODE
    """
    with open(CSV_chosen, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for line in csvreader:
            data_list.append(line)

#starting loop
while True:
    data_list.clear()  # clear previous data for new run

    #TASK A - get user input
    import csv

    valid_airports = ["LHR", "MAD", "CDG", "IST", "AMS", "LIS", "FRA", "FCO", "MUC", "BCN"]

    while True:
        city_code = input("Please enter a three-letter city code: ").upper()
        if len(city_code) != 3:
            print("Wrong code length – please enter a three-letter city code.")
        elif city_code not in valid_airports:
            print("Unavailable city code - please enter a valid city code.")
        else:
            break

    while True:
        year = input("Please enter the year required in the format YYYY: ")
        if not year.isdigit() or len(year) != 4:
            print("Wrong data type - please enter a four-digit year value.")
        elif int(year) < 2000 or int(year) > 2025:
            print("Out of range - please enter a value from 2000 to 2025.")
        else:
            break

    selected_data_file = f"{city_code}{year}.csv"
    
    try:
        load_csv(selected_data_file)
    except FileNotFoundError:
        print("That file wasn’t found in this folder. Make sure the CSV is here!")
        continue  # restart loop



    # TASK B - read data from file


    airport_names = {
        "LHR":"London Heathline", "MAD":"Madrid Adolfo Suárez-Barajas",
        "CDG":"Charles De Gaulle International", "IST":"Istanbul Airport International",
        "AMS":"Amsterdam Schiphol", "LIS":"Lisbon Portela", "FRA":"Frankfurt Main",
        "FCO":"Rome Fiumicino", "MUC":"Munich International", "BCN":"Barcelona International"}
    #this is a dictionary to convert airport code names to real names.
    

    airport_code = selected_data_file[:3] #first 3 letters of data file will be the airport code
    airport_fullname = airport_names.get(airport_code, airport_code)
    year = selected_data_file[3:7] #take character position from 3 to 7 
    
    
    
#starts all counts from zero
    total_flights = 0
    terminal2_count = 0
    under600_count = 0
    airfrance_count = 0
    below15_count = 0
    ba_count = 0
    af_delayed_count = 0

    rain_hours = set() #not to repeat hours

    from collections import Counter 
    destination_count = Counter()
    #reference taken from w3schools : https://www.w3schools.com/python/ref_module_collections.asp
    #to count how many flights went to a destination

    for line in data_list:
        total_flights += 1

        terminal = line[8]
        if terminal == "2":
            terminal2_count += 1

        
        distance = int(line[5])
        if distance < 600:
            under600_count += 1
        
        

        flightnum = line[1]
        airline = flightnum[:2].upper()
        if airline == "AF":
            airfrance_count += 1
            if line[3] != line[2]:
                af_delayed_count += 1
        if airline == "BA":
            ba_count += 1
            

        weather = line[10]
        temperature_value = int(weather[:2])
        if temperature_value < 15:
            below15_count += 1
            
            

        scheduled_time_departure = line[2]
        if len(scheduled_time_departure) >= 2:
            hour = scheduled_time_departure[:2]
            if "rain" in weather.lower():
                rain_hours.add(hour)
#the "hour" set counts how many unique hours had rain                

        destination_code = line[4]
        destination_count[destination_code] += 1


#calculate the values
        
    # average number of British Airways departures per hour      
    avg_ba_per_hour = round(ba_count / 12.0, 2)
    
    #  British Airways percentage 
    if total_flights > 0:
        ba_pct = round((ba_count / total_flights) * 100, 2)
    else:
        ba_pct = 0.0


    # Air France delayed percentage 
    if airfrance_count > 0:
        af_delayed_pct = round((af_delayed_count / airfrance_count) * 100, 2)
    else:
        af_delayed_pct = 0.0


  #how many unique hours had rain
    hours_of_rain = len(rain_hours)


#find least common destination

    min_count = min(destination_count.values())
    least_common_names = [
        airport_names.get(code)
        for code, count in destination_count.items()
        if count == min_count]
    
    if len(data_list) == 0:
        print("No data loaded. Exiting.")
        exit()
    

    print()
    print("************************************************************************")
    print("File", selected_data_file, "- Planes departing", airport_fullname, year)
    print("************************************************************************")
    print()

    print(f"The total number of flights from this airport was {total_flights}")
    print(f"The total number of flights departing Terminal Two was {terminal2_count}")
    print(f"The total number of departures on flights under 600 miles was {under600_count}")
    print(f"There were {airfrance_count} Air France flights from this airport")
    print(f"There were {below15_count} flights departing in temperatures below 15 degrees")
    print(f"There was an average of {avg_ba_per_hour:.2f} British Airways flights per hour from this airport")
    print(f"British Airways planes made up {ba_pct:.2f}% of all departures")
    print(f"{af_delayed_pct:.2f}% of Air France departures were delayed")
    print(f"There were {hours_of_rain} hours in which rain fell")
    print(f"The least common destinations are {least_common_names}")

    # TASK C: Save results to text file

    with open("results.txt", "a") as file:
        file.write("****************************************************************************\n")
        file.write(f"File {selected_data_file} selected - Planes departing {airport_fullname} {year}\n")
        file.write("****************************************************************************\n\n")
        file.write(f"The total number of flights from this airport was {total_flights}\n")
        file.write(f"The total number of flights departing Terminal Two was {terminal2_count}\n")
        file.write(f"The total number of departures on flights under 600 miles was {under600_count}\n")
        file.write(f"There were {airfrance_count} Air France flights from this airport\n")
        file.write(f"There were {below15_count} flights departing in temperatures below 15 degrees\n")
        file.write(f"There was an average of {avg_ba_per_hour:.2f} British Airways flights per hour from this airport\n")
        file.write(f"British Airways planes made up {ba_pct:.2f}% of all departures\n")
        file.write(f"{af_delayed_pct:.2f}% of Air France departures were delayed\n")
        file.write(f"There were {hours_of_rain} hours in which rain fell\n")
        file.write(f"The least common destinations are {least_common_names}\n\n")
        
        
        

 # TASK D: Histogram
 #reference taken from @leftpeel7846 on youtube
 # video link : https://youtu.be/R39vTAj1u_8?si=Sb1pA9BLW72UFxqi
 
 
        valid_airlines = ["AF", "BA", "KL", "LH", "EZ", "IB", "TK", "SU", "QR", "EK"]
  
        airline_names = {
                "BA": "British Airways",
                "AF": "Air France",
                "AY": "Finnair",
                "KL": "KLM",
                "SK": "Scandinavian Airlines",
                "TP": "TAP Air Portugal",
                "TK": "Turkish Airlines",
                "W6": "Wizz Air",
                "U2": "easyJet",
                "FR": "Ryanair",
                "A3": "Aegean Airlines",
                "SN": "Brussels Airlines",
                "EK": "Emirates",
                "QR": "Qatar Airways",
                "IB": "Iberia",
                "LH": "Lufthansa"}      
#this is a dictionary to convert airline code names to real names.

        while True:
            airline_code = input("enter a two-letter airline code to plot a histogram :").upper()
            if airline_code in valid_airlines:
                break
            else:
                print("Unavailable Airline code please try again: ")

        hours = []
        for h in range(12):
            if h < 10:
                hr = '0' + str(h)
            else:
                hr = str(h)
            hours.append(hr)

        hour_counts = {}
        for hr in hours:
            hour_counts[hr] = 0

        for line in data_list:
            flight = line[1].upper()
            if flight.startswith(airline_code):
                scheduled_time = line[2]
                if len(scheduled_time) >= 2:
                    hr = scheduled_time[:2]
                    if hr in hour_counts:
                        hour_counts[hr] = hour_counts[hr] + 1

        win = GraphWin("histogram", 800, 500)
        win.setBackground("white")

        # in case max_value was 0
        try:
            max_value = max(hour_counts.values())
            scale = 450.0 / max_value  
        except (ValueError, ZeroDivisionError):
            
            # If no flights or max_value is 0 set scale to 1
            max_value = 0
            scale = 1

        x_origin = 200
        y_top = 80
        bar_height = 25
        gap = 10

      
        airline_fullname = airline_names.get(airline_code, airline_code)

        title_text = "Departure by hour for " + airline_fullname + " from " + airport_fullname + " " + year
        title = Text(Point(400, 40), title_text)
        title.setSize(10)
        title.draw(win)


        i = 0
        for hr in hours:
            count = hour_counts[hr]

            y1 = y_top + i * (bar_height + gap)
            y2 = y1 + bar_height
            bar_len = count * scale

            bar = Rectangle(Point(x_origin, y1), Point(x_origin + bar_len, y2))
            bar.setFill("turquoise")
            bar.draw(win)

            hour_label = Text(Point(140, y1 + bar_height / 2), hr)
            hour_label.draw(win)

            value_label = Text(Point(x_origin + bar_len + 20, y1 + bar_height / 2), str(count))
            value_label.draw(win)

            i = i + 1

        y_label = Text(Point(100, 60), "Hour")
        y_label.setSize(9)
        y_label.draw(win)

        win.getMouse()
        win.close()
        
 #Task E
#ask user if they want to re run the program

        again = input("Do you want to select a new data file? (Y/N): ").upper()

        if again == "Y":
            continue
        else:
            print("Thank you. End of run")
            break






