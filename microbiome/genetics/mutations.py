# Erasmus GP Gene Pool


from microbiome.genetics.gc_mutation_functions import *
from random import random, uniform


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:44.370142Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '0000000000000000000000000000000000000000000000000000000000000000',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 1,
 'graph': {'A': [['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'function': {'python3': {'0': {'inline': 'append_constant({0[i0]}, '
                                                        '-1.0)'}}},
               'name': 'New constant: -1.0'},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 1,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '7404cd51f0ff21ae1b51cd8e13b6bacf706cafde670c9ef05ae282fea9ff2364'}
'''
def gc_7404cd51f0ff21ae1b51cd8e13b6bacf706cafde670c9ef05ae282fea9ff2364(i):
	return (append_constant(i[0], -1.0),)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:44.079798Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '0000000000000000000000000000000000000000000000000000000000000000',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 1,
 'graph': {'A': [['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'function': {'python3': {'0': {'inline': "connect({0[i0]}, 'A', "
                                                        "'B', random(), "
                                                        'random())'}}},
               'name': 'GCB-GCA connection with random fractional offsets'},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 1,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'b3426a0b5077c14d09c2eb091e8ba0ded68486890d5f0146cfdec34ebbe383d6'}
'''
def gc_b3426a0b5077c14d09c2eb091e8ba0ded68486890d5f0146cfdec34ebbe383d6(i):
	return (connect(i[0], 'A', 'B', random(), random()),)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:45.086937Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'fcba468768bf701a1234ea41739916b0655512c74c74e5930cae35d13b92925f',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0], ['I', 1]], 'O': [['A', 0]]},
 'meta_data': {'parents': [['fcba468768bf701a1234ea41739916b0655512c74c74e5930cae35d13b92925f']]},
 'num_codes': 1,
 'num_inputs': 2,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '282424295de4addaa42b8117a6e53ce0136fcfba2b1cdfab61ac3c7e3a823516'}
'''
def gc_282424295de4addaa42b8117a6e53ce0136fcfba2b1cdfab61ac3c7e3a823516(i):
	a = gc_fcba468768bf701a1234ea41739916b0655512c74c74e5930cae35d13b92925f((i[0], i[1],))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:45.045221Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '81b5a567e50cf6fd71bfcfc3c5d23faa0f245fb0a71900fa9573eba1a94ee80d',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'parents': [['81b5a567e50cf6fd71bfcfc3c5d23faa0f245fb0a71900fa9573eba1a94ee80d']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'b98b16eb6649388de0a5294dcbde704470050a9c23850db69a1b239bd6788ee6'}
'''
def gc_b98b16eb6649388de0a5294dcbde704470050a9c23850db69a1b239bd6788ee6(i):
	a = gc_81b5a567e50cf6fd71bfcfc3c5d23faa0f245fb0a71900fa9573eba1a94ee80d((i[0],))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:45.002726Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'f131f1d7c087d2b567acec3f2a476de27b9110e0794c11b2c97098e878feed08',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'parents': [['f131f1d7c087d2b567acec3f2a476de27b9110e0794c11b2c97098e878feed08']]},
 'num_codes': 1,
 'num_inputs': 0,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'aab332740bb7b6730311c956b05c16d19814c2d752e1db38b65aa95c7b9209d7'}
'''
def gc_aab332740bb7b6730311c956b05c16d19814c2d752e1db38b65aa95c7b9209d7(i):
	a = gc_f131f1d7c087d2b567acec3f2a476de27b9110e0794c11b2c97098e878feed08((0.0, 0.0, 0.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:44.959186Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '23c441e967ef4b8637554409522bc07c1d0faac129bccf73473c098650a63957',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'parents': [['23c441e967ef4b8637554409522bc07c1d0faac129bccf73473c098650a63957']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '3669b2f53208e322423da38d8006444917940ddfedbf169eaf0212c0fe6f10b7'}
'''
def gc_3669b2f53208e322423da38d8006444917940ddfedbf169eaf0212c0fe6f10b7(i):
	a = gc_23c441e967ef4b8637554409522bc07c1d0faac129bccf73473c098650a63957((i[0], 0.0, 0.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:44.922374Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '5f1ff9bfaf9bc1cdb5d520bd056048ebe5467cc6580f03b9c0c29b7eb64c4d2b',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'parents': [['5f1ff9bfaf9bc1cdb5d520bd056048ebe5467cc6580f03b9c0c29b7eb64c4d2b']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'cc7cfb52a4658ba440bd7691c5a3d6f736f94d3d795857725a2e400f9e3624a9'}
'''
def gc_cc7cfb52a4658ba440bd7691c5a3d6f736f94d3d795857725a2e400f9e3624a9(i):
	a = gc_5f1ff9bfaf9bc1cdb5d520bd056048ebe5467cc6580f03b9c0c29b7eb64c4d2b((i[0], 0.0, 0.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:44.833983Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '4793e082e2462b3ed47a23c000e9e8165bf7b6dea9bde08182b7203a708f6214',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'parents': [['4793e082e2462b3ed47a23c000e9e8165bf7b6dea9bde08182b7203a708f6214']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'f5b607832778f539c313b5dbe664e0cdbaf016bcdba4ac95d45c54f999e08a4f'}
'''
def gc_f5b607832778f539c313b5dbe664e0cdbaf016bcdba4ac95d45c54f999e08a4f(i):
	a = gc_4793e082e2462b3ed47a23c000e9e8165bf7b6dea9bde08182b7203a708f6214((i[0],))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:45.999753Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'c436ba9675317cfa2b5e32a3f00cf08b57295e06f28d5203fbaa1cd6b430e6d7',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'parents': [['c436ba9675317cfa2b5e32a3f00cf08b57295e06f28d5203fbaa1cd6b430e6d7']]},
 'num_codes': 1,
 'num_inputs': 0,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'de16d05c96f141351c6e918906ad8565426b05c77a187edc20763c01f4d8db86'}
'''
def gc_de16d05c96f141351c6e918906ad8565426b05c77a187edc20763c01f4d8db86(i):
	a = gc_c436ba9675317cfa2b5e32a3f00cf08b57295e06f28d5203fbaa1cd6b430e6d7((0.0, 0.0, 0.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:45.927752Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '4f54b44dd522c044b41833089ca47ece6b280ff8c11324a5b8b6a957d92f6de8',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 1], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'parents': [['4f54b44dd522c044b41833089ca47ece6b280ff8c11324a5b8b6a957d92f6de8']]},
 'num_codes': 1,
 'num_inputs': 0,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '63f4c2177ea134118ee0d3b75c8a1e48a85dbb4214bcf0abf70b44241329f23c'}
'''
def gc_63f4c2177ea134118ee0d3b75c8a1e48a85dbb4214bcf0abf70b44241329f23c(i):
	a = gc_4f54b44dd522c044b41833089ca47ece6b280ff8c11324a5b8b6a957d92f6de8((0.0, 0.0, 0.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:46.576239Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'ea549df0fcde3b6375528205fef6eea94b79a442fd8afa77905fbeab96c6bcea',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0], ['I', 1]], 'O': [['A', 0]]},
 'meta_data': {'parents': [['ea549df0fcde3b6375528205fef6eea94b79a442fd8afa77905fbeab96c6bcea']]},
 'num_codes': 1,
 'num_inputs': 2,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '8568fa49a69fc9c42c30d78866a45316976afca26ce6a75284546f07ad9f6aef'}
'''
def gc_8568fa49a69fc9c42c30d78866a45316976afca26ce6a75284546f07ad9f6aef(i):
	a = gc_ea549df0fcde3b6375528205fef6eea94b79a442fd8afa77905fbeab96c6bcea((i[0], i[1],))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:46.515385Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'ee2cc4658d03ebb3ffbcdc44d31fa89b7644a654567d66b93bac5f6186899d4d',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'parents': [['ee2cc4658d03ebb3ffbcdc44d31fa89b7644a654567d66b93bac5f6186899d4d']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '0b71cf0dd17adf2126959c3712c97c25420a33cb71657225c3d76c127a2d3f8d'}
'''
def gc_0b71cf0dd17adf2126959c3712c97c25420a33cb71657225c3d76c127a2d3f8d(i):
	a = gc_ee2cc4658d03ebb3ffbcdc44d31fa89b7644a654567d66b93bac5f6186899d4d((i[0], 0.0, 0.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:46.480136Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'f131f1d7c087d2b567acec3f2a476de27b9110e0794c11b2c97098e878feed08',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'parents': [['f131f1d7c087d2b567acec3f2a476de27b9110e0794c11b2c97098e878feed08']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '065c6b174b50d8682b49d71112febf3f052ad94f794cef68009887ae1bc09b69'}
'''
def gc_065c6b174b50d8682b49d71112febf3f052ad94f794cef68009887ae1bc09b69(i):
	a = gc_f131f1d7c087d2b567acec3f2a476de27b9110e0794c11b2c97098e878feed08((i[0], 0.0, 0.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:46.398723Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '4cde93184158819b805ef591641fad84f4c0ee4fdb2715d267cbbcce1a53f8a4',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'parents': [['4cde93184158819b805ef591641fad84f4c0ee4fdb2715d267cbbcce1a53f8a4']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'a380199b1efb5e06e8bf0ba253f2250b665534df9402e9ba08405876a9d0911b'}
'''
def gc_a380199b1efb5e06e8bf0ba253f2250b665534df9402e9ba08405876a9d0911b(i):
	a = gc_4cde93184158819b805ef591641fad84f4c0ee4fdb2715d267cbbcce1a53f8a4((i[0],))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:46.313539Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'bcf49ecb02279621bc1dd9d70265175f142ccfcc742ff07cf3983c830c4670fc',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'parents': [['bcf49ecb02279621bc1dd9d70265175f142ccfcc742ff07cf3983c830c4670fc']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '15351a2e310bb0e2f6189d1728d5eee750c673dcb0b15c0f40302c6ef4e33535'}
'''
def gc_15351a2e310bb0e2f6189d1728d5eee750c673dcb0b15c0f40302c6ef4e33535(i):
	a = gc_bcf49ecb02279621bc1dd9d70265175f142ccfcc742ff07cf3983c830c4670fc((i[0],))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:46.234992Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '278ddaaaa439429bad68df4b81f3b42ecdc7cf2d2ea8ad086a2ca185a3acbbb6',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0]], 'C': [0.0], 'O': [['A', 0]]},
 'meta_data': {'parents': [['278ddaaaa439429bad68df4b81f3b42ecdc7cf2d2ea8ad086a2ca185a3acbbb6']]},
 'num_codes': 1,
 'num_inputs': 0,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '8e63d58261949359d0c4f000d50406d5c5df57a1809ca623baa7940a1ac1c84a'}
'''
def gc_8e63d58261949359d0c4f000d50406d5c5df57a1809ca623baa7940a1ac1c84a(i):
	a = gc_278ddaaaa439429bad68df4b81f3b42ecdc7cf2d2ea8ad086a2ca185a3acbbb6((0.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:47.282471Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'ce4e58fcbe55e5caf14c456fd2603a7d81c19e89e61e63b0e56f8c1958ba3da1',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0], ['I', 1]], 'O': [['A', 0]]},
 'meta_data': {'parents': [['ce4e58fcbe55e5caf14c456fd2603a7d81c19e89e61e63b0e56f8c1958ba3da1']]},
 'num_codes': 1,
 'num_inputs': 2,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': True,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': False},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '66ac33a3f469fe70a0c72886b61ccd32f2b9b4738c8dd22112ba9e47ebe4ff2b'}
'''
def gc_66ac33a3f469fe70a0c72886b61ccd32f2b9b4738c8dd22112ba9e47ebe4ff2b(i):
	a = gc_ce4e58fcbe55e5caf14c456fd2603a7d81c19e89e61e63b0e56f8c1958ba3da1((i[0], i[1],))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:47.213333Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'b4dc32c9bc15e51d8070be7bf0ee9bfc344b73cc8ec857978ff72e71a3efb911',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'parents': [['b4dc32c9bc15e51d8070be7bf0ee9bfc344b73cc8ec857978ff72e71a3efb911']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '69f8bddf1ba8386b128c82b9e9d61bfbcd39a2adfb0f072e1c0edd6fc96c2b5e'}
'''
def gc_69f8bddf1ba8386b128c82b9e9d61bfbcd39a2adfb0f072e1c0edd6fc96c2b5e(i):
	a = gc_b4dc32c9bc15e51d8070be7bf0ee9bfc344b73cc8ec857978ff72e71a3efb911((i[0], 0.0, 0.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:47.004854Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '6bba0589ed454784e75f8a184fb8fc8d59a3772e73a8414f2ba915ce211f6773',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'parents': [['6bba0589ed454784e75f8a184fb8fc8d59a3772e73a8414f2ba915ce211f6773']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '572f3d56521fb576738b38239b46b1f2e4f881dbeb18ba57b3254a6dceb5782e'}
'''
def gc_572f3d56521fb576738b38239b46b1f2e4f881dbeb18ba57b3254a6dceb5782e(i):
	a = gc_6bba0589ed454784e75f8a184fb8fc8d59a3772e73a8414f2ba915ce211f6773((i[0],))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:48.162033Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '4140f47e72adf3343c04c82d7766bf9e3bc71a6b606b7bc2e93f45a6349792e5',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0], ['I', 1]], 'O': [['A', 0]]},
 'meta_data': {'parents': [['4140f47e72adf3343c04c82d7766bf9e3bc71a6b606b7bc2e93f45a6349792e5']]},
 'num_codes': 1,
 'num_inputs': 2,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'b33df5beef7cd7d5e49e74b229864ba0664bae07dbe6a28a3c9c11643518f37d'}
'''
def gc_b33df5beef7cd7d5e49e74b229864ba0664bae07dbe6a28a3c9c11643518f37d(i):
	a = gc_4140f47e72adf3343c04c82d7766bf9e3bc71a6b606b7bc2e93f45a6349792e5((i[0], i[1],))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:48.094573Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '7bb5eb204e326fbabe069fb824e88a6ca68ec34c39eaa05a4d271a3f92e4b4fd',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'parents': [['7bb5eb204e326fbabe069fb824e88a6ca68ec34c39eaa05a4d271a3f92e4b4fd']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '42bdabf6208e9529f50a37386efafc88a45bdd1ed90be29c97a18041626dba9b'}
'''
def gc_42bdabf6208e9529f50a37386efafc88a45bdd1ed90be29c97a18041626dba9b(i):
	a = gc_7bb5eb204e326fbabe069fb824e88a6ca68ec34c39eaa05a4d271a3f92e4b4fd((i[0],))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:48.043672Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'c436ba9675317cfa2b5e32a3f00cf08b57295e06f28d5203fbaa1cd6b430e6d7',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'parents': [['c436ba9675317cfa2b5e32a3f00cf08b57295e06f28d5203fbaa1cd6b430e6d7']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '7c81e32cacdeb941a0c6989d24d58a9591a9771cce66ec0752ebbd0b2e1f5eae'}
'''
def gc_7c81e32cacdeb941a0c6989d24d58a9591a9771cce66ec0752ebbd0b2e1f5eae(i):
	a = gc_c436ba9675317cfa2b5e32a3f00cf08b57295e06f28d5203fbaa1cd6b430e6d7((i[0], 0.0, 0.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:49.053697Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '102a4d1fc747c5f81b314937da02b830ca4a49a6010aa65fd478dd1bd68675e8',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'parents': [['102a4d1fc747c5f81b314937da02b830ca4a49a6010aa65fd478dd1bd68675e8']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '5e518b6b4668611c3d1602f784ad410609d5657a5d5690f9abca54eb4b7c0f3a'}
'''
def gc_5e518b6b4668611c3d1602f784ad410609d5657a5d5690f9abca54eb4b7c0f3a(i):
	a = gc_102a4d1fc747c5f81b314937da02b830ca4a49a6010aa65fd478dd1bd68675e8((i[0],))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:48.791218Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '23c441e967ef4b8637554409522bc07c1d0faac129bccf73473c098650a63957',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0], ['C', 0], ['I', 0]], 'C': [0.0], 'O': [['A', 0]]},
 'meta_data': {'parents': [['23c441e967ef4b8637554409522bc07c1d0faac129bccf73473c098650a63957']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'a0429192b8ead5be37fc2c644a9ed57cf4a9eaf2a10c9fe225a6e39a204b5e16'}
'''
def gc_a0429192b8ead5be37fc2c644a9ed57cf4a9eaf2a10c9fe225a6e39a204b5e16(i):
	a = gc_23c441e967ef4b8637554409522bc07c1d0faac129bccf73473c098650a63957((i[0], 0.0, i[0],))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:48.756988Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'a95ea10e7327badf07045086c7e935f5cc66a9b47f323fcdf30d76f66a592829',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0], ['I', 0], ['C', 0]], 'C': [0.0], 'O': [['A', 0]]},
 'meta_data': {'parents': [['a95ea10e7327badf07045086c7e935f5cc66a9b47f323fcdf30d76f66a592829']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'bf3161b1d66c4f7b2c4d7c9901bd0044d3dcb0e2bc05dbe82e1feeeb40ef9931'}
'''
def gc_bf3161b1d66c4f7b2c4d7c9901bd0044d3dcb0e2bc05dbe82e1feeeb40ef9931(i):
	a = gc_a95ea10e7327badf07045086c7e935f5cc66a9b47f323fcdf30d76f66a592829((i[0], i[0], 0.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:50.962542Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '4f54b44dd522c044b41833089ca47ece6b280ff8c11324a5b8b6a957d92f6de8',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'parents': [['4f54b44dd522c044b41833089ca47ece6b280ff8c11324a5b8b6a957d92f6de8']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'cf8cd9075b571cb5a59d37e378029ff54502df66779163ba058c01384f335c2c'}
'''
def gc_cf8cd9075b571cb5a59d37e378029ff54502df66779163ba058c01384f335c2c(i):
	a = gc_4f54b44dd522c044b41833089ca47ece6b280ff8c11324a5b8b6a957d92f6de8((i[0], 0.0, 0.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:50.876654Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '81d83b6dfe8764bc32df13948a86e7721818e3648d8f916708f8d416b2b94370',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'parents': [['81d83b6dfe8764bc32df13948a86e7721818e3648d8f916708f8d416b2b94370']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '65205972c2842865c3b8de9cd43d117c8bc0ff4fc05f27284d93416cd604dcf4'}
'''
def gc_65205972c2842865c3b8de9cd43d117c8bc0ff4fc05f27284d93416cd604dcf4(i):
	a = gc_81d83b6dfe8764bc32df13948a86e7721818e3648d8f916708f8d416b2b94370((i[0],))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:50.790871Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '81b5a567e50cf6fd71bfcfc3c5d23faa0f245fb0a71900fa9573eba1a94ee80d',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0]], 'C': [-1.0], 'O': [['A', 0]]},
 'meta_data': {'parents': [['81b5a567e50cf6fd71bfcfc3c5d23faa0f245fb0a71900fa9573eba1a94ee80d']]},
 'num_codes': 1,
 'num_inputs': 0,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '7eb61a64d6aa1248cf7c1973ece726698b4d3b61964060a46a9789bda79d7c72'}
'''
def gc_7eb61a64d6aa1248cf7c1973ece726698b4d3b61964060a46a9789bda79d7c72(i):
	a = gc_81b5a567e50cf6fd71bfcfc3c5d23faa0f245fb0a71900fa9573eba1a94ee80d((-1.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:50.686983Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'e279714512f0498ee888c84f1906de2a5e6bf082d60fdbb32de84a0c16f6f071',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'parents': [['e279714512f0498ee888c84f1906de2a5e6bf082d60fdbb32de84a0c16f6f071']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'db707d1e30841606ccbc7f7d349dcdadcf7b3b5e1e8d1a2e8cec17e1317bfd13'}
'''
def gc_db707d1e30841606ccbc7f7d349dcdadcf7b3b5e1e8d1a2e8cec17e1317bfd13(i):
	a = gc_e279714512f0498ee888c84f1906de2a5e6bf082d60fdbb32de84a0c16f6f071((i[0],))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:50.175609Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '4793e082e2462b3ed47a23c000e9e8165bf7b6dea9bde08182b7203a708f6214',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0]], 'C': [0.63940154460376], 'O': [['A', 0]]},
 'meta_data': {'parents': [['f5b607832778f539c313b5dbe664e0cdbaf016bcdba4ac95d45c54f999e08a4f']]},
 'num_codes': 1,
 'num_inputs': 0,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'afa54e4b4caac53b34964c353bec7a56c8f8a41a501e37afe3a2f0237968b97e'}
'''
def gc_afa54e4b4caac53b34964c353bec7a56c8f8a41a501e37afe3a2f0237968b97e(i):
	a = gc_4793e082e2462b3ed47a23c000e9e8165bf7b6dea9bde08182b7203a708f6214((0.63940154460376,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:50.046057Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '63971bfb77792f35cda0463d310e2724ae108354fb287df386ab88a752743fcc',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'parents': [['63971bfb77792f35cda0463d310e2724ae108354fb287df386ab88a752743fcc']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '562f9ffb473aade86537c9d78a94314f32cc0e1e6a5c71926777777c5fd35bbf'}
'''
def gc_562f9ffb473aade86537c9d78a94314f32cc0e1e6a5c71926777777c5fd35bbf(i):
	a = gc_63971bfb77792f35cda0463d310e2724ae108354fb287df386ab88a752743fcc((i[0],))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:49.731821Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '4f54b44dd522c044b41833089ca47ece6b280ff8c11324a5b8b6a957d92f6de8',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0], ['I', 0], ['C', 0]], 'C': [0.0], 'O': [['A', 0]]},
 'meta_data': {'parents': [['4f54b44dd522c044b41833089ca47ece6b280ff8c11324a5b8b6a957d92f6de8']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '67aa64f950ed976c1835461b09f7aee23a9ef5508d2a06d7b02e026b32f4134a'}
'''
def gc_67aa64f950ed976c1835461b09f7aee23a9ef5508d2a06d7b02e026b32f4134a(i):
	a = gc_4f54b44dd522c044b41833089ca47ece6b280ff8c11324a5b8b6a957d92f6de8((i[0], i[0], 0.0,))
	return (a[0],)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:44.042046Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '0000000000000000000000000000000000000000000000000000000000000000',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 1,
 'graph': {'A': [['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'function': {'python3': {'0': {'inline': "connect({0[i0]}, 'C', "
                                                        "'A', random(), "
                                                        'random())'}}},
               'name': 'GCA-constant connection with random fractional '
                       'offsets'},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 1,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '102a4d1fc747c5f81b314937da02b830ca4a49a6010aa65fd478dd1bd68675e8'}
'''
def gc_102a4d1fc747c5f81b314937da02b830ca4a49a6010aa65fd478dd1bd68675e8(i):
	return (connect(i[0], 'C', 'A', random(), random()),)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:44.061054Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '0000000000000000000000000000000000000000000000000000000000000000',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 1,
 'graph': {'A': [['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'function': {'python3': {'0': {'inline': "connect({0[i0]}, 'I', "
                                                        "'B', random(), "
                                                        'random())'}}},
               'name': 'GCB-input connection with random fractional offsets'},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 1,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '81d83b6dfe8764bc32df13948a86e7721818e3648d8f916708f8d416b2b94370'}
'''
def gc_81d83b6dfe8764bc32df13948a86e7721818e3648d8f916708f8d416b2b94370(i):
	return (connect(i[0], 'I', 'B', random(), random()),)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:44.117988Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '0000000000000000000000000000000000000000000000000000000000000000',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 1,
 'graph': {'A': [['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'function': {'python3': {'0': {'inline': "connect({0[i0]}, 'I', "
                                                        "'O', random(), "
                                                        'random())'}}},
               'name': 'Output-input connection with random fractional '
                       'offsets'},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 1,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '6bba0589ed454784e75f8a184fb8fc8d59a3772e73a8414f2ba915ce211f6773'}
'''
def gc_6bba0589ed454784e75f8a184fb8fc8d59a3772e73a8414f2ba915ce211f6773(i):
	return (connect(i[0], 'I', 'O', random(), random()),)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:44.137077Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '0000000000000000000000000000000000000000000000000000000000000000',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 1,
 'graph': {'A': [['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'function': {'python3': {'0': {'inline': "connect({0[i0]}, 'A', "
                                                        "'O', random(), "
                                                        'random())'}}},
               'name': 'Output-GCA connection with random fractional offsets'},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 1,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '4793e082e2462b3ed47a23c000e9e8165bf7b6dea9bde08182b7203a708f6214'}
'''
def gc_4793e082e2462b3ed47a23c000e9e8165bf7b6dea9bde08182b7203a708f6214(i):
	return (connect(i[0], 'A', 'O', random(), random()),)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:44.156605Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '0000000000000000000000000000000000000000000000000000000000000000',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 1,
 'graph': {'A': [['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'function': {'python3': {'0': {'inline': "connect({0[i0]}, 'C', "
                                                        "'O', random(), "
                                                        'random())'}}},
               'name': 'Output-constant connection with random fractional '
                       'offsets'},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 1,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '63971bfb77792f35cda0463d310e2724ae108354fb287df386ab88a752743fcc'}
'''
def gc_63971bfb77792f35cda0463d310e2724ae108354fb287df386ab88a752743fcc(i):
	return (connect(i[0], 'C', 'O', random(), random()),)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:44.176071Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '0000000000000000000000000000000000000000000000000000000000000000',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 1,
 'graph': {'A': [['I', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'function': {'python3': {'0': {'inline': "connect({0[i0]}, 'I', "
                                                        "'C', {0[c0]}, "
                                                        '{0[c1]})'}}},
               'name': 'GCA-input connection with constant fractional offsets'},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 1,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'a95ea10e7327badf07045086c7e935f5cc66a9b47f323fcdf30d76f66a592829'}
'''
def gc_a95ea10e7327badf07045086c7e935f5cc66a9b47f323fcdf30d76f66a592829(i):
	return (connect(i[0], 'I', 'C', 0.0, 0.0),)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:44.195624Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '0000000000000000000000000000000000000000000000000000000000000000',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 1,
 'graph': {'A': [['I', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'function': {'python3': {'0': {'inline': "connect({0[i0]}, 'C', "
                                                        "'A', {0[c0]}, "
                                                        '{0[c1]})'}}},
               'name': 'GCA-constant connection with constant fractional '
                       'offsets'},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 1,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '4f54b44dd522c044b41833089ca47ece6b280ff8c11324a5b8b6a957d92f6de8'}
'''
def gc_4f54b44dd522c044b41833089ca47ece6b280ff8c11324a5b8b6a957d92f6de8(i):
	return (connect(i[0], 'C', 'A', 0.0, 0.0),)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:44.254348Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '0000000000000000000000000000000000000000000000000000000000000000',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 1,
 'graph': {'A': [['I', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'function': {'python3': {'0': {'inline': "connect({0[i0]}, 'C', "
                                                        "'B', {0[c0]}, "
                                                        '{0[c1]})'}}},
               'name': 'GCB-constant connection with constant fractional '
                       'offsets'},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 1,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'c436ba9675317cfa2b5e32a3f00cf08b57295e06f28d5203fbaa1cd6b430e6d7'}
'''
def gc_c436ba9675317cfa2b5e32a3f00cf08b57295e06f28d5203fbaa1cd6b430e6d7(i):
	return (connect(i[0], 'C', 'B', 0.0, 0.0),)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:44.274756Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '0000000000000000000000000000000000000000000000000000000000000000',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 1,
 'graph': {'A': [['I', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'function': {'python3': {'0': {'inline': "connect({0[i0]}, 'I', "
                                                        "'O', {0[c0]}, "
                                                        '{0[c1]})'}}},
               'name': 'Output-input connection with constant fractional '
                       'offsets'},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 1,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'b4dc32c9bc15e51d8070be7bf0ee9bfc344b73cc8ec857978ff72e71a3efb911'}
'''
def gc_b4dc32c9bc15e51d8070be7bf0ee9bfc344b73cc8ec857978ff72e71a3efb911(i):
	return (connect(i[0], 'I', 'O', 0.0, 0.0),)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:44.293938Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '0000000000000000000000000000000000000000000000000000000000000000',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 1,
 'graph': {'A': [['I', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'function': {'python3': {'0': {'inline': "connect({0[i0]}, 'A', "
                                                        "'O', {0[c0]}, "
                                                        '{0[c1]})'}}},
               'name': 'Output-GCA connection with constant fractional '
                       'offsets'},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 1,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'f131f1d7c087d2b567acec3f2a476de27b9110e0794c11b2c97098e878feed08'}
'''
def gc_f131f1d7c087d2b567acec3f2a476de27b9110e0794c11b2c97098e878feed08(i):
	return (connect(i[0], 'A', 'O', 0.0, 0.0),)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:44.313303Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '0000000000000000000000000000000000000000000000000000000000000000',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 1,
 'graph': {'A': [['I', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'function': {'python3': {'0': {'inline': "connect({0[i0]}, 'C', "
                                                        "'O', {0[c0]}, "
                                                        '{0[c1]})'}}},
               'name': 'Output-constant connection with constant fractional '
                       'offsets'},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 1,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'ee2cc4658d03ebb3ffbcdc44d31fa89b7644a654567d66b93bac5f6186899d4d'}
'''
def gc_ee2cc4658d03ebb3ffbcdc44d31fa89b7644a654567d66b93bac5f6186899d4d(i):
	return (connect(i[0], 'C', 'O', 0.0, 0.0),)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:44.332305Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '0000000000000000000000000000000000000000000000000000000000000000',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 1,
 'graph': {'A': [['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'function': {'python3': {'0': {'inline': 'append_constant({0[i0]}, '
                                                        'uniform(-1.0, '
                                                        '1.0))'}}},
               'name': 'New constant: Random -1.0 to 1.0'},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 1,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'e279714512f0498ee888c84f1906de2a5e6bf082d60fdbb32de84a0c16f6f071'}
'''
def gc_e279714512f0498ee888c84f1906de2a5e6bf082d60fdbb32de84a0c16f6f071(i):
	return (append_constant(i[0], uniform(-1.0, 1.0)),)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:44.351029Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '0000000000000000000000000000000000000000000000000000000000000000',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 1,
 'graph': {'A': [['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'function': {'python3': {'0': {'inline': 'append_constant({0[i0]}, '
                                                        '1.0)'}}},
               'name': 'New constant: 1.0'},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 1,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '7bb5eb204e326fbabe069fb824e88a6ca68ec34c39eaa05a4d271a3f92e4b4fd'}
'''
def gc_7bb5eb204e326fbabe069fb824e88a6ca68ec34c39eaa05a4d271a3f92e4b4fd(i):
	return (append_constant(i[0], 1.0),)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:44.408511Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '0000000000000000000000000000000000000000000000000000000000000000',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 1,
 'graph': {'A': [['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'function': {'python3': {'0': {'inline': 'remove_constant({0[i0]}, '
                                                        'random())'}}},
               'name': 'Remove constant with random offset'},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 1,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'bcf49ecb02279621bc1dd9d70265175f142ccfcc742ff07cf3983c830c4670fc'}
'''
def gc_bcf49ecb02279621bc1dd9d70265175f142ccfcc742ff07cf3983c830c4670fc(i):
	return (remove_constant(i[0], random()),)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:44.427737Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '0000000000000000000000000000000000000000000000000000000000000000',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 1,
 'graph': {'A': [['I', 0], ['I', 1]], 'O': [['A', 0]]},
 'meta_data': {'function': {'python3': {'0': {'inline': 'mutate_constant({0[i0]}, '
                                                        '{0[i1]}, 1.5)'}}},
               'name': 'Mutate constant: +50%'},
 'num_codes': 1,
 'num_inputs': 2,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 1,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'ea549df0fcde3b6375528205fef6eea94b79a442fd8afa77905fbeab96c6bcea'}
'''
def gc_ea549df0fcde3b6375528205fef6eea94b79a442fd8afa77905fbeab96c6bcea(i):
	return (mutate_constant(i[0], i[1], 1.5),)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:44.448360Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '0000000000000000000000000000000000000000000000000000000000000000',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 1,
 'graph': {'A': [['I', 0], ['I', 1]], 'O': [['A', 0]]},
 'meta_data': {'function': {'python3': {'0': {'inline': 'mutate_constant({0[i0]}, '
                                                        '{0[i1]}, 0.5)'}}},
               'name': 'Mutate constant: -50%'},
 'num_codes': 1,
 'num_inputs': 2,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 1,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'fcba468768bf701a1234ea41739916b0655512c74c74e5930cae35d13b92925f'}
'''
def gc_fcba468768bf701a1234ea41739916b0655512c74c74e5930cae35d13b92925f(i):
	return (mutate_constant(i[0], i[1], 0.5),)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:44.467937Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '0000000000000000000000000000000000000000000000000000000000000000',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 1,
 'graph': {'A': [['I', 0], ['I', 1]], 'O': [['A', 0]]},
 'meta_data': {'function': {'python3': {'0': {'inline': 'mutate_constant({0[i0]}, '
                                                        '{0[i1]}, -1.0)'}}},
               'name': 'Mutate constant: Negate'},
 'num_codes': 1,
 'num_inputs': 2,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 1,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '4140f47e72adf3343c04c82d7766bf9e3bc71a6b606b7bc2e93f45a6349792e5'}
'''
def gc_4140f47e72adf3343c04c82d7766bf9e3bc71a6b606b7bc2e93f45a6349792e5(i):
	return (mutate_constant(i[0], i[1], -1.0),)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:44.487233Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '0000000000000000000000000000000000000000000000000000000000000000',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 1,
 'graph': {'A': [['I', 0], ['I', 1]], 'O': [['A', 0]]},
 'meta_data': {'function': {'python3': {'0': {'inline': 'stack({0[i0]}, '
                                                        '{0[i1]})'}}},
               'name': 'Stack'},
 'num_codes': 1,
 'num_inputs': 2,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 1,
 'properties': {'binary_mutation': True,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': False},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'ce4e58fcbe55e5caf14c456fd2603a7d81c19e89e61e63b0e56f8c1958ba3da1'}
'''
def gc_ce4e58fcbe55e5caf14c456fd2603a7d81c19e89e61e63b0e56f8c1958ba3da1(i):
	return (stack(i[0], i[1]),)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:53.075365Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'e279714512f0498ee888c84f1906de2a5e6bf082d60fdbb32de84a0c16f6f071',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0]], 'C': [1.0], 'O': [['A', 0]]},
 'meta_data': {'parents': [['e279714512f0498ee888c84f1906de2a5e6bf082d60fdbb32de84a0c16f6f071']]},
 'num_codes': 1,
 'num_inputs': 0,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'ce171d8207600a6c5b494439f1af004fb58b93f4051e75a05ef354e360cf2fe3'}
'''
def gc_ce171d8207600a6c5b494439f1af004fb58b93f4051e75a05ef354e360cf2fe3(i):
	a = gc_e279714512f0498ee888c84f1906de2a5e6bf082d60fdbb32de84a0c16f6f071((1.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:52.623651Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '23c441e967ef4b8637554409522bc07c1d0faac129bccf73473c098650a63957',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0], ['C', 0], ['I', 0]], 'C': [0.0], 'O': [['A', 0]]},
 'meta_data': {'parents': [['a0429192b8ead5be37fc2c644a9ed57cf4a9eaf2a10c9fe225a6e39a204b5e16']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'aa04da1966f1433e73396dd5c16b8deb59e0104cdbc1f0a41aa021a3aad22268'}
'''
def gc_aa04da1966f1433e73396dd5c16b8deb59e0104cdbc1f0a41aa021a3aad22268(i):
	a = gc_23c441e967ef4b8637554409522bc07c1d0faac129bccf73473c098650a63957((0.0, 0.0, i[0],))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:52.395936Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'bcf49ecb02279621bc1dd9d70265175f142ccfcc742ff07cf3983c830c4670fc',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0]], 'C': [1.0], 'O': [['A', 0]]},
 'meta_data': {'parents': [['bcf49ecb02279621bc1dd9d70265175f142ccfcc742ff07cf3983c830c4670fc']]},
 'num_codes': 1,
 'num_inputs': 0,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '75ff6e5392d8ac373c8b0445027b904ffd1a62b19774a2326aa1e596049ca132'}
'''
def gc_75ff6e5392d8ac373c8b0445027b904ffd1a62b19774a2326aa1e596049ca132(i):
	a = gc_bcf49ecb02279621bc1dd9d70265175f142ccfcc742ff07cf3983c830c4670fc((1.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:52.352474Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '23c441e967ef4b8637554409522bc07c1d0faac129bccf73473c098650a63957',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0], ['I', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'parents': [['23c441e967ef4b8637554409522bc07c1d0faac129bccf73473c098650a63957']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '986ae757be6910ae3b92411b03d2f9feace48fe748d96a7933f98b0ca9d5e3c9'}
'''
def gc_986ae757be6910ae3b92411b03d2f9feace48fe748d96a7933f98b0ca9d5e3c9(i):
	a = gc_23c441e967ef4b8637554409522bc07c1d0faac129bccf73473c098650a63957((0.0, i[0], 0.0,))
	return (a[0],)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:44.389566Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '0000000000000000000000000000000000000000000000000000000000000000',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 1,
 'graph': {'A': [['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'function': {'python3': {'0': {'inline': 'append_constant({0[i0]}, '
                                                        '0.0)'}}},
               'name': 'New constant: 0.0'},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 1,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '81b5a567e50cf6fd71bfcfc3c5d23faa0f245fb0a71900fa9573eba1a94ee80d'}
'''
def gc_81b5a567e50cf6fd71bfcfc3c5d23faa0f245fb0a71900fa9573eba1a94ee80d(i):
	return (append_constant(i[0], 0.0),)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:54.740354Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'bcf49ecb02279621bc1dd9d70265175f142ccfcc742ff07cf3983c830c4670fc',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0]], 'C': [0.0], 'O': [['A', 0]]},
 'meta_data': {'parents': [['bcf49ecb02279621bc1dd9d70265175f142ccfcc742ff07cf3983c830c4670fc']]},
 'num_codes': 1,
 'num_inputs': 0,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '6583b66e7cb73e5c773e7700cb4485a2b81d4ce942220fbc65ef67b99589ca08'}
'''
def gc_6583b66e7cb73e5c773e7700cb4485a2b81d4ce942220fbc65ef67b99589ca08(i):
	a = gc_bcf49ecb02279621bc1dd9d70265175f142ccfcc742ff07cf3983c830c4670fc((0.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:54.539880Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '63971bfb77792f35cda0463d310e2724ae108354fb287df386ab88a752743fcc',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0]], 'C': [-1.0], 'O': [['A', 0]]},
 'meta_data': {'parents': [['63971bfb77792f35cda0463d310e2724ae108354fb287df386ab88a752743fcc']]},
 'num_codes': 1,
 'num_inputs': 0,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '0377050cd3534281ac885213d141494d2ea6ce8b50f787f224a6dc65ecb90e10'}
'''
def gc_0377050cd3534281ac885213d141494d2ea6ce8b50f787f224a6dc65ecb90e10(i):
	a = gc_63971bfb77792f35cda0463d310e2724ae108354fb287df386ab88a752743fcc((-1.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:54.146820Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '6bba0589ed454784e75f8a184fb8fc8d59a3772e73a8414f2ba915ce211f6773',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0]], 'C': [0.0], 'O': [['A', 0]]},
 'meta_data': {'parents': [['6bba0589ed454784e75f8a184fb8fc8d59a3772e73a8414f2ba915ce211f6773']]},
 'num_codes': 1,
 'num_inputs': 0,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '731f9ff5e9cfdb53f1944bf6962c32b21be104ef51b2fdb3db0244b077010af2'}
'''
def gc_731f9ff5e9cfdb53f1944bf6962c32b21be104ef51b2fdb3db0244b077010af2(i):
	a = gc_6bba0589ed454784e75f8a184fb8fc8d59a3772e73a8414f2ba915ce211f6773((0.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:53.973717Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '81d83b6dfe8764bc32df13948a86e7721818e3648d8f916708f8d416b2b94370',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0]], 'C': [-0.8225245593482424], 'O': [['A', 0]]},
 'meta_data': {'parents': [['81d83b6dfe8764bc32df13948a86e7721818e3648d8f916708f8d416b2b94370']]},
 'num_codes': 1,
 'num_inputs': 0,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '18aefb88a3ddaf2056601643afd03be838c5c77317ca3b89c700e219db26e18c'}
'''
def gc_18aefb88a3ddaf2056601643afd03be838c5c77317ca3b89c700e219db26e18c(i):
	a = gc_81d83b6dfe8764bc32df13948a86e7721818e3648d8f916708f8d416b2b94370((-0.8225245593482424,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:56.462599Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '278ddaaaa439429bad68df4b81f3b42ecdc7cf2d2ea8ad086a2ca185a3acbbb6',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'parents': [['278ddaaaa439429bad68df4b81f3b42ecdc7cf2d2ea8ad086a2ca185a3acbbb6']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '5d180795babcb82e7ea8b4357ae602a44666c60f0d2b851051c89e1149e72f97'}
'''
def gc_5d180795babcb82e7ea8b4357ae602a44666c60f0d2b851051c89e1149e72f97(i):
	a = gc_278ddaaaa439429bad68df4b81f3b42ecdc7cf2d2ea8ad086a2ca185a3acbbb6((i[0],))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:56.342044Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '4793e082e2462b3ed47a23c000e9e8165bf7b6dea9bde08182b7203a708f6214',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0]], 'C': [0.0], 'O': [['A', 0]]},
 'meta_data': {'parents': [['4793e082e2462b3ed47a23c000e9e8165bf7b6dea9bde08182b7203a708f6214']]},
 'num_codes': 1,
 'num_inputs': 0,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '7743aba320d9a6dd5f2b7a8e5777b997d61131f2a4db0f78fb4a881d40244898'}
'''
def gc_7743aba320d9a6dd5f2b7a8e5777b997d61131f2a4db0f78fb4a881d40244898(i):
	a = gc_4793e082e2462b3ed47a23c000e9e8165bf7b6dea9bde08182b7203a708f6214((0.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:55.724426Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '5f1ff9bfaf9bc1cdb5d520bd056048ebe5467cc6580f03b9c0c29b7eb64c4d2b',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0], ['I', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'parents': [['cc7cfb52a4658ba440bd7691c5a3d6f736f94d3d795857725a2e400f9e3624a9']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '13b3b21f4b1e53f66075fa59d78dccab619d1f8e65a22bb82d9a68c347a212c6'}
'''
def gc_13b3b21f4b1e53f66075fa59d78dccab619d1f8e65a22bb82d9a68c347a212c6(i):
	a = gc_5f1ff9bfaf9bc1cdb5d520bd056048ebe5467cc6580f03b9c0c29b7eb64c4d2b((0.0, i[0], 0.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:57.183688Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'ea549df0fcde3b6375528205fef6eea94b79a442fd8afa77905fbeab96c6bcea',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0], ['C', 0]],
           'C': [0.9258937854313394],
           'O': [['A', 0]]},
 'meta_data': {'parents': [['8568fa49a69fc9c42c30d78866a45316976afca26ce6a75284546f07ad9f6aef']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'cb159d2420f0a661bcdd192ab4cfac4363d652f0ec3ac8ab69e84e33768b97ec'}
'''
def gc_cb159d2420f0a661bcdd192ab4cfac4363d652f0ec3ac8ab69e84e33768b97ec(i):
	a = gc_ea549df0fcde3b6375528205fef6eea94b79a442fd8afa77905fbeab96c6bcea((i[0], 0.9258937854313394,))
	return (a[0],)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:44.098931Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '0000000000000000000000000000000000000000000000000000000000000000',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 1,
 'graph': {'A': [['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'function': {'python3': {'0': {'inline': "connect({0[i0]}, 'C', "
                                                        "'B', random(), "
                                                        'random())'}}},
               'name': 'GCB-constant connection with random fractional '
                       'offsets'},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 1,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '278ddaaaa439429bad68df4b81f3b42ecdc7cf2d2ea8ad086a2ca185a3acbbb6'}
'''
def gc_278ddaaaa439429bad68df4b81f3b42ecdc7cf2d2ea8ad086a2ca185a3acbbb6(i):
	return (connect(i[0], 'C', 'B', random(), random()),)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:59.633086Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '5f1ff9bfaf9bc1cdb5d520bd056048ebe5467cc6580f03b9c0c29b7eb64c4d2b',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'parents': [['5f1ff9bfaf9bc1cdb5d520bd056048ebe5467cc6580f03b9c0c29b7eb64c4d2b']]},
 'num_codes': 1,
 'num_inputs': 0,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'd583313ac7265d903f96aebefac338b54f234df8c3250552bea73f53de7b4cfa'}
'''
def gc_d583313ac7265d903f96aebefac338b54f234df8c3250552bea73f53de7b4cfa(i):
	a = gc_5f1ff9bfaf9bc1cdb5d520bd056048ebe5467cc6580f03b9c0c29b7eb64c4d2b((0.0, 0.0, 0.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:59.494506Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '7404cd51f0ff21ae1b51cd8e13b6bacf706cafde670c9ef05ae282fea9ff2364',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'parents': [['7404cd51f0ff21ae1b51cd8e13b6bacf706cafde670c9ef05ae282fea9ff2364']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'f269bf2281717b6c6d4cd1c4f6bdd61dd63f8501ed8a3846b79dca9c82387a51'}
'''
def gc_f269bf2281717b6c6d4cd1c4f6bdd61dd63f8501ed8a3846b79dca9c82387a51(i):
	a = gc_7404cd51f0ff21ae1b51cd8e13b6bacf706cafde670c9ef05ae282fea9ff2364((i[0],))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:58.591615Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'e279714512f0498ee888c84f1906de2a5e6bf082d60fdbb32de84a0c16f6f071',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0]], 'C': [-1.0], 'O': [['A', 0]]},
 'meta_data': {'parents': [['e279714512f0498ee888c84f1906de2a5e6bf082d60fdbb32de84a0c16f6f071']]},
 'num_codes': 1,
 'num_inputs': 0,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '2a1a7136267b40ddef2589b706851cadea6ea3617c681bca44d915ca2c48c865'}
'''
def gc_2a1a7136267b40ddef2589b706851cadea6ea3617c681bca44d915ca2c48c865(i):
	a = gc_e279714512f0498ee888c84f1906de2a5e6bf082d60fdbb32de84a0c16f6f071((-1.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:26:00.941061Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'b3426a0b5077c14d09c2eb091e8ba0ded68486890d5f0146cfdec34ebbe383d6',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'parents': [['b3426a0b5077c14d09c2eb091e8ba0ded68486890d5f0146cfdec34ebbe383d6']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '57445022b9dc0d937721bb272de55001607f26c9b9cc9dd40cd4dead77da6366'}
'''
def gc_57445022b9dc0d937721bb272de55001607f26c9b9cc9dd40cd4dead77da6366(i):
	a = gc_b3426a0b5077c14d09c2eb091e8ba0ded68486890d5f0146cfdec34ebbe383d6((i[0],))
	return (a[0],)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:44.215255Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '0000000000000000000000000000000000000000000000000000000000000000',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 1,
 'graph': {'A': [['I', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'function': {'python3': {'0': {'inline': "connect({0[i0]}, 'I', "
                                                        "'B', {0[c0]}, "
                                                        '{0[c1]})'}}},
               'name': 'GCB-input connection with constant fractional offsets'},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 1,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '5f1ff9bfaf9bc1cdb5d520bd056048ebe5467cc6580f03b9c0c29b7eb64c4d2b'}
'''
def gc_5f1ff9bfaf9bc1cdb5d520bd056048ebe5467cc6580f03b9c0c29b7eb64c4d2b(i):
	return (connect(i[0], 'I', 'B', 0.0, 0.0),)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:26:02.188011Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'f131f1d7c087d2b567acec3f2a476de27b9110e0794c11b2c97098e878feed08',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 1], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'parents': [['aab332740bb7b6730311c956b05c16d19814c2d752e1db38b65aa95c7b9209d7']]},
 'num_codes': 1,
 'num_inputs': 0,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'd990e3a0af629cd2048c76bdc4dbfe12a93eb16e35ccf71818050b1a9c915ae2'}
'''
def gc_d990e3a0af629cd2048c76bdc4dbfe12a93eb16e35ccf71818050b1a9c915ae2(i):
	a = gc_f131f1d7c087d2b567acec3f2a476de27b9110e0794c11b2c97098e878feed08((0.0, 0.0, 0.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:26:01.853522Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '5f1ff9bfaf9bc1cdb5d520bd056048ebe5467cc6580f03b9c0c29b7eb64c4d2b',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0], ['I', 0], ['C', 0]], 'C': [0.0], 'O': [['A', 0]]},
 'meta_data': {'parents': [['cc7cfb52a4658ba440bd7691c5a3d6f736f94d3d795857725a2e400f9e3624a9']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '315774e833d514d7ebcd50e83a42e91b93910f3590880100f0582c8734bdb919'}
'''
def gc_315774e833d514d7ebcd50e83a42e91b93910f3590880100f0582c8734bdb919(i):
	a = gc_5f1ff9bfaf9bc1cdb5d520bd056048ebe5467cc6580f03b9c0c29b7eb64c4d2b((i[0], i[0], 0.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:26:01.584386Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'b4dc32c9bc15e51d8070be7bf0ee9bfc344b73cc8ec857978ff72e71a3efb911',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'parents': [['69f8bddf1ba8386b128c82b9e9d61bfbcd39a2adfb0f072e1c0edd6fc96c2b5e']]},
 'num_codes': 1,
 'num_inputs': 0,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'aa177a51676b4ac9993b3491a70b5e6d53f2b26bde6e775c5a22fa1e22186c41'}
'''
def gc_aa177a51676b4ac9993b3491a70b5e6d53f2b26bde6e775c5a22fa1e22186c41(i):
	a = gc_b4dc32c9bc15e51d8070be7bf0ee9bfc344b73cc8ec857978ff72e71a3efb911((0.0, 0.0, 0.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:26:01.520992Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '102a4d1fc747c5f81b314937da02b830ca4a49a6010aa65fd478dd1bd68675e8',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0]], 'C': [1.0], 'O': [['A', 0]]},
 'meta_data': {'parents': [['102a4d1fc747c5f81b314937da02b830ca4a49a6010aa65fd478dd1bd68675e8']]},
 'num_codes': 1,
 'num_inputs': 0,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'ea69bccc1973aaff350a95c2d8cc9b3b41832729d1a7492c05beb61f1f8bd79e'}
'''
def gc_ea69bccc1973aaff350a95c2d8cc9b3b41832729d1a7492c05beb61f1f8bd79e(i):
	a = gc_102a4d1fc747c5f81b314937da02b830ca4a49a6010aa65fd478dd1bd68675e8((1.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:26:05.015378Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'ce4e58fcbe55e5caf14c456fd2603a7d81c19e89e61e63b0e56f8c1958ba3da1',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0], ['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'parents': [['ce4e58fcbe55e5caf14c456fd2603a7d81c19e89e61e63b0e56f8c1958ba3da1']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': True,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': False},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'cd3de5e6d4722a72bdd55203c51f7b616dd5f6a7db68158ff5148b2ef17ed6cb'}
'''
def gc_cd3de5e6d4722a72bdd55203c51f7b616dd5f6a7db68158ff5148b2ef17ed6cb(i):
	a = gc_ce4e58fcbe55e5caf14c456fd2603a7d81c19e89e61e63b0e56f8c1958ba3da1((i[0], i[0],))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:26:04.946458Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '23c441e967ef4b8637554409522bc07c1d0faac129bccf73473c098650a63957',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 1], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'parents': [['23c441e967ef4b8637554409522bc07c1d0faac129bccf73473c098650a63957']]},
 'num_codes': 1,
 'num_inputs': 0,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '325fe4a0507140bc1587cb40eb3f8dcb256226f6395341db9a7f6112ca0f858e'}
'''
def gc_325fe4a0507140bc1587cb40eb3f8dcb256226f6395341db9a7f6112ca0f858e(i):
	a = gc_23c441e967ef4b8637554409522bc07c1d0faac129bccf73473c098650a63957((0.0, 0.0, 0.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:26:04.579792Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '5f1ff9bfaf9bc1cdb5d520bd056048ebe5467cc6580f03b9c0c29b7eb64c4d2b',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0], ['I', 0], ['C', 0]], 'C': [0.0], 'O': [['A', 0]]},
 'meta_data': {'parents': [['cc7cfb52a4658ba440bd7691c5a3d6f736f94d3d795857725a2e400f9e3624a9']]},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': 'd849b50b3877bd437c27d41487f9c9836b6a470b1308738b1ef19a4c43cf007d'}
'''
def gc_d849b50b3877bd437c27d41487f9c9836b6a470b1308738b1ef19a4c43cf007d(i):
	a = gc_5f1ff9bfaf9bc1cdb5d520bd056048ebe5467cc6580f03b9c0c29b7eb64c4d2b((0.0, i[0], 0.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:26:05.860803Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '5f1ff9bfaf9bc1cdb5d520bd056048ebe5467cc6580f03b9c0c29b7eb64c4d2b',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 1], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'parents': [['cc7cfb52a4658ba440bd7691c5a3d6f736f94d3d795857725a2e400f9e3624a9']]},
 'num_codes': 1,
 'num_inputs': 0,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '1d83336c23e184a7944854e7afb07a8107ae335f680d3cc4a86cfa27cc30ebd8'}
'''
def gc_1d83336c23e184a7944854e7afb07a8107ae335f680d3cc4a86cfa27cc30ebd8(i):
	a = gc_5f1ff9bfaf9bc1cdb5d520bd056048ebe5467cc6580f03b9c0c29b7eb64c4d2b((0.0, 0.0, 0.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-16T00:26:05.517362Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '81b5a567e50cf6fd71bfcfc3c5d23faa0f245fb0a71900fa9573eba1a94ee80d',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0]], 'C': [0.0], 'O': [['A', 0]]},
 'meta_data': {'parents': [['b98b16eb6649388de0a5294dcbde704470050a9c23850db69a1b239bd6788ee6']]},
 'num_codes': 1,
 'num_inputs': 0,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 0,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '87d95699b95f73b0d9cd4b559dce51d13722fd143c7cc9b0b6be5430f0fdff56'}
'''
def gc_87d95699b95f73b0d9cd4b559dce51d13722fd143c7cc9b0b6be5430f0fdff56(i):
	a = gc_81b5a567e50cf6fd71bfcfc3c5d23faa0f245fb0a71900fa9573eba1a94ee80d((0.0,))
	return (a[0],)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-16T00:25:44.234761Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '0000000000000000000000000000000000000000000000000000000000000000',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 1,
 'graph': {'A': [['I', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'function': {'python3': {'0': {'inline': "connect({0[i0]}, 'A', "
                                                        "'B', {0[c0]}, "
                                                        '{0[c1]})'}}},
               'name': 'GCB-GCA connection with constant fractional offsets'},
 'num_codes': 1,
 'num_inputs': 1,
 'num_outputs': 1,
 'num_unique_codes': 1,
 'opt_num_codons': 1,
 'properties': {'binary_mutation': False,
                'conditional': False,
                'extended': False,
                'logical': False,
                'mathematical': False,
                'unary_mutation': True},
 'raw_num_codons': 1,
 'reference_count': 0,
 'signature': '23c441e967ef4b8637554409522bc07c1d0faac129bccf73473c098650a63957'}
'''
def gc_23c441e967ef4b8637554409522bc07c1d0faac129bccf73473c098650a63957(i):
	return (connect(i[0], 'A', 'B', 0.0, 0.0),)


meta_data = {
	'7404cd51f0ff21ae1b51cd8e13b6bacf706cafde670c9ef05ae282fea9ff2364':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_7404cd51f0ff21ae1b51cd8e13b6bacf706cafde670c9ef05ae282fea9ff2364 },
	'b3426a0b5077c14d09c2eb091e8ba0ded68486890d5f0146cfdec34ebbe383d6':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_b3426a0b5077c14d09c2eb091e8ba0ded68486890d5f0146cfdec34ebbe383d6 },
	'282424295de4addaa42b8117a6e53ce0136fcfba2b1cdfab61ac3c7e3a823516':{'num_inputs': 2,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_282424295de4addaa42b8117a6e53ce0136fcfba2b1cdfab61ac3c7e3a823516 },
	'b98b16eb6649388de0a5294dcbde704470050a9c23850db69a1b239bd6788ee6':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_b98b16eb6649388de0a5294dcbde704470050a9c23850db69a1b239bd6788ee6 },
	'aab332740bb7b6730311c956b05c16d19814c2d752e1db38b65aa95c7b9209d7':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_aab332740bb7b6730311c956b05c16d19814c2d752e1db38b65aa95c7b9209d7 },
	'3669b2f53208e322423da38d8006444917940ddfedbf169eaf0212c0fe6f10b7':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_3669b2f53208e322423da38d8006444917940ddfedbf169eaf0212c0fe6f10b7 },
	'cc7cfb52a4658ba440bd7691c5a3d6f736f94d3d795857725a2e400f9e3624a9':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_cc7cfb52a4658ba440bd7691c5a3d6f736f94d3d795857725a2e400f9e3624a9 },
	'f5b607832778f539c313b5dbe664e0cdbaf016bcdba4ac95d45c54f999e08a4f':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_f5b607832778f539c313b5dbe664e0cdbaf016bcdba4ac95d45c54f999e08a4f },
	'de16d05c96f141351c6e918906ad8565426b05c77a187edc20763c01f4d8db86':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_de16d05c96f141351c6e918906ad8565426b05c77a187edc20763c01f4d8db86 },
	'63f4c2177ea134118ee0d3b75c8a1e48a85dbb4214bcf0abf70b44241329f23c':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_63f4c2177ea134118ee0d3b75c8a1e48a85dbb4214bcf0abf70b44241329f23c },
	'8568fa49a69fc9c42c30d78866a45316976afca26ce6a75284546f07ad9f6aef':{'num_inputs': 2,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_8568fa49a69fc9c42c30d78866a45316976afca26ce6a75284546f07ad9f6aef },
	'0b71cf0dd17adf2126959c3712c97c25420a33cb71657225c3d76c127a2d3f8d':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_0b71cf0dd17adf2126959c3712c97c25420a33cb71657225c3d76c127a2d3f8d },
	'065c6b174b50d8682b49d71112febf3f052ad94f794cef68009887ae1bc09b69':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_065c6b174b50d8682b49d71112febf3f052ad94f794cef68009887ae1bc09b69 },
	'a380199b1efb5e06e8bf0ba253f2250b665534df9402e9ba08405876a9d0911b':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_a380199b1efb5e06e8bf0ba253f2250b665534df9402e9ba08405876a9d0911b },
	'15351a2e310bb0e2f6189d1728d5eee750c673dcb0b15c0f40302c6ef4e33535':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_15351a2e310bb0e2f6189d1728d5eee750c673dcb0b15c0f40302c6ef4e33535 },
	'8e63d58261949359d0c4f000d50406d5c5df57a1809ca623baa7940a1ac1c84a':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_8e63d58261949359d0c4f000d50406d5c5df57a1809ca623baa7940a1ac1c84a },
	'66ac33a3f469fe70a0c72886b61ccd32f2b9b4738c8dd22112ba9e47ebe4ff2b':{'num_inputs': 2,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': False, 'binary_mutation': True, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_66ac33a3f469fe70a0c72886b61ccd32f2b9b4738c8dd22112ba9e47ebe4ff2b },
	'69f8bddf1ba8386b128c82b9e9d61bfbcd39a2adfb0f072e1c0edd6fc96c2b5e':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_69f8bddf1ba8386b128c82b9e9d61bfbcd39a2adfb0f072e1c0edd6fc96c2b5e },
	'572f3d56521fb576738b38239b46b1f2e4f881dbeb18ba57b3254a6dceb5782e':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_572f3d56521fb576738b38239b46b1f2e4f881dbeb18ba57b3254a6dceb5782e },
	'b33df5beef7cd7d5e49e74b229864ba0664bae07dbe6a28a3c9c11643518f37d':{'num_inputs': 2,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_b33df5beef7cd7d5e49e74b229864ba0664bae07dbe6a28a3c9c11643518f37d },
	'42bdabf6208e9529f50a37386efafc88a45bdd1ed90be29c97a18041626dba9b':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_42bdabf6208e9529f50a37386efafc88a45bdd1ed90be29c97a18041626dba9b },
	'7c81e32cacdeb941a0c6989d24d58a9591a9771cce66ec0752ebbd0b2e1f5eae':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_7c81e32cacdeb941a0c6989d24d58a9591a9771cce66ec0752ebbd0b2e1f5eae },
	'5e518b6b4668611c3d1602f784ad410609d5657a5d5690f9abca54eb4b7c0f3a':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_5e518b6b4668611c3d1602f784ad410609d5657a5d5690f9abca54eb4b7c0f3a },
	'a0429192b8ead5be37fc2c644a9ed57cf4a9eaf2a10c9fe225a6e39a204b5e16':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_a0429192b8ead5be37fc2c644a9ed57cf4a9eaf2a10c9fe225a6e39a204b5e16 },
	'bf3161b1d66c4f7b2c4d7c9901bd0044d3dcb0e2bc05dbe82e1feeeb40ef9931':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_bf3161b1d66c4f7b2c4d7c9901bd0044d3dcb0e2bc05dbe82e1feeeb40ef9931 },
	'cf8cd9075b571cb5a59d37e378029ff54502df66779163ba058c01384f335c2c':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_cf8cd9075b571cb5a59d37e378029ff54502df66779163ba058c01384f335c2c },
	'65205972c2842865c3b8de9cd43d117c8bc0ff4fc05f27284d93416cd604dcf4':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_65205972c2842865c3b8de9cd43d117c8bc0ff4fc05f27284d93416cd604dcf4 },
	'7eb61a64d6aa1248cf7c1973ece726698b4d3b61964060a46a9789bda79d7c72':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_7eb61a64d6aa1248cf7c1973ece726698b4d3b61964060a46a9789bda79d7c72 },
	'db707d1e30841606ccbc7f7d349dcdadcf7b3b5e1e8d1a2e8cec17e1317bfd13':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_db707d1e30841606ccbc7f7d349dcdadcf7b3b5e1e8d1a2e8cec17e1317bfd13 },
	'afa54e4b4caac53b34964c353bec7a56c8f8a41a501e37afe3a2f0237968b97e':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_afa54e4b4caac53b34964c353bec7a56c8f8a41a501e37afe3a2f0237968b97e },
	'562f9ffb473aade86537c9d78a94314f32cc0e1e6a5c71926777777c5fd35bbf':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_562f9ffb473aade86537c9d78a94314f32cc0e1e6a5c71926777777c5fd35bbf },
	'67aa64f950ed976c1835461b09f7aee23a9ef5508d2a06d7b02e026b32f4134a':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_67aa64f950ed976c1835461b09f7aee23a9ef5508d2a06d7b02e026b32f4134a },
	'102a4d1fc747c5f81b314937da02b830ca4a49a6010aa65fd478dd1bd68675e8':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_102a4d1fc747c5f81b314937da02b830ca4a49a6010aa65fd478dd1bd68675e8 },
	'81d83b6dfe8764bc32df13948a86e7721818e3648d8f916708f8d416b2b94370':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_81d83b6dfe8764bc32df13948a86e7721818e3648d8f916708f8d416b2b94370 },
	'6bba0589ed454784e75f8a184fb8fc8d59a3772e73a8414f2ba915ce211f6773':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_6bba0589ed454784e75f8a184fb8fc8d59a3772e73a8414f2ba915ce211f6773 },
	'4793e082e2462b3ed47a23c000e9e8165bf7b6dea9bde08182b7203a708f6214':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_4793e082e2462b3ed47a23c000e9e8165bf7b6dea9bde08182b7203a708f6214 },
	'63971bfb77792f35cda0463d310e2724ae108354fb287df386ab88a752743fcc':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_63971bfb77792f35cda0463d310e2724ae108354fb287df386ab88a752743fcc },
	'a95ea10e7327badf07045086c7e935f5cc66a9b47f323fcdf30d76f66a592829':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_a95ea10e7327badf07045086c7e935f5cc66a9b47f323fcdf30d76f66a592829 },
	'4f54b44dd522c044b41833089ca47ece6b280ff8c11324a5b8b6a957d92f6de8':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_4f54b44dd522c044b41833089ca47ece6b280ff8c11324a5b8b6a957d92f6de8 },
	'c436ba9675317cfa2b5e32a3f00cf08b57295e06f28d5203fbaa1cd6b430e6d7':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_c436ba9675317cfa2b5e32a3f00cf08b57295e06f28d5203fbaa1cd6b430e6d7 },
	'b4dc32c9bc15e51d8070be7bf0ee9bfc344b73cc8ec857978ff72e71a3efb911':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_b4dc32c9bc15e51d8070be7bf0ee9bfc344b73cc8ec857978ff72e71a3efb911 },
	'f131f1d7c087d2b567acec3f2a476de27b9110e0794c11b2c97098e878feed08':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_f131f1d7c087d2b567acec3f2a476de27b9110e0794c11b2c97098e878feed08 },
	'ee2cc4658d03ebb3ffbcdc44d31fa89b7644a654567d66b93bac5f6186899d4d':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_ee2cc4658d03ebb3ffbcdc44d31fa89b7644a654567d66b93bac5f6186899d4d },
	'e279714512f0498ee888c84f1906de2a5e6bf082d60fdbb32de84a0c16f6f071':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_e279714512f0498ee888c84f1906de2a5e6bf082d60fdbb32de84a0c16f6f071 },
	'7bb5eb204e326fbabe069fb824e88a6ca68ec34c39eaa05a4d271a3f92e4b4fd':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_7bb5eb204e326fbabe069fb824e88a6ca68ec34c39eaa05a4d271a3f92e4b4fd },
	'bcf49ecb02279621bc1dd9d70265175f142ccfcc742ff07cf3983c830c4670fc':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_bcf49ecb02279621bc1dd9d70265175f142ccfcc742ff07cf3983c830c4670fc },
	'ea549df0fcde3b6375528205fef6eea94b79a442fd8afa77905fbeab96c6bcea':{'num_inputs': 2,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_ea549df0fcde3b6375528205fef6eea94b79a442fd8afa77905fbeab96c6bcea },
	'fcba468768bf701a1234ea41739916b0655512c74c74e5930cae35d13b92925f':{'num_inputs': 2,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_fcba468768bf701a1234ea41739916b0655512c74c74e5930cae35d13b92925f },
	'4140f47e72adf3343c04c82d7766bf9e3bc71a6b606b7bc2e93f45a6349792e5':{'num_inputs': 2,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_4140f47e72adf3343c04c82d7766bf9e3bc71a6b606b7bc2e93f45a6349792e5 },
	'ce4e58fcbe55e5caf14c456fd2603a7d81c19e89e61e63b0e56f8c1958ba3da1':{'num_inputs': 2,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': False, 'binary_mutation': True, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_ce4e58fcbe55e5caf14c456fd2603a7d81c19e89e61e63b0e56f8c1958ba3da1 },
	'ce171d8207600a6c5b494439f1af004fb58b93f4051e75a05ef354e360cf2fe3':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_ce171d8207600a6c5b494439f1af004fb58b93f4051e75a05ef354e360cf2fe3 },
	'aa04da1966f1433e73396dd5c16b8deb59e0104cdbc1f0a41aa021a3aad22268':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_aa04da1966f1433e73396dd5c16b8deb59e0104cdbc1f0a41aa021a3aad22268 },
	'75ff6e5392d8ac373c8b0445027b904ffd1a62b19774a2326aa1e596049ca132':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_75ff6e5392d8ac373c8b0445027b904ffd1a62b19774a2326aa1e596049ca132 },
	'986ae757be6910ae3b92411b03d2f9feace48fe748d96a7933f98b0ca9d5e3c9':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_986ae757be6910ae3b92411b03d2f9feace48fe748d96a7933f98b0ca9d5e3c9 },
	'81b5a567e50cf6fd71bfcfc3c5d23faa0f245fb0a71900fa9573eba1a94ee80d':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_81b5a567e50cf6fd71bfcfc3c5d23faa0f245fb0a71900fa9573eba1a94ee80d },
	'6583b66e7cb73e5c773e7700cb4485a2b81d4ce942220fbc65ef67b99589ca08':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_6583b66e7cb73e5c773e7700cb4485a2b81d4ce942220fbc65ef67b99589ca08 },
	'0377050cd3534281ac885213d141494d2ea6ce8b50f787f224a6dc65ecb90e10':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_0377050cd3534281ac885213d141494d2ea6ce8b50f787f224a6dc65ecb90e10 },
	'731f9ff5e9cfdb53f1944bf6962c32b21be104ef51b2fdb3db0244b077010af2':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_731f9ff5e9cfdb53f1944bf6962c32b21be104ef51b2fdb3db0244b077010af2 },
	'18aefb88a3ddaf2056601643afd03be838c5c77317ca3b89c700e219db26e18c':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_18aefb88a3ddaf2056601643afd03be838c5c77317ca3b89c700e219db26e18c },
	'5d180795babcb82e7ea8b4357ae602a44666c60f0d2b851051c89e1149e72f97':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_5d180795babcb82e7ea8b4357ae602a44666c60f0d2b851051c89e1149e72f97 },
	'7743aba320d9a6dd5f2b7a8e5777b997d61131f2a4db0f78fb4a881d40244898':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_7743aba320d9a6dd5f2b7a8e5777b997d61131f2a4db0f78fb4a881d40244898 },
	'13b3b21f4b1e53f66075fa59d78dccab619d1f8e65a22bb82d9a68c347a212c6':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_13b3b21f4b1e53f66075fa59d78dccab619d1f8e65a22bb82d9a68c347a212c6 },
	'cb159d2420f0a661bcdd192ab4cfac4363d652f0ec3ac8ab69e84e33768b97ec':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_cb159d2420f0a661bcdd192ab4cfac4363d652f0ec3ac8ab69e84e33768b97ec },
	'278ddaaaa439429bad68df4b81f3b42ecdc7cf2d2ea8ad086a2ca185a3acbbb6':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_278ddaaaa439429bad68df4b81f3b42ecdc7cf2d2ea8ad086a2ca185a3acbbb6 },
	'd583313ac7265d903f96aebefac338b54f234df8c3250552bea73f53de7b4cfa':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_d583313ac7265d903f96aebefac338b54f234df8c3250552bea73f53de7b4cfa },
	'f269bf2281717b6c6d4cd1c4f6bdd61dd63f8501ed8a3846b79dca9c82387a51':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_f269bf2281717b6c6d4cd1c4f6bdd61dd63f8501ed8a3846b79dca9c82387a51 },
	'2a1a7136267b40ddef2589b706851cadea6ea3617c681bca44d915ca2c48c865':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_2a1a7136267b40ddef2589b706851cadea6ea3617c681bca44d915ca2c48c865 },
	'57445022b9dc0d937721bb272de55001607f26c9b9cc9dd40cd4dead77da6366':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_57445022b9dc0d937721bb272de55001607f26c9b9cc9dd40cd4dead77da6366 },
	'5f1ff9bfaf9bc1cdb5d520bd056048ebe5467cc6580f03b9c0c29b7eb64c4d2b':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_5f1ff9bfaf9bc1cdb5d520bd056048ebe5467cc6580f03b9c0c29b7eb64c4d2b },
	'd990e3a0af629cd2048c76bdc4dbfe12a93eb16e35ccf71818050b1a9c915ae2':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_d990e3a0af629cd2048c76bdc4dbfe12a93eb16e35ccf71818050b1a9c915ae2 },
	'315774e833d514d7ebcd50e83a42e91b93910f3590880100f0582c8734bdb919':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_315774e833d514d7ebcd50e83a42e91b93910f3590880100f0582c8734bdb919 },
	'aa177a51676b4ac9993b3491a70b5e6d53f2b26bde6e775c5a22fa1e22186c41':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_aa177a51676b4ac9993b3491a70b5e6d53f2b26bde6e775c5a22fa1e22186c41 },
	'ea69bccc1973aaff350a95c2d8cc9b3b41832729d1a7492c05beb61f1f8bd79e':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_ea69bccc1973aaff350a95c2d8cc9b3b41832729d1a7492c05beb61f1f8bd79e },
	'cd3de5e6d4722a72bdd55203c51f7b616dd5f6a7db68158ff5148b2ef17ed6cb':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': False, 'binary_mutation': True, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_cd3de5e6d4722a72bdd55203c51f7b616dd5f6a7db68158ff5148b2ef17ed6cb },
	'325fe4a0507140bc1587cb40eb3f8dcb256226f6395341db9a7f6112ca0f858e':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_325fe4a0507140bc1587cb40eb3f8dcb256226f6395341db9a7f6112ca0f858e },
	'd849b50b3877bd437c27d41487f9c9836b6a470b1308738b1ef19a4c43cf007d':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_d849b50b3877bd437c27d41487f9c9836b6a470b1308738b1ef19a4c43cf007d },
	'1d83336c23e184a7944854e7afb07a8107ae335f680d3cc4a86cfa27cc30ebd8':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_1d83336c23e184a7944854e7afb07a8107ae335f680d3cc4a86cfa27cc30ebd8 },
	'87d95699b95f73b0d9cd4b559dce51d13722fd143c7cc9b0b6be5430f0fdff56':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_87d95699b95f73b0d9cd4b559dce51d13722fd143c7cc9b0b6be5430f0fdff56 },
	'23c441e967ef4b8637554409522bc07c1d0faac129bccf73473c098650a63957':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_23c441e967ef4b8637554409522bc07c1d0faac129bccf73473c098650a63957 }
}
