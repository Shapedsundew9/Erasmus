from json import dump


gc_types = {}

gc_types["gc_list"] = {
    "type": "list",
    "schema": {
        "value_types": "gc",
        "minlength": 1
    }
}

gc_query_keys = [
    "signature",
    "gca",
    "gcb",
    "reference_count",
    "generation",
    "code_depth",
    "codon_depth",
    "num_codes",
    "num_unique_codes",
    "raw_num_codons",
    "opt_num_codons",
    "num_inputs",
    "input0_type",
    "input1_type",
    "input2_type",
    "input3_type",
    "input4_type",
    "input5_type",
    "input6_type",
    "input7_type",
    "num_outputs",
    "output0_type",
    "output1_type",
    "output2_type",
    "output3_type",
    "alpha_class",
    "beta_class",
    "properties",
    "fitness",
    "evolvability",
    "creator",
    "updated",
    "created",
    "order_by",
    "limit",
    "random"
]

gc_query_value_types = [
    "gc_signature",
    "gc_signature",
    "gc_signature",
    "gc_reference_count",
    "gc_generation",
    "gc_code_depth",
    "gc_codon_depth",
    "gc_num_codes",
    "gc_num_unique_codes",
    "gc_raw_num_codons",
    "gc_opt_num_codons",
    "gc_num_inputs",
    "gc_type",
    "gc_type",
    "gc_type",
    "gc_type",
    "gc_type",
    "gc_type",
    "gc_type",
    "gc_type",
    "gc_num_outputs",
    "gc_type",
    "gc_type",
    "gc_type",
    "gc_type",
    "gc_class",
    "gc_class",
    "gc_properties",
    "gc_fitness",
    "gc_evolvability",
    "gc_creator",
    "gc_updated",
    "gc_created",
    "gc_query_order_by",
    "uint8",
    "bool"
]


gc_types['gc_query'] = {
    "type": "dict",
    "read-only": False,
    "schema": {
    }
}


gc_types['gc_query_order_by'] = {
    "type": "string",
    "read-only": False,
    "allowed": gc_query_keys
}


for k, v in zip(gc_query_keys, gc_query_value_types):
    if "gc_" in v:
        new_type = v.replace("gc_", "gc_query_")
        gc_types['gc_query']['schema'][k] = {"type": new_type, "read-only": False}
        if k != "properties":
            gc_types[new_type] = {
                "type": [v, v + "_list"],
                "read-only": False
            }
            gc_types[v + "_list"] = {
                "type": "list",
                "read-only": False,
                "schema": {
                    "type": v
                },
                "minlength": 1,
                "maxlength": 256
            }
            gc_types['gc_query']['schema'][k] = {"type": new_type, "read-only": False}
            if k in (
                "gc_reference_count",
                "gc_generation",
                "gc_code_depth",
                "gc_codon_depth",
                "gc_num_codes",
                "gc_num_unique_codes",
                "gc_raw_num_codons",
                "gc_opt_num_codons",
                "gc_num_inputs",
                "gc_num_outputs",
                "gc_class",
                "gc_fitness",
                "gc_evolvability",
                "gc_updated",
                "gc_created"
            ):
                gc_types[new_type]["type"].extend((v + "_min", v + "_max", v + "_range"))
                gc_types[v + "_min"] = {
                    "type": "dict",
                    "read-only": False,
                    "schema": {
                        "min": {
                            "type": "v",
                            "read-only": False
                        }
                    }
                }
                gc_types[v + "_max"] = {
                    "type": "dict",
                    "read-only": False,
                    "schema": {
                        "max": {
                            "type": "v",
                            "read-only": False
                        }
                    }
                }
                gc_types[v + "_range"] = {
                    "type": "dict",
                    "read-only": False,
                    "schema": {
                        "min": {
                            "type": "v",
                            "read-only": False
                        },
                        "max": {
                            "type": "v",
                            "read-only": False
                        }
                    }
                }
        else:
            gc_types[new_type] = {
                "type": [v, "int64"],
                "read-only": False
            }


with open('gc_query_types.json', 'w') as njsonfile:
    dump(gc_types, njsonfile, indent=4, sort_keys=True)
        