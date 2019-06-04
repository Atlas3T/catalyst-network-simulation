from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import graphviz
from openpyxl import load_workbook
import numpy as np


def check_excel_sheets_readable(path_name="Result_simulation_security_ledger_update.xlsx",sheet_ranges=""): 
    try: 
        wb = load_workbook(filename)
        try:
            source = wb.get_sheet_by_name(sheet_ranges)
            return True
        except KeyError as e:
            print("Unable to open sheet {}".format(sheet_ranges))
            return False
    except IOError as e:
        print("Unable to open workbook {}".format(path_name))
        return False


def worksheet_to_array(path_name="Result_simulation_security_ledger_update.xlsx",sheet_ranges=""):
    wb = load_workbook(filename)
    source = wb.get_sheet_by_name(sheet_ranges)
    firstRow = 2
    firstCol = 2
    nCols = 100
    nRows = 100
    allCells = np.array([[cell.value for cell in row] for row in source.iter_rows()])
    data = allCells[(firstRow-1):(firstRow-1+nRows),(firstCol-1):(firstCol-1+nCols)]
    return(data)


if __name__ == '__main__':


    #This function checks that both the excel file and the excel sheets can be opened#  
    filename = 'test.xlsx'
    P_Value = "P_100"
    if check_excel_sheets_readable(filename, P_Value) is not True:
         print("abort")
         exit()

    #Here we extract the cells from the array
    Full_Array = worksheet_to_array(filename,P_Value)
    # print(Full_Array)

    unique_a = np.unique(Full_Array[:,0], return_counts=False)
    print("a -- ", unique_a)
    unique_a_it = unique_a[0]
    for i in Full_Array: 
        while Full_Array[i,0] == unique_a_it:
            print(i, " ",Full_Array[i,0])
        unique_a_it = Full_Array[i,0]
        

    # Load work book, and sheet with "P_"+str(p) 
    # example
    udo = Node(P_Value)
    marc = Node("Marc", parent=udo)
    lian = Node("Lian", parent=marc)
    dan = Node("Dan", parent=udo)
    jet = Node("Jet", parent=dan)
    jan = Node("Jan", parent=dan)
    joe = Node("Joe", parent=dan)

    for pre, fill, node in RenderTree(udo):
        print("%s%s" % (pre, node.name))

    #DotExporter(udo).to_picture("udo.png")

    #main that execute

    #def can you read from excel --> True


    #def read from excel --> array (a,b,c,d)


#def build the tree (one per P)


