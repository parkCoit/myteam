import numpy
from transformers import GPT2LMHeadModel

from transformers import PreTrainedTokenizerFast
import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import PreTrainedTokenizerFast, GPT2LMHeadModel
import re
import urllib.request

Q_TKN = "<usr>"
A_TKN = "<sys>"
BOS = '</s>'
EOS = '</s>'
MASK = '<unused0>'
SENT = '<unused1>'
PAD = '<pad>'
sent = '자연어 처리는'
koGPT2_TOKENIZER = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
                                                           bos_token=BOS, eos_token=EOS, unk_token='<unk>',
                                                           pad_token=PAD, mask_token=MASK)


class ChatbotDataset(Dataset):
    def __init__(self, chats, max_len=40):  # 데이터셋의 전처리를 해주는 부분
        self._data = chats
        self.max_len = max_len
        self.q_token = Q_TKN
        self.a_token = A_TKN
        self.sent_token = SENT
        self.eos = EOS
        self.mask = MASK
        self.tokenizer = koGPT2_TOKENIZER

    def __len__(self):  # chatbotdata 의 길이를 리턴한다.
        return len(self._data)

    def __getitem__(self, idx):  # 로드한 챗봇 데이터를 차례차례 DataLoader로 넘겨주는 메서드
        turn = self._data.iloc[idx]
        q = turn["Q"]  # 질문을 가져온다.
        q = re.sub(r"([?.!,])", r" ", q)  # 구둣점들을 제거한다.

        a = turn["A"]  # 답변을 가져온다.
        a = re.sub(r"([?.!,])", r" ", a)  # 구둣점들을 제거한다.

        q_toked = self.tokenizer.tokenize(self.q_token + q + self.sent_token)
        q_len = len(q_toked)

        a_toked = self.tokenizer.tokenize(self.a_token + a + self.eos)
        a_len = len(a_toked)

        # 질문의 길이가 최대길이보다 크면
        if q_len > self.max_len:
            a_len = self.max_len - q_len  # 답변의 길이를 최대길이 - 질문길이
            if a_len <= 0:  # 질문의 길이가 너무 길어 질문만으로 최대 길이를 초과 한다면
                q_toked = q_toked[-(int(self.max_len / 2)):]  # 질문길이를 최대길이의 반으로
                q_len = len(q_toked)
                a_len = self.max_len - q_len  # 답변의 길이를 최대길이 - 질문길이
            a_toked = a_toked[:a_len]
            a_len = len(a_toked)

        # 질문의 길이 + 답변의 길이가 최대길이보다 크면
        if q_len + a_len > self.max_len:
            a_len = self.max_len - q_len  # 답변의 길이를 최대길이 - 질문길이
            if a_len <= 0:  # 질문의 길이가 너무 길어 질문만으로 최대 길이를 초과 한다면
                q_toked = q_toked[-(int(self.max_len / 2)):]  # 질문길이를 최대길이의 반으로
                q_len = len(q_toked)
                a_len = self.max_len - q_len  # 답변의 길이를 최대길이 - 질문길이
            a_toked = a_toked[:a_len]
            a_len = len(a_toked)

        # 답변 labels = [mask, mask, ...., mask, ..., <bos>,..답변.. <eos>, <pad>....]
        labels = [self.mask, ] * q_len + a_toked[1:]

        # mask = 질문길이 0 + 답변길이 1 + 나머지 0
        mask = [0] * q_len + [1] * a_len + [0] * (self.max_len - q_len - a_len)
        # 답변 labels을 index 로 만든다.
        labels_ids = self.tokenizer.convert_tokens_to_ids(labels)
        # 최대길이만큼 PADDING
        while len(labels_ids) < self.max_len:
            labels_ids += [self.tokenizer.pad_token_id]

        # 질문 + 답변을 index 로 만든다.
        token_ids = self.tokenizer.convert_tokens_to_ids(q_toked + a_toked)
        # 최대길이만큼 PADDING
        while len(token_ids) < self.max_len:
            token_ids += [self.tokenizer.pad_token_id]

        # 질문+답변, 마스크, 답변
        return token_ids, np.array(mask), labels_ids


class Sk_ChatBot(ChatbotDataset):
    def collate_batch(batch):
        data = numpy.array([item[0] for item in batch])
        mask = numpy.array([item[1] for item in batch])
        label = numpy.array([item[2] for item in batch])
        return torch.LongTensor(data), torch.LongTensor(mask), torch.LongTensor(label)

    def finishsentence(self):
        tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2", bos_token='</s>', eos_token='</s>',
                                                            unk_token='<unk>', pad_token='<pad>', mask_token='<mask>')
        tokenizer.tokenize("안녕하세요. 한국어 GPT-2 입니다.😤:)l^o")
        model = GPT2LMHeadModel.from_pretrained('skt/kogpt2-base-v2')
        text = '근육이 커지기 위해서는'
        input_ids = tokenizer.encode(text)
        gen_ids = model.generate(torch.tensor([input_ids]),
                                 max_length=128,
                                 repetition_penalty=2.0,
                                 pad_token_id=tokenizer.pad_token_id,
                                 eos_token_id=tokenizer.eos_token_id,
                                 bos_token_id=tokenizer.bos_token_id,
                                 use_cache=True)
        generated = tokenizer.decode(gen_ids[0, :].tolist())
        print(generated)

    def chatbot_train(self):
        model = GPT2LMHeadModel.from_pretrained('skt/kogpt2-base-v2')
        print('1')
        Chatbot_Data = pd.read_csv("ChatBotData.csv")
        print('2')
        # Test 용으로 300개 데이터만 처리한다.
        Chatbot_Data = Chatbot_Data[:300]
        print('3')
        Chatbot_Data.head()
        print('4')
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print('5')
        train_set = ChatbotDataset(Chatbot_Data, max_len=40)
        print('6')
        # 윈도우 환경에서 num_workers 는 무조건 0으로 지정, 리눅스에서는 2
        train_dataloader = DataLoader(train_set, batch_size=32, num_workers=0, shuffle=True,
                                      collate_fn=self.collate_batch)
        print('7')
        model.to(device)
        print('8')
        model.train()
        print('9')
        learning_rate = 3e-5
        print('10')
        criterion = torch.nn.CrossEntropyLoss(reduction="none")
        print('11')
        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

        epoch = 10
        Sneg = -1e18
        print("start")
        check = 0
        for epoch in range(epoch):
            print(check)
            for batch_idx, samples in enumerate(train_dataloader):  ##문제
                print('check after')
                optimizer.zero_grad()
                token_ids, mask, label = samples
                out = model(token_ids)
                out = out.logits  # Returns a new tensor with the logit of the elements of input
                mask_3d = mask.unsqueeze(dim=2).repeat_interleave(repeats=out.shape[2], dim=2)
                mask_out = torch.where(mask_3d == 1, out, Sneg * torch.ones_like(out))
                loss = criterion(mask_out.transpose(2, 1), label)
                # 평균 loss 만들기 avg_loss[0] / avg_loss[1] <- loss 정규화
                avg_loss = loss.sum() / mask.sum()
                avg_loss.backward()
                # 학습 끝
                optimizer.step()
            check += 1
        print("end")

    def chatbot_test(self):
        model = GPT2LMHeadModel.from_pretrained('skt/kogpt2-base-v2')
        with torch.no_grad():
            while 1:
                q = input("user > ").strip()
                if q == "quit":
                    break
                a = ""
                while 1:
                    input_ids = torch.LongTensor(
                        koGPT2_TOKENIZER.encode(Q_TKN + q + SENT + A_TKN + a)).unsqueeze(dim=0)
                    pred = model(input_ids)
                    pred = pred.logits
                    gen = koGPT2_TOKENIZER.convert_ids_to_tokens(torch.argmax(pred, dim=-1).squeeze().numpy().tolist())[
                        -1]
                    if gen == EOS:
                        break
                    a += gen.replace("▁", " ")
                print("Chatbot > {}".format(a.strip()))


if __name__ == "__main__":
    data = pd.read_csv('ChatBotData.csv')
    chatbot = Sk_ChatBot(data)
    chatbot.chatbot_train()
    # chatbot.finishsentence()
    # print('*'*500)
