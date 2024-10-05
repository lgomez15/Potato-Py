import csv

def format_data():
    file_path = "LST-Request-MOD11A1-061-results.csv"
    with open(file_path, mode='r', newline='') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Read the header
            # Find the indices of the required columns
            date_idx = header.index("Date")
            lst_day_idx = header.index("MOD11A1_061_LST_Day_1km")
            
            # Filter the data to include only the required columns
            data = [
                (row[date_idx], row[lst_day_idx]) 
                for row in csv_reader
            ]

    # Print only the filtered data
    # Convert the second part of the data to float and subtract 273.15
    data = [(date, float(lst_day) - 273.15) for date, lst_day in data]

    filtered_data = [(date, round(temp, 2)) for date, temp in data if temp >= -270]
    data = filtered_data

    output_file_path = "SalamancaLST.csv"
    with open(output_file_path, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        # Write the header
        csv_writer.writerow(["Date", "LST_Day_Celsius"])
        # Write the data
        csv_writer.writerows(data)