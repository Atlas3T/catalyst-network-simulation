from storage import simple_storage

def main():
	
	store = simple_storage.store('/home/engr/Results/')

	x=5
	store.save_variable('test_folder_A','x',x)
	y = store.load_variable('test_folder_A','x')
	print(x == y)

	a=[[3, 7, 10], [5, 5, 3]]
	store.save_variable('test_folder_A','a',a)
	b = store.load_variable('test_folder_A','a')
	print(a == b)
	
	z='hello'
	store.save_variable('test_folder_B','z',z)
	w = store.load_variable('test_folder_B','z')
	print(z == w)

		
		

if __name__ == '__main__':
	main()
