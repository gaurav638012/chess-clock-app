import csv
fields=['white_time','black_time','white_increment','black_increment']
with open("created_games1.csv","w") as file:
    csvwriter=csv.writer(file)
    csvwriter.writerow(fields)
    


