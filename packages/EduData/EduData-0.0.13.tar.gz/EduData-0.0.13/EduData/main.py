# coding: utf-8
# 2019/8/23 @ tongshiwei

import fire

from EduData.DataSet.download_data.download_data import get_data, list_resources
from EduData.Task.KnowledgeTracing.format import tl2json, json2tl
from EduData.Task.KnowledgeTracing.statistics import analysis_records, analysis_edges
from longling.ML.toolkit.dataset import train_valid_test, kfold
from EduData.DataSet.junyi import extract_relations, build_json_sequence
from EduData.DataSet.EdNet import build_interactions, select_n_most_active
from EduData.Task.KnowledgeTracing.graph import dense_graph, transition_graph, correct_transition_graph
from EduData.Task.KnowledgeTracing.graph import similarity_graph, concurrence_graph, correct_co_influence_graph


def cli():  # pragma: no cover
    fire.Fire(
        {
            "download": get_data,
            "ls": list_resources,
            "tl2json": tl2json,
            "json2tl": json2tl,
            "kt_stat": analysis_records,
            "edge_stat": analysis_edges,
            "train_valid_test": train_valid_test,
            "kfold": kfold,
            "dataset": {
                "junyi": {
                    "kt": {
                        "extract_relations": extract_relations,
                        "build_json_sequence": build_json_sequence,
                    }
                },
                "ednet": {
                    "kt": {
                        "build_json_sequence": build_interactions,
                        "select_n": select_n_most_active,
                    }
                }
            },
            "graph": {
                "ccon": correct_co_influence_graph,
                "con": concurrence_graph,
                "dense": dense_graph,
                "trans": transition_graph,
                "ctrans": correct_transition_graph,
                "sim": similarity_graph,
            }
        }
    )
