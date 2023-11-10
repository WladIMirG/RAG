import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from chatbot.src.utils import *
from tqdm import tqdm
from time import sleep

def main():
    # Load UVQuAD
    UVQuAD = pd.read_csv('data/processed/UVQuAD.csv')
    chatbot = MariTalkChatBot(
        retriever_data_path="data/processed/context_data.csv"
    )
    chatbot.conv.offset = -4
    data = []
    for i in tqdm(UVQuAD.index):
        q = UVQuAD['question'][i]
        response = chatbot.get_answer_from_maritalk(q)
        # print(f"response: {response}")
        data.append(
            {
                'id': i,
                "prediction_text": response,
            }
        )
        pd.DataFrame(data).to_csv('data/processed/MariTalk_predictions.csv', index=False)
        sleep(1)
        # pd.DataFrame(data).to_csv('data/processed/predictions.csv', index=False)

if __name__ == "__main__":
    main()