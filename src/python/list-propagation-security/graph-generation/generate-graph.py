import matplotlib.pyplot as plt
import glob
import pandas as pd

def load_excel_file():
    get_excel_file = pd.ExcelFile("../datafile-generation/master_ouput.xlsx")
    get_sheet_names = get_excel_file.sheet_names
    return get_sheet_names, get_excel_file

def excel_to_graph(): 
   
    get_sheet_names, get_excel_file = load_excel_file()
    for sheet in get_sheet_names:    
        all_data = pd.DataFrame() 
        data = pd.read_excel('../datafile-generation/master_ouput.xlsx', sheet, dtype={'id': str})
        all_data = all_data.append(data,ignore_index=True)
        producer_ratio = set(data['Correct Producers Ratio'])
        for ratio in producer_ratio:
            split_data = all_data[all_data['Correct Producers Ratio'] == ratio]
            print (split_data)
            produce_graph(ratio, split_data)
        plt.legend()
        plt.title('Graph for {}'.format(sheet))
        plt.savefig('graphs/'+sheet) 

        
def produce_graph(ratio, split_data):
    ratio = str(ratio) 

    plt.plot(split_data['Collected Updates Ratio'], split_data['percentage_for_50_%'], label=ratio)
    

if __name__ == '__main__':               

    excel_to_graph()
