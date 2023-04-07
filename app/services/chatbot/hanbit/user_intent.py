from app.admin.GlobalParams import MAX_SEQ_LEN
from app.admin.Preprocess import Preprocess
from app.models.IntentModel import IntentModel
import tensorflow as tf
import numpy as np
from keras.models import Model, load_model
from keras import preprocessing
from keras_preprocessing.sequence import pad_sequences


class UserIntentModel(object):
    def __init__(self, model_name, proprocess):
        ## 의도 클래스별 레이블
        self.labels = {0: "인사", 1: "욕설", 2: "주문", 3: "예약", 4: "기타"}
        ## 의도 분류 모델 불러오기
        self.model = load_model(model_name)
        ## 챗봇 Proprocess 객체
        self.p = proprocess

        # 의도 클래스 예측

    def predict_class(self, query):
        ## 형태소 분석
        pos = self.p.pos(query)

        # 문장 내 키워드 추출 및 불용어 제거 후 인덱스로 전환
        keywords = self.p.get_keywords(pos, without_tag=True)
        sequences = [self.p.get_wordidx_sequence(keywords)]

        # 단어 시퀀스 벡터 크기

        # 패딩 처리
        padded_seqs = pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding='post')

        # 모델을 활용한 예측, 예측된 값 중 가장 큰 값의 인덱스 반환
        predict = self.model.predict(padded_seqs)
        predict_class = tf.math.argmax(predict, axis=1)

        return predict_class.numpy()[0]


def intent_test(query):
    try:
        p = Preprocess(
            word2index_dic="app/services/chatbot/data/chatbot_dict.bin",
            userdic="app/services/chatbot/data/user_dic.tsv")
        intent = UserIntentModel(
            model_name="app/services/chatbot/save/intent_model.h5",
            proprocess=p)
    except:
        p = Preprocess(
            word2index_dic="C:/Users/AiA/PycharmProjects/FastAPIServer/app/services/chatbot/data/chatbot_dict.bin",
            userdic="C:/Users/AiA/PycharmProjects/FastAPIServerapp/services/chatbot/data/user_dic.tsv")
        intent = UserIntentModel(
            model_name="C:/Users/AiA/PycharmProjects/FastAPIServer/app/services/chatbot/save/intent_model.h5",
            proprocess=p)
    predict = intent.predict_class(query)
    predict_label = intent.labels[predict]

    print(query)
    print("의도 예측 클래스 : ", predict)
    print("의도 예측 레이블 : ", predict_label)
    return predict, predict_label


if __name__ == "__main__":
    intent_test('오늘 탕수육 주문 가능한가요?')
