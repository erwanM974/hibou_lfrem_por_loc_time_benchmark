#
# Copyright 2023 Erwan Mahe (github.com/erwanM974)
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os

from implem.analyze import run_analyses
from implem.constants import INTERACTIONS_FOLDER, get_time_analysis_methods


def get_tracegen_folders(int_name):
    return [
        ("ACPT",os.path.join(INTERACTIONS_FOLDER, int_name + "_accepted")),
        ("PREF",os.path.join(INTERACTIONS_FOLDER, int_name + "_slices")),
        ("NOIS",os.path.join(INTERACTIONS_FOLDER, int_name + "_noise")),
        ("SACT",os.path.join(INTERACTIONS_FOLDER, int_name + "_swap_act")),
        ("SCMP",os.path.join(INTERACTIONS_FOLDER, int_name + "_swap_comp"))
    ]






def experiment(num_tries,timeout_in_secs):
    # parameterization
    analysis_methods = get_time_analysis_methods()
    # output
    results_filename = "results_time.csv"
    f = open(results_filename, "w")
    f.truncate(0) # empty file
    # ***
    columns = ["hif",
               "trace_kind",
               "htf",
               "trace_length",
               "verdict"]

    for method_name in analysis_methods:
        columns += [method_name + '_graph_size']
        columns += [method_name + '_time']
    f.write(";".join(columns) + "\n")
    f.flush()
    #
    for hif in os.listdir(INTERACTIONS_FOLDER):
        if hif.endswith(".hif"):
            hif_name = hif[:-4]
            hif_path = os.path.join(INTERACTIONS_FOLDER, hif)

            print("analyzing traces for : " + hif_name)
            for (trace_kind,trace_folder) in get_tracegen_folders(hif_name):
                for htf in os.listdir(trace_folder):
                    if htf.endswith(".htf"):
                        htf_name = htf[:-4]
                        htf_path = os.path.join(trace_folder,htf)
                        ana_dict = run_analyses(hif_path,htf_path,analysis_methods,num_tries,timeout_in_secs)
                        if ana_dict != None:
                            row = [
                                hif_name,
                                trace_kind,
                                htf_name,
                                str(ana_dict['trace_length']),
                                str(ana_dict['verdict'])
                            ]
                            for method_name in analysis_methods:
                                row += [str(ana_dict.get(method_name + '_graph_size'))]
                                row += [str(ana_dict.get(method_name + '_time'))]
                            print(row)
                            line = ";".join(row) + "\n"
                            f.write(line)
                            f.flush()


if __name__ == "__main__":
    experiment(3,3)

