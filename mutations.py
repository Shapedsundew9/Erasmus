# Erasmus GP Gene Pool


from microbiome.genetics.gc_mutation_functions import *
from random import random


def gc_ce4e58fcbe55e5caf14c456fd2603a7d81c19e89e61e63b0e56f8c1958ba3da1(i):
	return (stack(i[0], i[1]),)


def gc_4140f47e72adf3343c04c82d7766bf9e3bc71a6b606b7bc2e93f45a6349792e5(i):
	return (mutate_constant(i[0], i[1], -1.0),)


def gc_fcba468768bf701a1234ea41739916b0655512c74c74e5930cae35d13b92925f(i):
	return (mutate_constant(i[0], i[1], 0.5),)


def gc_ea549df0fcde3b6375528205fef6eea94b79a442fd8afa77905fbeab96c6bcea(i):
	return (mutate_constant(i[0], i[1], 1.5),)


def gc_81b5a567e50cf6fd71bfcfc3c5d23faa0f245fb0a71900fa9573eba1a94ee80d(i):
	return (append_constant(i[0], 0.0),)


def gc_7404cd51f0ff21ae1b51cd8e13b6bacf706cafde670c9ef05ae282fea9ff2364(i):
	return (append_constant(i[0], -1.0),)


def gc_7bb5eb204e326fbabe069fb824e88a6ca68ec34c39eaa05a4d271a3f92e4b4fd(i):
	return (append_constant(i[0], 1.0),)


def gc_b92ef4788519865c1f1253887c3722b3c0860113cec9f5461e3fdc4d7c11f19f(i):
	return (append_constant(i[0], random(-1.0, 1.0)),)


def gc_1775c5e7dc2f2795da3379116dc7b247d6eecfdfc678a688b43d97a24de451d8(i):
	return (connect(i[0], 'O', 'C', 0.0, 0.0),)


def gc_3f384d919dcea9aac65918b24c96deeadda3f7d8fc40972cccb554a119d24ca9(i):
	return (connect(i[0], 'O', 'A', 0.0, 0.0),)


def gc_926b32d2bc59cdabada787445b9a592ad7bbac27d5e4a47315c71ebb847b968a(i):
	return (connect(i[0], 'O', 'I', 0.0, 0.0),)


def gc_f4718920110f018511f8c87bb23da8f67cb7139e3676356eedfdc890f5f1002a(i):
	return (connect(i[0], 'B', 'C', 0.0, 0.0),)


def gc_66f631fb1e0da9e80ec4b5b1f719e336f1775933f8d66ff0216f3ca1d7ba5576(i):
	return (connect(i[0], 'B', 'A', 0.0, 0.0),)


def gc_2f94122a16f522b1738db63f7aad4148ef6d947c96b44cff9db98e52cd850d3e(i):
	return (connect(i[0], 'B', 'I', 0.0, 0.0),)


def gc_b95b4f9d26990566624790b96c690b73b964a1907dba5bea03eb47d7c6c2c005(i):
	return (connect(i[0], 'A', 'C', 0.0, 0.0),)


def gc_e757a58c7b3f7781a1abe0dc246d3c9def253c889a77a6548da5555bb6f1dca5(i):
	return (connect(i[0], 'A', 'I', 0.0, 0.0),)


def gc_5fa0b1d47138a2787b8abd7de01bd065651a3c37870a91f1e66de611debb81d0(i):
	return (connect(i[0], 'O', 'C', random(), random()),)


def gc_0c827aaa1a48dc86f478c6c7cf4d97f989c1509d7482203e57f4fc76e6f88e50(i):
	return (connect(i[0], 'O', 'A', random(), random()),)


def gc_d6eb31fd546edd7958cb699dee14c1db4d119ee5c43d81b63e661ee3e94e0e7f(i):
	return (connect(i[0], 'O', 'I', random(), random()),)


def gc_e1d4f0ee70fc8a5c1002f40f87f3633e4ffb99457407c6c2907fc38b75539355(i):
	return (connect(i[0], 'B', 'C', random(), random()),)


def gc_d595e29c35f9e1ad64f167ea8b60e8618e0b8d6bcf21e685de5bb1d2c2eedba4(i):
	return (connect(i[0], 'B', 'A', random(), random()),)


def gc_1420c746963ee390cf60514c2d4164b70aaf37e25b1af7f38350dce22ecc9ef6(i):
	return (connect(i[0], 'B', 'I', random(), random()),)


def gc_d478bc0f1d51d76d78e003621fe18b76fe62fe5b272be2eb836ba9da52658077(i):
	return (connect(i[0], 'A', 'C', random(), random()),)


def gc_203ba752b9f378fcfc5550e2f03511ddc7087563fdf0f9fed0d2824466aff988(i):
	return (connect(i[0], 'A', 'I', random(), random()),)


