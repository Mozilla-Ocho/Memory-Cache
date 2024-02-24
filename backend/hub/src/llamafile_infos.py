# llamafile_name_llava_v1_5_7b_q4 = "llava-v1.5-7b-q4.llamafile"
# llamafile_url_llava_v1_5_7b_q4 = "https://huggingface.co/jartine/llava-v1.5-7B-GGUF/resolve/main/llava-v1.5-7b-q4.llamafile?download=true"

# llamafile_name_mistral_7b_instruct_v0_2_q5_k_m = "mistral-7b-instruct-v0.2.Q5_K_M.llamafile"
# llamafile_url_mistral_7b_instruct_v0_2_q5_k_m = "https://huggingface.co/jartine/Mistral-7B-Instruct-v0.2-llamafile/resolve/main/mistral-7b-instruct-v0.2.Q5_K_M.llamafile?download=true"

# Parse the json in llamafile_infos.json
import json
import os

class LlamafileInfo:
    def __init__(self, info_dict):
        self.model = info_dict['Model']
        self.size = info_dict['Size']
        self.license = info_dict['License']
        self.license_url = info_dict['License URL']
        self.name = info_dict['filename']
        self.url = info_dict['url']

def get_llamafile_infos():
    llamafile_infos_path = os.path.join(os.path.dirname(__file__), "llamafile_infos.json")
    with open(llamafile_infos_path, "r") as f:
        llamafile_infos_dicts = json.load(f)

    # Convert each dictionary to a LlamafileInfo object
    llamafile_infos = [LlamafileInfo(info_dict) for info_dict in llamafile_infos_dicts]
    return llamafile_infos
