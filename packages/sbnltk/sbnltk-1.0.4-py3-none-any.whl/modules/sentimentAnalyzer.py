'''
Types of SentimentAnalyzer
1. logisticRegression
2. LinearSVC
3. Multinomial_naive_bayes
5. Random Forest
4. Bert Sentiment
5. RNN

'''

from Downloader import downloader
import pickle
import pandas as pd
import numpy as np
from transformers import *
import tensorflow as tf
import tensorflow_addons as tfa


class SentimentAnalyzer:
    __dl=downloader()
    __sentiment_models=[('LR','Logistic Regression'),('LSVC','Linear SVC'),
                      ('MNB','Multinomial naive bayes'),('RF','Random Forest'),('BERT','Bert Sentiment Analysis')
                      ]

    def all_sentiment_models(self):
        st='All Sentiment analysis models name with code\n'
        for sent in self.__sentiment_models:
            st+=sent[1]+' ::: '+sent[0]+'\n'
        return st
    def __LR(self,sentence):
        self.__dl.download('sentiment_LR','model/')
        self.__dl.download('sentiment_vector','model/')
        logreg = pickle.load(open('../model/sentiment_LR.pkl', 'rb'))
        vectorizer = pickle.load(open('../model/sentiment_vector.pkl', 'rb'))
        unknown_vectors = vectorizer.transform([sentence])
        unknown_words_df = pd.DataFrame(unknown_vectors.toarray(), columns=vectorizer.get_feature_names())
        unknown_words_df.head()
        return logreg.predict(unknown_words_df)[0],logreg.predict_proba(unknown_words_df)[:, 1][0]
    def __LSVC(self,sentence):
        self.__dl.download('sentiment_LSVC', 'model/')
        self.__dl.download('sentiment_vector', 'model/')
        svc = pickle.load(open('../model/sentiment_LSVC.pkl', 'rb'))
        vectorizer = pickle.load(open('../model/sentiment_vector.pkl', 'rb'))
        unknown_vectors = vectorizer.transform([sentence])
        unknown_words_df = pd.DataFrame(unknown_vectors.toarray(), columns=vectorizer.get_feature_names())
        unknown_words_df.head()
        return svc.predict(unknown_words_df)[0], svc.predict(unknown_words_df)[0]
    def __MNB(self,sentence):
        self.__dl.download('sentiment_MNB','model/')
        self.__dl.download('sentiment_vector','model/')
        mnb = pickle.load(open('../model/sentiment_MNB.pkl', 'rb'))
        vectorizer = pickle.load(open('../model/sentiment_vector.pkl', 'rb'))
        unknown_vectors = vectorizer.transform([sentence])
        unknown_words_df = pd.DataFrame(unknown_vectors.toarray(), columns=vectorizer.get_feature_names())
        unknown_words_df.head()
        return mnb.predict(unknown_words_df)[0],mnb.predict_proba(unknown_words_df)[:, 1][0]
    def __RF(self,sentence):
        self.__dl.download('sentiment_RF','model/')
        self.__dl.download('sentiment_vector','model/')
        rf = pickle.load(open('../model/sentiment_RF.pkl', 'rb'))
        vectorizer = pickle.load(open('../model/sentiment_vector.pkl', 'rb'))
        unknown_vectors = vectorizer.transform([sentence])
        unknown_words_df = pd.DataFrame(unknown_vectors.toarray(), columns=vectorizer.get_feature_names())
        unknown_words_df.head()
        return rf.predict(unknown_words_df)[0],rf.predict_proba(unknown_words_df)[:, 1][0]

    def __sentence_convert_data(self,data):
        tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
        SEQ_LEN = 147
        tokens, masks, segments = [], [], []
        token = tokenizer.encode(data, max_length=SEQ_LEN, truncation=True, padding='max_length')
        num_zeros = token.count(0)
        mask = [1] * (SEQ_LEN - num_zeros) + [0] * num_zeros
        segment = [0] * SEQ_LEN
        tokens.append(token)
        segments.append(segment)
        masks.append(mask)
        tokens = np.array(tokens)
        masks = np.array(masks)
        segments = np.array(segments)
        return [tokens, masks, segments]

    def __b_predict(self,bert,sentence):
        data_x = self.__sentence_convert_data(sentence)
        predict = bert.predict(data_x)
        predict_value = np.ravel(predict)
        predict_answer = np.round(predict_value, 0).item()
        if predict_answer == 0:
            return 0, (1.0 - predict_value)
        elif predict_answer == 1:
            return 1, predict_value

    def __create_sentiment_bert(self):
        SEQ_LEN = 147
        model = TFBertModel.from_pretrained('bert-base-multilingual-cased')
        token_inputs = tf.keras.layers.Input((SEQ_LEN,), dtype=tf.int32, name='input_word_ids')
        mask_inputs = tf.keras.layers.Input((SEQ_LEN,), dtype=tf.int32, name='input_masks')
        segment_inputs = tf.keras.layers.Input((SEQ_LEN,), dtype=tf.int32, name='input_segment')
        bert_outputs = model([token_inputs, mask_inputs, segment_inputs])
        bert_outputs = bert_outputs[1]
        sentiment_first = tf.keras.layers.Dense(1, activation='sigmoid',
                                                kernel_initializer=tf.keras.initializers.TruncatedNormal(stddev=0.02))(
            bert_outputs)
        sentiment_model = tf.keras.Model([token_inputs, mask_inputs, segment_inputs], sentiment_first)
        opt = tfa.optimizers.RectifiedAdam(lr=2.0e-5, weight_decay=0.0025)
        sentiment_model.compile(optimizer=opt, loss=tf.keras.losses.BinaryCrossentropy(), metrics=['acc'])
        return sentiment_model
    def __BERT(self,sentence):
        self.__dl.download('sentiment_BERT', 'model/')
        bert = self.__create_sentiment_bert()
        bert.load_weights('model/sentiment_BERT.h5')
        return self.__b_predict(bert,sentence)
    def predict(self,model_code,sentence):
        if len(sentence)==0:
            raise ValueError('Empty Sentence is detected in Sentiment analysis!!')
        if model_code=='LR':
               pred,prop=self.__LR(sentence)
               return pred
        elif model_code=='LSVC':
            pred,prop=self.__LSVC(sentence)
            return pred
        elif model_code=='MNB':
            pred,prop=self.__MNB(sentence)
            return pred
        elif model_code=='RF':
            pred,prop=self.__RF(sentence)
            return pred
        elif model_code=='BERT':
            pred,prop=self.__BERT(sentence)
            return pred
        else:
            raise ValueError('Model code Does not exist!!\n'+ self.all_sentiment_models())
    def predict_probability(self,model_code,sentence):
        if len(sentence)==0:
            raise ValueError('Empty Sentence is detected in Sentiment analysis!!')
        if model_code=='LR':
               pred,prop=self.__LR(sentence)
               return prop
        elif model_code=='LSVC':
            pred,prop=self.__LSVC(sentence)
            return prop
        elif model_code=='MNB':
            pred,prop=self.__MNB(sentence)
            return prop
        elif model_code=='RF':
            pred,prop=self.__RF(sentence)
            return prop
        elif model_code=='BERT':
            pred,prop=self.__BERT(sentence)
            return prop
        else:
            raise ValueError('Model code Does not exist!!\n'+ self.all_sentiment_models())



