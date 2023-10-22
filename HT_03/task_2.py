"""
Write a script to remove an empty elements from a list.
    
    Test list: [(), ('hey'), ('',), ('ma', 'ke', 'my'), [''], {}, ['d', 'a', 'y'], '', []]
"""

test_list = [(), ('hey'), ('',), ('ma', 'ke', 'my'), [''], {}, ['d', 'a', 'y'], '', []]
result_list = [elem for elem in test_list if elem]

print(result_list)