from iiapds.node import Node

class BinaryTree(Node):
	"""docstring for ClassName"""
	def __init__(self,val=None):
		super(BinaryTree, self).__init__(val=val)

	def insert_left(self,node=None):
		# Example: 
		#    Original  Insert  Final
		#
		# 		0     l -> 3         0
		#      / \        / \       / \
		#     1   2      a   b     3   2
		#    / \                  / \
		#   x   y                a   b
		#                       /
		#                      1
		#                     / \
		#                    x   y

		if self.left == None:
			# insert left if don't have left child
			if type(node) == BinaryTree:
				self.left = node
			else:
				self.left = BinaryTree(val=node)
		else:
			# insert left have a left child
			if type(node) == BinaryTree:
				temp = node
			else:
				temp = BinaryTree(val=node)
			temp2 = temp
			while(temp2.left != None):
				temp2 = temp2.left
			temp2.insert_left(self.left)
			self.left = temp

	def insert_right(self,node=None):
		if self.right == None:
			# insert left if don't have right child
			if type(node) == BinaryTree:
				self.right = node
			else:
				self.right = BinaryTree(val=node)
		else:
			# insert right have a right child
			if type(node) == BinaryTree:
				temp = node
			else:
				temp = BinaryTree(val=node)
			temp2 = temp
			while(temp2.right != None):
				temp2 = temp2.right
			temp2.insert_right(self.right)
			self.right = temp

	def visit_node(self,node):
		'''
		Write your own code!
		See the example in test()
		'''
		pass

	def preorder(self,tree=None):
		''' Tree Traversals - Preorder
		order: [root] -> left -> right
		'''
		if tree != None:
			self.visit_node(tree)
			self.preorder(tree.get_left_child())
			self.preorder(tree.get_right_child())

	def inorder(self,tree):
		''' Tree Traversals - Inorder
		order: left -> [root] -> right
		'''
		if tree != None:
			self.preorder(tree.get_left_child())
			self.visit_node(tree)
			self.preorder(tree.get_right_child())
	
	def postorder(self,tree):
		''' Tree Traversals - Postorder
		order: left -> right -> [root]
		'''
		if tree != None:
			self.preorder(tree.get_left_child())
			self.preorder(tree.get_right_child())
			self.visit_node(tree)

	def get_left_child(self):
		return self.left

	def get_right_child(self):
		return self.right

	def set_value(self,val):
		self.val = val

	def get_value(self):
		return self.val

	def draw(self):
		print('Not developed yet!')

	def test(self):
		print('-------------------')
		print('Initial BinaryTree: 1')
		my_tree = BinaryTree(1)

		print('\nCreat left child: 2,3,4')
		my_tree.insert_left(2)
		my_tree.left.insert_left(3)
		my_tree.left.insert_right(4)

		print('\nCreat right child: 5')
		my_tree.insert_right(5)
		
		''' Now the tree is:
		            1
		           / \
		          2   5
		         / \
		        3   4
		'''

		print('\nCreat insert tree: a,b,c')
		new_left_child = BinaryTree('a')
		new_left_child.insert_left('b')
		new_left_child.insert_right('c')

		''' Insert tree is:
                    a
                   / \
                  b   c
		'''

		print('\nInsert to left child of Root')
		my_tree.insert_left(new_left_child)

		''' New tree should be:
                     1
                    / \
                   a   5
                  / \
                 b   c
                /
               2
              / \
             3   4
		'''
		print('\nPrint New tree:')
		print('        ',my_tree.val)
		print('        / \\')
		print('      ',my_tree.left.val,
			  ' ',my_tree.right.val)
		print('      / \\')
		print('    ',my_tree.left.left.val,
			  ' ',my_tree.left.right.val)
		print('    /')
		print('  ',my_tree.left.left.left.val)
		print('  / \\')
		print('',my_tree.left.left.left.left.val,
			  ' ',my_tree.left.left.left.right.val)

		def visit_node(node):
			print(node.val,end='')
		my_tree.visit_node = visit_node

		print('\nTree Traversals - Preorder:')
		my_tree.preorder(my_tree)
		print('\n\nTree Traversals - Inorder:')
		my_tree.inorder(my_tree)
		print('\n\nTree Traversals - Postorder:')
		my_tree.postorder(my_tree)
