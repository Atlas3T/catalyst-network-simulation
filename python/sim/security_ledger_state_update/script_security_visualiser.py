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
    node_p = "P_100"
    if check_excel_sheets_readable(filename, node_p) is not True:
         print("abort")
         exit()

    #Here we extract the cells from the array
    Full_Array = worksheet_to_array(filename,node_p)
    # print(Full_Array)

    node_p_tree = Node(node_p)

    unique_a = np.unique(Full_Array[:,0], return_counts=False) #Produces a list of unique I'Ds for first collumn
    print("a -- ", unique_a)
    ind_unique = 0 
    unique_a_it_parent = unique_a[ind_unique]
    parent_top_it = unique_a_it_parent #From those unique values it selects the first value from that list 
    std_parent = "parent: " + parent_top_it
    node_parent_top_it = Node("{}".format(std_parent), parent=node_p_tree) #Creates the top level i.e. p=100
    # cretae the first child of the first parent

    unique_b = np.unique(Full_Array[:,1], return_counts=False) #Produces a list of unique I'Ds for first collumn
    print("b -- ", unique_b)
    ind_unique_child = 0 
    unique_b_it_child = unique_b[ind_unique_child] #From those unique values it selects the first value from that list 
    child_top_it = unique_b_it_child
    std_child = "child: " + child_top_it 
    node_child_top_it = Node("{}".format(std_child), parent=node_parent_top_it) #Creates the top level i.e. p=100

    #create the parent node 1
    for rowa in Full_Array: #for each row in the full array 
        if rowa[0] == unique_a_it_parent: #if first row = 
            #creatre a child 
            ind_unique_child += 1
            unique_b_it = unique_b[ind_unique_child]
            child_top_it = unique_b_it_child
            std_child = "parent: " + child_top_it
            node_child_it  = Node("{}".format(std_parent), parent=node_parent_top_it)
        else:
            ind_unique += 1
            unique_a_it = unique_a[ind_unique]
            parent_top_it = unique_a_it
            std_parent = "parent: " + parent_top_it
            node_parent_top_it  = Node("{}".format(std_parent), parent=node_p_tree)
            # create the first child
       
    for pre, fill, node in RenderTree(node_p_tree):
        print("%s%s" % (pre, node.node_p_tree)) 

    #    while Full_Array[i,0] == unique_a_it:
    #        print(i, " ",Full_Array[i,0])
    #    unique_a_it = Full_Array[i,0]

    #DotExporter(udo).to_picture("udo.png")

    #main that execute

    #def can you read from excel --> True


    #def read from excel --> array (a,b,c,d)


#def build the tree (one per P)


