import math

class Array(list):
	"""Array
	https://www.geeksforgeeks.org/array-data-structure/
	contents:
		* Array Rotation: left_rotate(),right_rotate()
		* Search an element in a Sorted and Rotated array:
			sorted_rotated_search()
	"""
	def __init__(self, content=[]):
		list.__init__([])
		self.extend(content)
		self.ans = None

	def _swap(self, fi, si, d):
		# This code is contributed by Rohit_ranjan
		for i in range(d):
		    temp = self[fi + i];
		    self[fi + i] = self[si + i];
		    self[si + i] = temp;

	def reverse(self, start=0, end=-1): 
		if len(self) == 0: return False
		if end == -1: end = len(self)-1
		while (start < end): 
			temp = self[start] 
			self[start] = self[end] 
			self[end] = temp 
			start = start + 1
			end = end - 1

	def binarySearch(self, low, high, key): 
		''' Standard Binary Search function 
		'''
		if high < low: 
		    return -1
		      
		# low + (high - low)/2;     
		mid = int((low + high)/2) 
		  
		if key == self[mid]: 
		    return mid 
		if key > self[mid]: 
		    return self.binarySearch((mid + 1),high,key); 
		return self.binarySearch(low, (mid -1), key); 

	def _findPivot(self, low, high): 
		''' Function to get pivot. For array  
		    3, 4, 5, 6, 1, 2 it returns 3  
		    (index of 6) 
		    example:
		    [1,2,3,4,5] -(rotate)> [2,3,4,{5},1] -> 3 (count from left)
		    [5,4,3,2,1] -(rotate)> [1,{5},4,3,2] -> 3 (count from right)
		    [1,2,3,6,8] -(rotate)> [2,3,6,{8},1] -> 3 (arrays can not contiguous)

		    This is contributed by Smitha Dinesh Semwal 
		'''
		# base cases 
		if high < low: 
		    return -1
		if high == low: 
		    return low 
		  
		# low + (high - low)/2; 
		mid = int((low + high)/2) 
		  
		if mid < high and self[mid] > self[mid + 1]: 
		    return mid 
		if mid > low and self[mid] < self[mid - 1]: 
		    return (mid-1) 
		if self[low] >= self[mid]: 
		    return self._findPivot(low, mid-1) 
		return self._findPivot(mid + 1, high) 

	def left_rotate(self,n,method=3):
		''' leftRotate
		Method 1: using temp array
			Time complexity: O(m) - m items in array
			Auxiliary Space: O(n) - move n items
		Method 2: rotate one by one
			Time complexity: O(m*n) - m items in array
			Auxiliary Space: O(1)
		Method 3: A Juggling Algorithm (Improved Method 2)
			Time complexity: O(m) - m items in array
			Auxiliary Space: O(1)
		Method 4: The Reversal Algorithm
		    Time complexity: O(m) - m items in array
		Method 5: Block swap algorithm
		    Time complexity: O(m) - m items in array
		'''
		# Validity check and change
		if type(n) != int or n < 1:
			return False
		m = len(self)
		if n>=m:
			n = n%m
			if n == 0:
				return False

		# leftRotate
		# Method 1: using temp array
		if method == 1:
			temp_array = self[n:]+self[:n]
			self.clear()
			self.extend(temp_array)
		# Method 2: rotate one by one
		elif method == 2:
			temp = self[0]
			for i in range(m-1):
				self[i] = self[i+1]
			self[-1] = temp
			self.leftRotate(n-1,1)
		# Method 3: A Juggling Algorithm
		elif method == 3:
			# divide into several group to move
			group_num = math.gcd(m,n) # Greatest common factor
			if group_num == 1:
				group_len = m
			else:
				group_len = m//group_num
			# move each group
			for group in range(group_num):
				# set initial parameters
				index = n+group
				temp1 = self[index]
				for count in range(group_len):
					# get current index
					index = index - n
					if index < 0:
						index = m + index
					# change current item and temp1
					temp2 = self[index]
					self[index] = temp1
					temp1 = temp2
			''' Method 3 example: This case only has one group
			1 2 3 4 5 6 7 m = 7 n = 3 --> m = 7 n = 4
			                        temp = 4 index = 3
			[1]2 3 4 5 6 7 count = 1 temp = 1 index = 3-3 = 0
			4 2 3 4[1]6 7 count = 2 temp = 5 index = 0-3 = -3 => 7-3=4
			4[5]3 4 1 6 7 count = 3 temp = 2 index = 4-3 = 1
			4 5 3 4 1[2]7 count = 4 temp = 6 index = 1-3 = -2 => 7-2=5
			4 5[6]4 1 2 7 count = 5 temp = 3 index = 5-3 = 2
			4 5 6 4 1 2[3]count = 6 temp = 3 index = 2-3 = -1 => 7-1=6
			4 5 6 7 1 2 3
			'''
		# Method 4: The Reversal Algorithm
		elif method == 4:
			# This code is contributed by Devesh Agrawal 
			# https://www.geeksforgeeks.org/program-for-array-rotation-continued-reversal-algorithm/
			self.reverse(0, n-1) 
			self.reverse(n, m-1) 
			self.reverse(0, m-1) 
		# Method 5: Block swap algorithm
		elif method == 5: 
			# This code is contributed by Rohit_ranjan
			# https://www.geeksforgeeks.org/block-swap-algorithm-for-array-rotation/
			if(n == 0 or n == m): 
			    return False
			i = n 
			j = m - n 
			while (i != j): 
			    if(i < j): # A is shorter
			        self._swap(n - i, n + j - i, i) 
			        j = j-i 
			    else: # B is shorter
			        self._swap(n - i, n, j) 
			        i = i-j 
			self._swap(n - i, n, i)

	def right_rotate(self,n,method=3):
		''' rightRotate
		Method 1: using temp array
			Time complexity: O(m) - m items in array
			Auxiliary Space: O(n) - move n items
		Method 2: rotate one by one
			Time complexity: O(m*n) - m items in array
			Auxiliary Space: O(1)
		Method 3: A Juggling Algorithm (Improved Method 2)
			Time complexity: O(m) - m items in array
			Auxiliary Space: O(1)
		Method 4: The Reversal Algorithm
		    Time complexity: O(m) - m items in array
		    Auxiliary Space: O(1)
		Method 5: Block swap algorithm
			Time complexity: O(m) - m items in array
		'''
		# Validity check and change
		if type(n) != int or n < 1:
			return False
		m = len(self)
		if n>=m:
			n = n%m
			if n == 0:
				return False

		# rightRotate
		if method == 1:
			temp_array = self[-n:]+self[:-n]
			self.clear()
			self.extend(temp_array)
		elif method == 2:
			temp = self[-1]
			for i in range(len(self)-1):
				self[-1-i] = self[-2-i]
			self[0] = temp
			self.rightRotate(n-1,1)
		elif method == 3:
			# convert rightRotate to leftRotate
			n = m - n
			# divide into several group to move
			group_num = math.gcd(m,n) #Greatest common factor
			if group_num == 1:
				group_len = m
			else:
				group_len = m//group_num
			# move each group
			for group in range(group_num):
				# set initial parameters
				index = n+group
				temp1 = self[index]
				for count in range(group_len):
					# get current index
					index = index - n
					if index < 0:
						index = m + index
					# change current item and temp1
					temp2 = self[index]
					self[index] = temp1
					temp1 = temp2
			''' Method 3 example: This case only has one group
			1 2 3 4 5 6 7 m = 7 n = 3 --> m = 7 n = 4
			than convert rightRotate to leftRotate
			'''
		elif method == 4:
			# convert rightRotate to leftRotate
			n = m - n
			self.reverse(0, n-1) 
			self.reverse(n, m-1) 
			self.reverse(0, m-1) 
		elif method == 5:
			# convert rightRotate to leftRotate
			n = m - n
			# This code is contributed by Rohit_ranjan
			# https://www.geeksforgeeks.org/block-swap-algorithm-for-array-rotation/
			if(n == 0 or n == m): 
			    return False
			i = n 
			j = m - n 
			while (i != j): 
			    if(i < j): # A is shorter
			        self._swap(n - i, n + j - i, i) 
			        j = j-i 
			    else: # B is shorter
			        self._swap(n - i, n, j) 
			        i = i-j 
			self._swap(n - i, n, i)

	def sorted_rotated_search(self,key, method=1):
		''' Search an element in a sorted and rotated array
		In this case, 1 2 3 4 5 might become 3 4 5 1 2. 
		Devise a way to find an element in the rotated array 
		in O(log n) time.

		Both Basic solution and Improved solution:
		Time Complexity: O(log n).
		Binary Search requires log n comparisons to find the element. 
		So time complexity is O(log n).
		Space Complexity:O(1), No extra space is required. 
		'''
		# Validity check and change
		index = None
		n = len(self)
		if n == 0: return None
		
		# Method 1: Basic Solution
		if method == 1:
			pivot = self._findPivot(0, n-1); 
			print(pivot)
			# If we didn't find a pivot,  
			# then array is not rotated at all 
			if pivot == -1: 
			    return self.binarySearch(0, n-1, key); 
			# If we found a pivot, then first 
			# compare with pivot and then 
			# search in two subarrays around pivot 
			if self[pivot] == key: 
			    return pivot 
			if self[0] <= key: 
			    return self.binarySearch(0, pivot-1, key); 
			return self.binarySearch(pivot + 1, n-1, key); 
		# Method 2: Improved Solution
		elif method == 2:
			def search(l, h, key):
				# This code is contributed by Shreyanshi Arun
				print('l ',l,', h',h)
				if l > h: 
				    return -1

				mid = (l + h) // 2
				if self[mid] == key: 
				    return mid 

				# If arr[l...mid] is sorted  
				if self[l] <= self[mid]: 

				    # As this subarray is sorted, we can quickly 
				    # check if key lies in half or other half  
				    if key >= self[l] and key <= self[mid]: 
				        return search(l, mid-1, key) 
				    return search(mid + 1, h, key) 

				# If arr[l..mid] is not sorted, then arr[mid... r] 
				# must be sorted 
				if key >= self[mid] and key <= self[h]: 
				    return search(mid + 1, h, key) 
				return search(l, mid-1, key) 
			index = search(0, n-1, key)

		return index

	def test(self):
		print('----------------------\n'
			  '     Array Test       ')
		print('\nInit')
		#my_array = Array([9,8,7,6,5,4,3,2,1])
		my_array = Array([1,2,3,4,5,6,7,8,9])
		print(my_array)
		print('\nleftRotate by 7')
		my_array.left_rotate(7,method=5)
		print(my_array)
		print('\nrightRotate by 3')
		my_array.right_rotate(3,method=3)
		print(my_array)
		print('\nSearch an element [2] in a sorted and rotated array')
		print('index of 2 is:',my_array.sorted_rotated_search(2,method=1))

#my_array = Array()
#my_array.test()