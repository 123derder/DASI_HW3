import csv
import math
import datetime
#from darts import TimeSeries

# You should not modify this part.
def config():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--consumption", default="./sample_data/consumption.csv", help="input the consumption data path")
    parser.add_argument("--generation", default="./sample_data/generation.csv", help="input the generation data path")
    parser.add_argument("--bidresult", default="./sample_data/bidresult.csv", help="input the bids result path")
    parser.add_argument("--output", default="output.csv", help="output the bids path")

    return parser.parse_args()


def output(path, data):
    import pandas as pd

    df = pd.DataFrame(data, columns=["time", "action", "target_price", "target_volume"])
    df.to_csv(path, index=False)

    return


if __name__ == "__main__":
    args = config()

    data = [["2018-01-01 00:00:00", "buy", 2.5, 3],
            ["2018-01-01 01:00:00", "sell", 3, 5]]

    
    times=[]
    values=[]
    for i in range(0,24):
        times.append(0)
        values.append(0)

    with open(args.consumption,'r') as C_file:
        Consumption=csv.DictReader(C_file)
        
        with open(args.generation,'r') as G_file: 
            Generation=csv.DictReader(G_file)

          
            i=0
            for consumption_data,generation_data in zip(Consumption,Generation):
                last_time=generation_data['time']
                if generation_data['generation'] > consumption_data['consumption']:
                    #print("> "+str(generation_data['time'])+' : '+str(generation_data['generation'])+"   "+str(consumption_data['consumption'])+"  "+str(math.floor((float(generation_data['generation'])-float(consumption_data['consumption']))*100)/100)+"  ***")
                    values[i] = values[i] + (math.floor((float(generation_data['generation'])-float(consumption_data['consumption']))*100)/100)
                    times[i] = times[i] + 1
                else:
                    #print("> "+str(generation_data['time'])+' : '+str(generation_data['generation'])+"   "+str(consumption_data['consumption']))
                    if times[i]==0:
                        values[i] = values[i] + (math.floor((float(generation_data['generation'])-float(consumption_data['consumption']))*100)/100)
                i=(i+1)%24

    with open(args.bidresult,'r',encoding='utf-8') as bid_file:
        bidresult=csv.DictReader(bid_file)
       
    #print('last_time: '+str(last_time))
    #print(str((datetime.datetime.strptime(last_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")))
   
    for i in range(0,24):
        if times[i]==0:
            values[i] = round(values[i]/7,2)
        else:
            values[i] = round(values[i]/times[i],2)
       
    '''
        time,action,target_price,target_volume
        2018-01-01 00:00:00,buy,2.5,3
        2018-01-01 01:00:00,sell,3.0,5

    '''
    # with open('names.csv', 'w',newline='') as csvfile:
    #     fieldnames = ['time', 'action','target_price','target_volume']
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    #     writer.writeheader()
    output_data=[]
    for i in range(0,24):
        last_time=(datetime.datetime.strptime(last_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        if values[i]<0:
            values[i]=-values[i]
        
        if times[i] > 2:
            output_data.append([last_time,"sell",0.01,values[i]])
        if times[i] == 0:
            output_data.append([last_time,"buy",2.52,values[i]])
        if times[i] <= 2:
            output_data.append([last_time,"sell",2.53,math.floor((1000+values[i])*100)/100])
            # if 0 < times[i] and times[i] <7:
            #     writer.writerow({"time":last_time, "action":"sell","target_price":0.01,"target_volume":0.1,"times":times[i]})

    output(args.output, output_data)
