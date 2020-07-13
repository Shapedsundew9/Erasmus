# Erasmus GP Gene Pool


from microbiome.genetics.gc_mutation_functions import *
from random import random, uniform


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:00.631760Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '4f54b44dd522c044b41833089ca47ece6b280ff8c11324a5b8b6a957d92f6de8',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 1]]},
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
 'signature': '03d3eaff46ecd43fd8772beef3c985fcf4de70c55d53552835bec4cc71bffb04'}
'''
def gc_03d3eaff46ecd43fd8772beef3c985fcf4de70c55d53552835bec4cc71bffb04(i):
	a = gc_4f54b44dd522c044b41833089ca47ece6b280ff8c11324a5b8b6a957d92f6de8((i[0], 0.0, 0.0,))
	return (a[1],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:06.558691Z',
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
 'created': '2020-07-13T17:51:00.735664Z',
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
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-13T17:50:59.444942Z',
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
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:02.330249Z',
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
 'created': '2020-07-13T17:51:32.788037Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '278ddaaaa439429bad68df4b81f3b42ecdc7cf2d2ea8ad086a2ca185a3acbbb6',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0]], 'C': [['I', 0]], 'O': [['I', 0]]},
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
 'signature': '1745bd810b62f97916ccde4247e74fb6b04fa3e07a0a2349d115daea3708c540'}
'''
def gc_1745bd810b62f97916ccde4247e74fb6b04fa3e07a0a2349d115daea3708c540(i):
	a = gc_278ddaaaa439429bad68df4b81f3b42ecdc7cf2d2ea8ad086a2ca185a3acbbb6((['I', 0],))
	return (i[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:51.444489Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '23c441e967ef4b8637554409522bc07c1d0faac129bccf73473c098650a63957',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 1]]},
 'meta_data': {'parents': [['aa8b534a5c93cfb139aeaa0ddda00367b2e88cace02bbdef8274aa9fb61ce4fe']]},
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
 'signature': '20f3364de91953b7b0e5e590831d3b36e2afd02defc8ec4ea0d221fa23224d17'}
'''
def gc_20f3364de91953b7b0e5e590831d3b36e2afd02defc8ec4ea0d221fa23224d17(i):
	a = gc_23c441e967ef4b8637554409522bc07c1d0faac129bccf73473c098650a63957((0.0, 0.0, 0.0,))
	return (a[1],)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-13T17:50:59.727708Z',
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


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:52:19.540663Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'f131f1d7c087d2b567acec3f2a476de27b9110e0794c11b2c97098e878feed08',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0], ['C', 0], ['I', 0]], 'C': [0.0], 'O': [['A', 0]]},
 'meta_data': {'parents': [['d91aec2848d9b2a917bc2edbf315e5c015fd56e9b4d961d39eaf7bdc07228eb4']]},
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
 'signature': '25345bc7f15998f42c66172678da46b0847a9ca2f723d3b9b72cdbaacf3fd8a3'}
'''
def gc_25345bc7f15998f42c66172678da46b0847a9ca2f723d3b9b72cdbaacf3fd8a3(i):
	a = gc_f131f1d7c087d2b567acec3f2a476de27b9110e0794c11b2c97098e878feed08((0.0, 0.0, i[0],))
	return (a[0],)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-13T17:50:59.533427Z',
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
 'created': '2020-07-13T17:51:00.818935Z',
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
 'created': '2020-07-13T17:51:08.376528Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'e279714512f0498ee888c84f1906de2a5e6bf082d60fdbb32de84a0c16f6f071',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['D', 0]], 'O': [['I', 0]]},
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
 'signature': '2a30f8b83f964a470b4c68e8c30d112f99cfca4a2ca3acf15cecf94aa5e3804f'}
'''
def gc_2a30f8b83f964a470b4c68e8c30d112f99cfca4a2ca3acf15cecf94aa5e3804f(i):
	a = gc_e279714512f0498ee888c84f1906de2a5e6bf082d60fdbb32de84a0c16f6f071((d[0],))
	return (i[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:13.897972Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '4f54b44dd522c044b41833089ca47ece6b280ff8c11324a5b8b6a957d92f6de8',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'parents': [['cf8cd9075b571cb5a59d37e378029ff54502df66779163ba058c01384f335c2c']]},
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
 'signature': '31e4e3af86f9d2a46cdc37171097324bfe35d2459baa32d61f46fe95742ba07e'}
'''
def gc_31e4e3af86f9d2a46cdc37171097324bfe35d2459baa32d61f46fe95742ba07e(i):
	a = gc_4f54b44dd522c044b41833089ca47ece6b280ff8c11324a5b8b6a957d92f6de8((0.0, 0.0, 0.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:06.306638Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'ee2cc4658d03ebb3ffbcdc44d31fa89b7644a654567d66b93bac5f6186899d4d',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 2]]},
 'meta_data': {'parents': [['5a133701ad6928931161f8dd2537b225cfb54c18f2b49efcc6fd743ccb8c062c']]},
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
 'signature': '33a14972c04f1771bc6bf7871d7438d38eec27ddfee6bdc23a2c4089f6f6f182'}
'''
def gc_33a14972c04f1771bc6bf7871d7438d38eec27ddfee6bdc23a2c4089f6f6f182(i):
	a = gc_ee2cc4658d03ebb3ffbcdc44d31fa89b7644a654567d66b93bac5f6186899d4d((i[0], 0.0, 0.0,))
	return (a[2],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:03.969033Z',
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
 'created': '2020-07-13T17:51:58.779049Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '4cde93184158819b805ef591641fad84f4c0ee4fdb2715d267cbbcce1a53f8a4',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['D', 0]], 'C': [0.0], 'O': [['A', 0]]},
 'meta_data': {'parents': [['4cde93184158819b805ef591641fad84f4c0ee4fdb2715d267cbbcce1a53f8a4']]},
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
 'signature': '3e499d7ca7138daf82cd99d0bb2e48aaed172cb47d090509f67041489cccd15d'}
'''
def gc_3e499d7ca7138daf82cd99d0bb2e48aaed172cb47d090509f67041489cccd15d(i):
	a = gc_4cde93184158819b805ef591641fad84f4c0ee4fdb2715d267cbbcce1a53f8a4((d[0],))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:52:16.204002Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'b4dc32c9bc15e51d8070be7bf0ee9bfc344b73cc8ec857978ff72e71a3efb911',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['D', 0], ['I', 0], ['D', 0]],
           'C': [-0.21162167368565665],
           'O': [['I', 1]]},
 'meta_data': {'parents': [['b4dc32c9bc15e51d8070be7bf0ee9bfc344b73cc8ec857978ff72e71a3efb911']]},
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
 'signature': '412893aa241dbb25bc8766eb459e0b255d8913ab368b600b587ca912dd5f730c'}
'''
def gc_412893aa241dbb25bc8766eb459e0b255d8913ab368b600b587ca912dd5f730c(i):
	a = gc_b4dc32c9bc15e51d8070be7bf0ee9bfc344b73cc8ec857978ff72e71a3efb911((d[0], i[0], d[0],))
	return (i[1],)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:00.038150Z',
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
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:05.301102Z',
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
 'created': '2020-07-13T17:51:06.269294Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '23c441e967ef4b8637554409522bc07c1d0faac129bccf73473c098650a63957',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'parents': [['3669b2f53208e322423da38d8006444917940ddfedbf169eaf0212c0fe6f10b7']]},
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
 'signature': '46b77d4a61398a228ef0b64e465cc33ee6f4527980586ea4a40ab2e6d3aedec0'}
'''
def gc_46b77d4a61398a228ef0b64e465cc33ee6f4527980586ea4a40ab2e6d3aedec0(i):
	a = gc_23c441e967ef4b8637554409522bc07c1d0faac129bccf73473c098650a63957((0.0, 0.0, 0.0,))
	return (a[0],)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-13T17:50:59.582949Z',
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
 'created': '2020-07-13T17:50:59.398319Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '0000000000000000000000000000000000000000000000000000000000000000',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 1,
 'graph': {'A': [['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'function': {'python3': {'0': {'inline': "connect({0[i0]}, 'I', "
                                                        "'A', random(), "
                                                        'random())'}}},
               'name': 'GCA-input connection with random fractional offsets'},
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
 'signature': '4cde93184158819b805ef591641fad84f4c0ee4fdb2715d267cbbcce1a53f8a4'}
'''
def gc_4cde93184158819b805ef591641fad84f4c0ee4fdb2715d267cbbcce1a53f8a4(i):
	return (connect(i[0], 'I', 'A', random(), random()),)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-13T17:50:59.657631Z',
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
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:00.544498Z',
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
 'created': '2020-07-13T17:51:43.135683Z',
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
 'created': '2020-07-13T17:51:03.840034Z',
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
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:04.080611Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'ee2cc4658d03ebb3ffbcdc44d31fa89b7644a654567d66b93bac5f6186899d4d',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 1]]},
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
 'signature': '5a133701ad6928931161f8dd2537b225cfb54c18f2b49efcc6fd743ccb8c062c'}
'''
def gc_5a133701ad6928931161f8dd2537b225cfb54c18f2b49efcc6fd743ccb8c062c(i):
	a = gc_ee2cc4658d03ebb3ffbcdc44d31fa89b7644a654567d66b93bac5f6186899d4d((i[0], 0.0, 0.0,))
	return (a[1],)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-13T17:50:59.699451Z',
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
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-13T17:50:59.608353Z',
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
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:00.501684Z',
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
 'created': '2020-07-13T17:51:03.161685Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'ce4e58fcbe55e5caf14c456fd2603a7d81c19e89e61e63b0e56f8c1958ba3da1',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0], ['I', 1]], 'O': [['I', 0]]},
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
	return (i[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:15.379937Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'b3426a0b5077c14d09c2eb091e8ba0ded68486890d5f0146cfdec34ebbe383d6',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0]], 'C': [1.0], 'O': [['C', 0]]},
 'meta_data': {'parents': [['b3426a0b5077c14d09c2eb091e8ba0ded68486890d5f0146cfdec34ebbe383d6']]},
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
 'signature': '670a0aa12cc1491b80aa34adae09fa3a0e801f4b0d3cd47851fb452b736fbe1a'}
'''
def gc_670a0aa12cc1491b80aa34adae09fa3a0e801f4b0d3cd47851fb452b736fbe1a(i):
	a = gc_b3426a0b5077c14d09c2eb091e8ba0ded68486890d5f0146cfdec34ebbe383d6((1.0,))
	return (1.0,)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:25.021316Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '4cde93184158819b805ef591641fad84f4c0ee4fdb2715d267cbbcce1a53f8a4',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0]], 'C': [['I', 0]], 'O': [['C', 0]]},
 'meta_data': {'parents': [['4cde93184158819b805ef591641fad84f4c0ee4fdb2715d267cbbcce1a53f8a4']]},
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
 'signature': '680d118644077298a193b75aa60abd05063f6892893c6dc4f02660352eee472b'}
'''
def gc_680d118644077298a193b75aa60abd05063f6892893c6dc4f02660352eee472b(i):
	a = gc_4cde93184158819b805ef591641fad84f4c0ee4fdb2715d267cbbcce1a53f8a4((['I', 0],))
	return (['I', 0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:09.074098Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'b4dc32c9bc15e51d8070be7bf0ee9bfc344b73cc8ec857978ff72e71a3efb911',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'parents': [['e3f608304dd03aacec080715777dd780d6488977a115c98932e042b63d69c6e1']]},
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
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-13T17:50:59.556457Z',
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
 'created': '2020-07-13T17:50:59.914261Z',
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
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:04.269916Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '4793e082e2462b3ed47a23c000e9e8165bf7b6dea9bde08182b7203a708f6214',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0]], 'C': [['I', 0]], 'O': [['C', 0]]},
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
	a = gc_4793e082e2462b3ed47a23c000e9e8165bf7b6dea9bde08182b7203a708f6214((['I', 0],))
	return (['I', 0],)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-13T17:50:59.889504Z',
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
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:00.586197Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'a95ea10e7327badf07045086c7e935f5cc66a9b47f323fcdf30d76f66a592829',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
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
 'signature': '7bf45529286677eb2266ff38b3c8a6a898ea41a3cbe831a2e60b1397faa8c106'}
'''
def gc_7bf45529286677eb2266ff38b3c8a6a898ea41a3cbe831a2e60b1397faa8c106(i):
	a = gc_a95ea10e7327badf07045086c7e935f5cc66a9b47f323fcdf30d76f66a592829((i[0], 0.0, 0.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:02.724462Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '4f54b44dd522c044b41833089ca47ece6b280ff8c11324a5b8b6a957d92f6de8',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 1]]},
 'meta_data': {'parents': [['03d3eaff46ecd43fd8772beef3c985fcf4de70c55d53552835bec4cc71bffb04']]},
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
 'signature': '7c30338bf43f14fc54b72811e0cefdd09bf2bb87ce61b2a2fd192ade84cebba0'}
'''
def gc_7c30338bf43f14fc54b72811e0cefdd09bf2bb87ce61b2a2fd192ade84cebba0(i):
	a = gc_4f54b44dd522c044b41833089ca47ece6b280ff8c11324a5b8b6a957d92f6de8((0.0, 0.0, 0.0,))
	return (a[1],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:02.917218Z',
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
 'created': '2020-07-13T17:52:09.618763Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '4f54b44dd522c044b41833089ca47ece6b280ff8c11324a5b8b6a957d92f6de8',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['D', 0], ['D', 0], ['I', 0]], 'C': [1.0], 'O': [['I', 0]]},
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
 'signature': '7f20a5d632ea8a8387010dfa728eea4f15e28e973ba812e3933c40e3deb09a98'}
'''
def gc_7f20a5d632ea8a8387010dfa728eea4f15e28e973ba812e3933c40e3deb09a98(i):
	a = gc_4f54b44dd522c044b41833089ca47ece6b280ff8c11324a5b8b6a957d92f6de8((d[0], d[0], i[0],))
	return (i[0],)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-13T17:50:59.942065Z',
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
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-13T17:50:59.486472Z',
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
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:02.200245Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'a95ea10e7327badf07045086c7e935f5cc66a9b47f323fcdf30d76f66a592829',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'parents': [['a95ea10e7327badf07045086c7e935f5cc66a9b47f323fcdf30d76f66a592829']]},
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
 'signature': '830056fc717060a25cfa061faedab989fdbc7208958cac782cfddff53a9de65b'}
'''
def gc_830056fc717060a25cfa061faedab989fdbc7208958cac782cfddff53a9de65b(i):
	a = gc_a95ea10e7327badf07045086c7e935f5cc66a9b47f323fcdf30d76f66a592829((0.0, 0.0, 0.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:52:10.853281Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '81d83b6dfe8764bc32df13948a86e7721818e3648d8f916708f8d416b2b94370',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0]], 'C': [0.0], 'O': [['A', 0]]},
 'meta_data': {'parents': [['65205972c2842865c3b8de9cd43d117c8bc0ff4fc05f27284d93416cd604dcf4']]},
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
 'signature': '8302f7ebfa7604701b0799d946b8c2c578d3a1f9723699b97cb4598d4a9ad955'}
'''
def gc_8302f7ebfa7604701b0799d946b8c2c578d3a1f9723699b97cb4598d4a9ad955(i):
	a = gc_81d83b6dfe8764bc32df13948a86e7721818e3648d8f916708f8d416b2b94370((0.0,))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:18.286570Z',
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
 'created': '2020-07-13T17:51:18.923508Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '81b5a567e50cf6fd71bfcfc3c5d23faa0f245fb0a71900fa9573eba1a94ee80d',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['D', 0]], 'O': [['A', 0]]},
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
	a = gc_81b5a567e50cf6fd71bfcfc3c5d23faa0f245fb0a71900fa9573eba1a94ee80d((d[0],))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:26.288695Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '4f54b44dd522c044b41833089ca47ece6b280ff8c11324a5b8b6a957d92f6de8',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 2]]},
 'meta_data': {'parents': [['31e4e3af86f9d2a46cdc37171097324bfe35d2459baa32d61f46fe95742ba07e']]},
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
 'signature': '9a373664d556d7975eab9f9bc390debc5d26c570fa64acbb247cadac27883008'}
'''
def gc_9a373664d556d7975eab9f9bc390debc5d26c570fa64acbb247cadac27883008(i):
	a = gc_4f54b44dd522c044b41833089ca47ece6b280ff8c11324a5b8b6a957d92f6de8((0.0, 0.0, 0.0,))
	return (a[2],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:52:09.690200Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'fcba468768bf701a1234ea41739916b0655512c74c74e5930cae35d13b92925f',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0], ['I', 0]], 'C': [['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'parents': [['fcba468768bf701a1234ea41739916b0655512c74c74e5930cae35d13b92925f']]},
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
 'signature': '9b4e6a07d07413e898e7a996c44cd4182c6b7a805b106ef76bf28176c2103d32'}
'''
def gc_9b4e6a07d07413e898e7a996c44cd4182c6b7a805b106ef76bf28176c2103d32(i):
	a = gc_fcba468768bf701a1234ea41739916b0655512c74c74e5930cae35d13b92925f((['I', 0], i[0],))
	return (a[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:52:43.927200Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'ee2cc4658d03ebb3ffbcdc44d31fa89b7644a654567d66b93bac5f6186899d4d',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 1], ['D', 0], ['I', 1]],
           'C': [-0.2615033133351021],
           'O': [['C', 0]]},
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
 'signature': '9e7fe73ca9e453aa6fb3427a5aaf36069ac317d01720ccbb6b2e2d20ec7deb63'}
'''
def gc_9e7fe73ca9e453aa6fb3427a5aaf36069ac317d01720ccbb6b2e2d20ec7deb63(i):
	a = gc_ee2cc4658d03ebb3ffbcdc44d31fa89b7644a654567d66b93bac5f6186899d4d((i[1], d[0], i[1],))
	return (-0.2615033133351021,)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:03.055833Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '4cde93184158819b805ef591641fad84f4c0ee4fdb2715d267cbbcce1a53f8a4',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0]], 'C': [0.0], 'O': [['I', 0]]},
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
	a = gc_4cde93184158819b805ef591641fad84f4c0ee4fdb2715d267cbbcce1a53f8a4((0.0,))
	return (i[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:05.364747Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'ea549df0fcde3b6375528205fef6eea94b79a442fd8afa77905fbeab96c6bcea',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0], ['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'parents': [['ea549df0fcde3b6375528205fef6eea94b79a442fd8afa77905fbeab96c6bcea']]},
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
 'signature': 'a427790d770b0fa722ca1ebae60ce603fbc45f0358ed7df37f88f0a042284a70'}
'''
def gc_a427790d770b0fa722ca1ebae60ce603fbc45f0358ed7df37f88f0a042284a70(i):
	a = gc_ea549df0fcde3b6375528205fef6eea94b79a442fd8afa77905fbeab96c6bcea((i[0], i[0],))
	return (a[0],)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-13T17:50:59.633482Z',
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
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:07.898633Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '23c441e967ef4b8637554409522bc07c1d0faac129bccf73473c098650a63957',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 1]]},
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
 'signature': 'aa8b534a5c93cfb139aeaa0ddda00367b2e88cace02bbdef8274aa9fb61ce4fe'}
'''
def gc_aa8b534a5c93cfb139aeaa0ddda00367b2e88cace02bbdef8274aa9fb61ce4fe(i):
	a = gc_23c441e967ef4b8637554409522bc07c1d0faac129bccf73473c098650a63957((i[0], 0.0, 0.0,))
	return (a[1],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:09.250452Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'f131f1d7c087d2b567acec3f2a476de27b9110e0794c11b2c97098e878feed08',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 0]]},
 'meta_data': {'parents': [['065c6b174b50d8682b49d71112febf3f052ad94f794cef68009887ae1bc09b69']]},
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
 'created': '2020-07-13T17:51:05.442569Z',
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
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-13T17:50:59.509114Z',
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
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-13T17:50:59.781036Z',
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
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:02.289732Z',
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
 'created': '2020-07-13T17:51:04.494344Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '7404cd51f0ff21ae1b51cd8e13b6bacf706cafde670c9ef05ae282fea9ff2364',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['D', 0]], 'C': [-1.0], 'O': [['A', 0]]},
 'meta_data': {'parents': [['7404cd51f0ff21ae1b51cd8e13b6bacf706cafde670c9ef05ae282fea9ff2364']]},
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
 'signature': 'bc79a0da85fd799928bd29601213255ea269b68c594e223ee11742902035515d'}
'''
def gc_bc79a0da85fd799928bd29601213255ea269b68c594e223ee11742902035515d(i):
	a = gc_7404cd51f0ff21ae1b51cd8e13b6bacf706cafde670c9ef05ae282fea9ff2364((d[0],))
	return (a[0],)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-13T17:50:59.964755Z',
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
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:18.621871Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'a95ea10e7327badf07045086c7e935f5cc66a9b47f323fcdf30d76f66a592829',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0], ['I', 0], ['C', 0]],
           'C': [['I', 0]],
           'O': [['I', 0]]},
 'meta_data': {'parents': [['7bf45529286677eb2266ff38b3c8a6a898ea41a3cbe831a2e60b1397faa8c106']]},
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
	a = gc_a95ea10e7327badf07045086c7e935f5cc66a9b47f323fcdf30d76f66a592829((['I', 0], i[0], ['I', 0],))
	return (i[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:10.290439Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'e279714512f0498ee888c84f1906de2a5e6bf082d60fdbb32de84a0c16f6f071',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0]], 'C': [['I', 0]], 'O': [['I', 0]]},
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
 'signature': 'bfd010ec1db290614a408872aa7e43640a50e11f035a47bd2d484cc080db8b8a'}
'''
def gc_bfd010ec1db290614a408872aa7e43640a50e11f035a47bd2d484cc080db8b8a(i):
	a = gc_e279714512f0498ee888c84f1906de2a5e6bf082d60fdbb32de84a0c16f6f071((['I', 0],))
	return (i[0],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:05.405277Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'fcba468768bf701a1234ea41739916b0655512c74c74e5930cae35d13b92925f',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0], ['I', 1]], 'O': [['A', 1]]},
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
 'signature': 'c377bcc1307f651040c84d99eee44a7a4bf29e9b84c7a3233ca539498a14bef1'}
'''
def gc_c377bcc1307f651040c84d99eee44a7a4bf29e9b84c7a3233ca539498a14bef1(i):
	a = gc_fcba468768bf701a1234ea41739916b0655512c74c74e5930cae35d13b92925f((i[0], i[1],))
	return (a[1],)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-13T17:50:59.754256Z',
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
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:00.671659Z',
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
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:00.063170Z',
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
 'created': '2020-07-13T17:51:02.852139Z',
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
 'created': '2020-07-13T17:52:16.931049Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'c436ba9675317cfa2b5e32a3f00cf08b57295e06f28d5203fbaa1cd6b430e6d7',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 1], ['I', 1], ['I', 0]], 'C': [0.0], 'O': [['C', 0]]},
 'meta_data': {'parents': [['7c81e32cacdeb941a0c6989d24d58a9591a9771cce66ec0752ebbd0b2e1f5eae']]},
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
 'signature': 'd0ac245cf0c9cfef6bb2c46fb713f8c2afd785eec8418f371cdc4f1ae48be228'}
'''
def gc_d0ac245cf0c9cfef6bb2c46fb713f8c2afd785eec8418f371cdc4f1ae48be228(i):
	a = gc_c436ba9675317cfa2b5e32a3f00cf08b57295e06f28d5203fbaa1cd6b430e6d7((i[1], i[1], i[0],))
	return (0.0,)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:52:10.016113Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'f131f1d7c087d2b567acec3f2a476de27b9110e0794c11b2c97098e878feed08',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0], ['D', 0], ['I', 0]],
           'C': [['I', 0]],
           'O': [['I', 1]]},
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
 'signature': 'd91aec2848d9b2a917bc2edbf315e5c015fd56e9b4d961d39eaf7bdc07228eb4'}
'''
def gc_d91aec2848d9b2a917bc2edbf315e5c015fd56e9b4d961d39eaf7bdc07228eb4(i):
	a = gc_f131f1d7c087d2b567acec3f2a476de27b9110e0794c11b2c97098e878feed08((['I', 0], d[0], i[0],))
	return (i[1],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:09.964826Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'e279714512f0498ee888c84f1906de2a5e6bf082d60fdbb32de84a0c16f6f071',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 1]], 'C': [1.0], 'O': [['C', 0]]},
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
	a = gc_e279714512f0498ee888c84f1906de2a5e6bf082d60fdbb32de84a0c16f6f071((i[1],))
	return (1.0,)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:04.016873Z',
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
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-13T17:50:59.855157Z',
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
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:07.949940Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'b4dc32c9bc15e51d8070be7bf0ee9bfc344b73cc8ec857978ff72e71a3efb911',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0], ['C', 0], ['C', 1]],
           'C': [0.0, 0.0],
           'O': [['A', 1]]},
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
 'signature': 'e3f608304dd03aacec080715777dd780d6488977a115c98932e042b63d69c6e1'}
'''
def gc_e3f608304dd03aacec080715777dd780d6488977a115c98932e042b63d69c6e1(i):
	a = gc_b4dc32c9bc15e51d8070be7bf0ee9bfc344b73cc8ec857978ff72e71a3efb911((i[0], 0.0, 0.0,))
	return (a[1],)


'''
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:52:33.772001Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '4140f47e72adf3343c04c82d7766bf9e3bc71a6b606b7bc2e93f45a6349792e5',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0], ['I', 1]], 'C': [-1.0], 'O': [['C', 0]]},
 'meta_data': {'parents': [['b33df5beef7cd7d5e49e74b229864ba0664bae07dbe6a28a3c9c11643518f37d']]},
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
 'signature': 'e91f5b6057a2fa10a195258260de4a39639f3b909db0b6e9495f56f8f3398480'}
'''
def gc_e91f5b6057a2fa10a195258260de4a39639f3b909db0b6e9495f56f8f3398480(i):
	a = gc_4140f47e72adf3343c04c82d7766bf9e3bc71a6b606b7bc2e93f45a6349792e5((i[0], i[1],))
	return (-1.0,)


'''
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-13T17:50:59.989752Z',
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
 'created': '2020-07-13T17:50:59.828808Z',
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
 'created': '2020-07-13T17:50:59.805544Z',
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
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:19.695458Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': '7404cd51f0ff21ae1b51cd8e13b6bacf706cafde670c9ef05ae282fea9ff2364',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['I', 0]], 'O': [['A', 0]]},
 'meta_data': {'parents': [['bc79a0da85fd799928bd29601213255ea269b68c594e223ee11742902035515d']]},
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
{'alpha_class': 0,
 'beta_class': 0,
 'code_depth': 1,
 'codon_depth': 1,
 'created': '2020-07-13T17:51:00.014518Z',
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
{'alpha_class': 1,
 'beta_class': -1,
 'code_depth': 2,
 'codon_depth': 1,
 'created': '2020-07-13T17:53:00.049330Z',
 'creator': '0000000000000000000000000000000000000000000000000000000000000000',
 'gca': 'ee2cc4658d03ebb3ffbcdc44d31fa89b7644a654567d66b93bac5f6186899d4d',
 'gcb': '0000000000000000000000000000000000000000000000000000000000000000',
 'generation': 2,
 'graph': {'A': [['C', 0], ['I', 0], ['I', 0]], 'C': [-1.0], 'O': [['A', 0]]},
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
 'signature': 'ffa10a3b9dcca40b999152e57ec932a3dabf240cc3c92b50a0a02044b6f93267'}
'''
def gc_ffa10a3b9dcca40b999152e57ec932a3dabf240cc3c92b50a0a02044b6f93267(i):
	a = gc_ee2cc4658d03ebb3ffbcdc44d31fa89b7644a654567d66b93bac5f6186899d4d((-1.0, i[0], i[0],))
	return (a[0],)


meta_data = {
	'ce4e58fcbe55e5caf14c456fd2603a7d81c19e89e61e63b0e56f8c1958ba3da1':{'num_inputs': 2,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': False, 'binary_mutation': True, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_ce4e58fcbe55e5caf14c456fd2603a7d81c19e89e61e63b0e56f8c1958ba3da1 },
	'4140f47e72adf3343c04c82d7766bf9e3bc71a6b606b7bc2e93f45a6349792e5':{'num_inputs': 2,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_4140f47e72adf3343c04c82d7766bf9e3bc71a6b606b7bc2e93f45a6349792e5 },
	'fcba468768bf701a1234ea41739916b0655512c74c74e5930cae35d13b92925f':{'num_inputs': 2,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_fcba468768bf701a1234ea41739916b0655512c74c74e5930cae35d13b92925f },
	'ea549df0fcde3b6375528205fef6eea94b79a442fd8afa77905fbeab96c6bcea':{'num_inputs': 2,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_ea549df0fcde3b6375528205fef6eea94b79a442fd8afa77905fbeab96c6bcea },
	'bcf49ecb02279621bc1dd9d70265175f142ccfcc742ff07cf3983c830c4670fc':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_bcf49ecb02279621bc1dd9d70265175f142ccfcc742ff07cf3983c830c4670fc },
	'81b5a567e50cf6fd71bfcfc3c5d23faa0f245fb0a71900fa9573eba1a94ee80d':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_81b5a567e50cf6fd71bfcfc3c5d23faa0f245fb0a71900fa9573eba1a94ee80d },
	'7404cd51f0ff21ae1b51cd8e13b6bacf706cafde670c9ef05ae282fea9ff2364':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_7404cd51f0ff21ae1b51cd8e13b6bacf706cafde670c9ef05ae282fea9ff2364 },
	'7bb5eb204e326fbabe069fb824e88a6ca68ec34c39eaa05a4d271a3f92e4b4fd':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_7bb5eb204e326fbabe069fb824e88a6ca68ec34c39eaa05a4d271a3f92e4b4fd },
	'e279714512f0498ee888c84f1906de2a5e6bf082d60fdbb32de84a0c16f6f071':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_e279714512f0498ee888c84f1906de2a5e6bf082d60fdbb32de84a0c16f6f071 },
	'ee2cc4658d03ebb3ffbcdc44d31fa89b7644a654567d66b93bac5f6186899d4d':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_ee2cc4658d03ebb3ffbcdc44d31fa89b7644a654567d66b93bac5f6186899d4d },
	'f131f1d7c087d2b567acec3f2a476de27b9110e0794c11b2c97098e878feed08':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_f131f1d7c087d2b567acec3f2a476de27b9110e0794c11b2c97098e878feed08 },
	'b4dc32c9bc15e51d8070be7bf0ee9bfc344b73cc8ec857978ff72e71a3efb911':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_b4dc32c9bc15e51d8070be7bf0ee9bfc344b73cc8ec857978ff72e71a3efb911 },
	'c436ba9675317cfa2b5e32a3f00cf08b57295e06f28d5203fbaa1cd6b430e6d7':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_c436ba9675317cfa2b5e32a3f00cf08b57295e06f28d5203fbaa1cd6b430e6d7 },
	'23c441e967ef4b8637554409522bc07c1d0faac129bccf73473c098650a63957':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_23c441e967ef4b8637554409522bc07c1d0faac129bccf73473c098650a63957 },
	'5f1ff9bfaf9bc1cdb5d520bd056048ebe5467cc6580f03b9c0c29b7eb64c4d2b':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_5f1ff9bfaf9bc1cdb5d520bd056048ebe5467cc6580f03b9c0c29b7eb64c4d2b },
	'4f54b44dd522c044b41833089ca47ece6b280ff8c11324a5b8b6a957d92f6de8':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_4f54b44dd522c044b41833089ca47ece6b280ff8c11324a5b8b6a957d92f6de8 },
	'a95ea10e7327badf07045086c7e935f5cc66a9b47f323fcdf30d76f66a592829':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_a95ea10e7327badf07045086c7e935f5cc66a9b47f323fcdf30d76f66a592829 },
	'63971bfb77792f35cda0463d310e2724ae108354fb287df386ab88a752743fcc':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_63971bfb77792f35cda0463d310e2724ae108354fb287df386ab88a752743fcc },
	'4793e082e2462b3ed47a23c000e9e8165bf7b6dea9bde08182b7203a708f6214':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_4793e082e2462b3ed47a23c000e9e8165bf7b6dea9bde08182b7203a708f6214 },
	'6bba0589ed454784e75f8a184fb8fc8d59a3772e73a8414f2ba915ce211f6773':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_6bba0589ed454784e75f8a184fb8fc8d59a3772e73a8414f2ba915ce211f6773 },
	'278ddaaaa439429bad68df4b81f3b42ecdc7cf2d2ea8ad086a2ca185a3acbbb6':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_278ddaaaa439429bad68df4b81f3b42ecdc7cf2d2ea8ad086a2ca185a3acbbb6 },
	'b3426a0b5077c14d09c2eb091e8ba0ded68486890d5f0146cfdec34ebbe383d6':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_b3426a0b5077c14d09c2eb091e8ba0ded68486890d5f0146cfdec34ebbe383d6 },
	'81d83b6dfe8764bc32df13948a86e7721818e3648d8f916708f8d416b2b94370':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_81d83b6dfe8764bc32df13948a86e7721818e3648d8f916708f8d416b2b94370 },
	'102a4d1fc747c5f81b314937da02b830ca4a49a6010aa65fd478dd1bd68675e8':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_102a4d1fc747c5f81b314937da02b830ca4a49a6010aa65fd478dd1bd68675e8 },
	'4cde93184158819b805ef591641fad84f4c0ee4fdb2715d267cbbcce1a53f8a4':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 0,'beta_class': 0, 'callable': gc_4cde93184158819b805ef591641fad84f4c0ee4fdb2715d267cbbcce1a53f8a4 },
	'282424295de4addaa42b8117a6e53ce0136fcfba2b1cdfab61ac3c7e3a823516':{'num_inputs': 2,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_282424295de4addaa42b8117a6e53ce0136fcfba2b1cdfab61ac3c7e3a823516 },
	'0b71cf0dd17adf2126959c3712c97c25420a33cb71657225c3d76c127a2d3f8d':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_0b71cf0dd17adf2126959c3712c97c25420a33cb71657225c3d76c127a2d3f8d },
	'cc7cfb52a4658ba440bd7691c5a3d6f736f94d3d795857725a2e400f9e3624a9':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_cc7cfb52a4658ba440bd7691c5a3d6f736f94d3d795857725a2e400f9e3624a9 },
	'03d3eaff46ecd43fd8772beef3c985fcf4de70c55d53552835bec4cc71bffb04':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_03d3eaff46ecd43fd8772beef3c985fcf4de70c55d53552835bec4cc71bffb04 },
	'7bf45529286677eb2266ff38b3c8a6a898ea41a3cbe831a2e60b1397faa8c106':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_7bf45529286677eb2266ff38b3c8a6a898ea41a3cbe831a2e60b1397faa8c106 },
	'562f9ffb473aade86537c9d78a94314f32cc0e1e6a5c71926777777c5fd35bbf':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_562f9ffb473aade86537c9d78a94314f32cc0e1e6a5c71926777777c5fd35bbf },
	'65205972c2842865c3b8de9cd43d117c8bc0ff4fc05f27284d93416cd604dcf4':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_65205972c2842865c3b8de9cd43d117c8bc0ff4fc05f27284d93416cd604dcf4 },
	'15351a2e310bb0e2f6189d1728d5eee750c673dcb0b15c0f40302c6ef4e33535':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_15351a2e310bb0e2f6189d1728d5eee750c673dcb0b15c0f40302c6ef4e33535 },
	'b98b16eb6649388de0a5294dcbde704470050a9c23850db69a1b239bd6788ee6':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_b98b16eb6649388de0a5294dcbde704470050a9c23850db69a1b239bd6788ee6 },
	'830056fc717060a25cfa061faedab989fdbc7208958cac782cfddff53a9de65b':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_830056fc717060a25cfa061faedab989fdbc7208958cac782cfddff53a9de65b },
	'66ac33a3f469fe70a0c72886b61ccd32f2b9b4738c8dd22112ba9e47ebe4ff2b':{'num_inputs': 2,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': False, 'binary_mutation': True, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_66ac33a3f469fe70a0c72886b61ccd32f2b9b4738c8dd22112ba9e47ebe4ff2b },
	'a380199b1efb5e06e8bf0ba253f2250b665534df9402e9ba08405876a9d0911b':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_a380199b1efb5e06e8bf0ba253f2250b665534df9402e9ba08405876a9d0911b },
	'7c81e32cacdeb941a0c6989d24d58a9591a9771cce66ec0752ebbd0b2e1f5eae':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_7c81e32cacdeb941a0c6989d24d58a9591a9771cce66ec0752ebbd0b2e1f5eae },
	'cf8cd9075b571cb5a59d37e378029ff54502df66779163ba058c01384f335c2c':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_cf8cd9075b571cb5a59d37e378029ff54502df66779163ba058c01384f335c2c },
	'7c30338bf43f14fc54b72811e0cefdd09bf2bb87ce61b2a2fd192ade84cebba0':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_7c30338bf43f14fc54b72811e0cefdd09bf2bb87ce61b2a2fd192ade84cebba0 },
	'bc79a0da85fd799928bd29601213255ea269b68c594e223ee11742902035515d':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_bc79a0da85fd799928bd29601213255ea269b68c594e223ee11742902035515d },
	'7743aba320d9a6dd5f2b7a8e5777b997d61131f2a4db0f78fb4a881d40244898':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_7743aba320d9a6dd5f2b7a8e5777b997d61131f2a4db0f78fb4a881d40244898 },
	'5a133701ad6928931161f8dd2537b225cfb54c18f2b49efcc6fd743ccb8c062c':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_5a133701ad6928931161f8dd2537b225cfb54c18f2b49efcc6fd743ccb8c062c },
	'de16d05c96f141351c6e918906ad8565426b05c77a187edc20763c01f4d8db86':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_de16d05c96f141351c6e918906ad8565426b05c77a187edc20763c01f4d8db86 },
	'3669b2f53208e322423da38d8006444917940ddfedbf169eaf0212c0fe6f10b7':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_3669b2f53208e322423da38d8006444917940ddfedbf169eaf0212c0fe6f10b7 },
	'57445022b9dc0d937721bb272de55001607f26c9b9cc9dd40cd4dead77da6366':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_57445022b9dc0d937721bb272de55001607f26c9b9cc9dd40cd4dead77da6366 },
	'b33df5beef7cd7d5e49e74b229864ba0664bae07dbe6a28a3c9c11643518f37d':{'num_inputs': 2,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_b33df5beef7cd7d5e49e74b229864ba0664bae07dbe6a28a3c9c11643518f37d },
	'c377bcc1307f651040c84d99eee44a7a4bf29e9b84c7a3233ca539498a14bef1':{'num_inputs': 2,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_c377bcc1307f651040c84d99eee44a7a4bf29e9b84c7a3233ca539498a14bef1 },
	'a427790d770b0fa722ca1ebae60ce603fbc45f0358ed7df37f88f0a042284a70':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_a427790d770b0fa722ca1ebae60ce603fbc45f0358ed7df37f88f0a042284a70 },
	'42bdabf6208e9529f50a37386efafc88a45bdd1ed90be29c97a18041626dba9b':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_42bdabf6208e9529f50a37386efafc88a45bdd1ed90be29c97a18041626dba9b },
	'065c6b174b50d8682b49d71112febf3f052ad94f794cef68009887ae1bc09b69':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_065c6b174b50d8682b49d71112febf3f052ad94f794cef68009887ae1bc09b69 },
	'33a14972c04f1771bc6bf7871d7438d38eec27ddfee6bdc23a2c4089f6f6f182':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_33a14972c04f1771bc6bf7871d7438d38eec27ddfee6bdc23a2c4089f6f6f182 },
	'46b77d4a61398a228ef0b64e465cc33ee6f4527980586ea4a40ab2e6d3aedec0':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_46b77d4a61398a228ef0b64e465cc33ee6f4527980586ea4a40ab2e6d3aedec0 },
	'2a30f8b83f964a470b4c68e8c30d112f99cfca4a2ca3acf15cecf94aa5e3804f':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_2a30f8b83f964a470b4c68e8c30d112f99cfca4a2ca3acf15cecf94aa5e3804f },
	'e3f608304dd03aacec080715777dd780d6488977a115c98932e042b63d69c6e1':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_e3f608304dd03aacec080715777dd780d6488977a115c98932e042b63d69c6e1 },
	'aa8b534a5c93cfb139aeaa0ddda00367b2e88cace02bbdef8274aa9fb61ce4fe':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_aa8b534a5c93cfb139aeaa0ddda00367b2e88cace02bbdef8274aa9fb61ce4fe },
	'bfd010ec1db290614a408872aa7e43640a50e11f035a47bd2d484cc080db8b8a':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_bfd010ec1db290614a408872aa7e43640a50e11f035a47bd2d484cc080db8b8a },
	'db707d1e30841606ccbc7f7d349dcdadcf7b3b5e1e8d1a2e8cec17e1317bfd13':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_db707d1e30841606ccbc7f7d349dcdadcf7b3b5e1e8d1a2e8cec17e1317bfd13 },
	'aab332740bb7b6730311c956b05c16d19814c2d752e1db38b65aa95c7b9209d7':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_aab332740bb7b6730311c956b05c16d19814c2d752e1db38b65aa95c7b9209d7 },
	'69f8bddf1ba8386b128c82b9e9d61bfbcd39a2adfb0f072e1c0edd6fc96c2b5e':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_69f8bddf1ba8386b128c82b9e9d61bfbcd39a2adfb0f072e1c0edd6fc96c2b5e },
	'670a0aa12cc1491b80aa34adae09fa3a0e801f4b0d3cd47851fb452b736fbe1a':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_670a0aa12cc1491b80aa34adae09fa3a0e801f4b0d3cd47851fb452b736fbe1a },
	'31e4e3af86f9d2a46cdc37171097324bfe35d2459baa32d61f46fe95742ba07e':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_31e4e3af86f9d2a46cdc37171097324bfe35d2459baa32d61f46fe95742ba07e },
	'f269bf2281717b6c6d4cd1c4f6bdd61dd63f8501ed8a3846b79dca9c82387a51':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_f269bf2281717b6c6d4cd1c4f6bdd61dd63f8501ed8a3846b79dca9c82387a51 },
	'87d95699b95f73b0d9cd4b559dce51d13722fd143c7cc9b0b6be5430f0fdff56':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_87d95699b95f73b0d9cd4b559dce51d13722fd143c7cc9b0b6be5430f0fdff56 },
	'bf3161b1d66c4f7b2c4d7c9901bd0044d3dcb0e2bc05dbe82e1feeeb40ef9931':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_bf3161b1d66c4f7b2c4d7c9901bd0044d3dcb0e2bc05dbe82e1feeeb40ef9931 },
	'8568fa49a69fc9c42c30d78866a45316976afca26ce6a75284546f07ad9f6aef':{'num_inputs': 2,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_8568fa49a69fc9c42c30d78866a45316976afca26ce6a75284546f07ad9f6aef },
	'680d118644077298a193b75aa60abd05063f6892893c6dc4f02660352eee472b':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_680d118644077298a193b75aa60abd05063f6892893c6dc4f02660352eee472b },
	'9a373664d556d7975eab9f9bc390debc5d26c570fa64acbb247cadac27883008':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_9a373664d556d7975eab9f9bc390debc5d26c570fa64acbb247cadac27883008 },
	'1745bd810b62f97916ccde4247e74fb6b04fa3e07a0a2349d115daea3708c540':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_1745bd810b62f97916ccde4247e74fb6b04fa3e07a0a2349d115daea3708c540 },
	'572f3d56521fb576738b38239b46b1f2e4f881dbeb18ba57b3254a6dceb5782e':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_572f3d56521fb576738b38239b46b1f2e4f881dbeb18ba57b3254a6dceb5782e },
	'20f3364de91953b7b0e5e590831d3b36e2afd02defc8ec4ea0d221fa23224d17':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_20f3364de91953b7b0e5e590831d3b36e2afd02defc8ec4ea0d221fa23224d17 },
	'3e499d7ca7138daf82cd99d0bb2e48aaed172cb47d090509f67041489cccd15d':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_3e499d7ca7138daf82cd99d0bb2e48aaed172cb47d090509f67041489cccd15d },
	'7f20a5d632ea8a8387010dfa728eea4f15e28e973ba812e3933c40e3deb09a98':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_7f20a5d632ea8a8387010dfa728eea4f15e28e973ba812e3933c40e3deb09a98 },
	'd91aec2848d9b2a917bc2edbf315e5c015fd56e9b4d961d39eaf7bdc07228eb4':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_d91aec2848d9b2a917bc2edbf315e5c015fd56e9b4d961d39eaf7bdc07228eb4 },
	'9b4e6a07d07413e898e7a996c44cd4182c6b7a805b106ef76bf28176c2103d32':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_9b4e6a07d07413e898e7a996c44cd4182c6b7a805b106ef76bf28176c2103d32 },
	'8302f7ebfa7604701b0799d946b8c2c578d3a1f9723699b97cb4598d4a9ad955':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_8302f7ebfa7604701b0799d946b8c2c578d3a1f9723699b97cb4598d4a9ad955 },
	'412893aa241dbb25bc8766eb459e0b255d8913ab368b600b587ca912dd5f730c':{'num_inputs': 0,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_412893aa241dbb25bc8766eb459e0b255d8913ab368b600b587ca912dd5f730c },
	'd0ac245cf0c9cfef6bb2c46fb713f8c2afd785eec8418f371cdc4f1ae48be228':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_d0ac245cf0c9cfef6bb2c46fb713f8c2afd785eec8418f371cdc4f1ae48be228 },
	'25345bc7f15998f42c66172678da46b0847a9ca2f723d3b9b72cdbaacf3fd8a3':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_25345bc7f15998f42c66172678da46b0847a9ca2f723d3b9b72cdbaacf3fd8a3 },
	'e91f5b6057a2fa10a195258260de4a39639f3b909db0b6e9495f56f8f3398480':{'num_inputs': 2,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_e91f5b6057a2fa10a195258260de4a39639f3b909db0b6e9495f56f8f3398480 },
	'9e7fe73ca9e453aa6fb3427a5aaf36069ac317d01720ccbb6b2e2d20ec7deb63':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_9e7fe73ca9e453aa6fb3427a5aaf36069ac317d01720ccbb6b2e2d20ec7deb63 },
	'ffa10a3b9dcca40b999152e57ec932a3dabf240cc3c92b50a0a02044b6f93267':{'num_inputs': 1,'num_outputs': 1,'properties': {'extended': False, 'unary_mutation': True, 'binary_mutation': False, 'mathematical': False, 'logical': False, 'conditional': False},'alpha_class': 1,'beta_class': -1, 'callable': gc_ffa10a3b9dcca40b999152e57ec932a3dabf240cc3c92b50a0a02044b6f93267 }
}
