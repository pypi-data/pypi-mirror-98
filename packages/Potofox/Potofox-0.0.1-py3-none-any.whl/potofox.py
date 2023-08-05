import pandas as pd
from potosnail import *

class datasets:
    
    def load_wikipedia(self):
        df = pd.read_csv('https://raw.githubusercontent.com/spe301/AI-generated-AI/main/Data/Wikipedia.csv')
        X, y, vocab = Wrappers().TCP(df['Text'], df['AI'])
        dataset = {'data': X, 'target': y, 'classes': ['Human', 'AI'], 'vocab': vocab}
        return dataset
    
    def load_twitter(self):
        df = pd.read_csv('https://raw.githubusercontent.com/spe301/AI-generated-AI/main/Data/Twitter.csv')
        X, y, vocab = Wrappers().TCP(df['tweet'], df['is_there_an_emotion_directed_at_a_brand_or_product'])
        dataset = {'data': X, 'target': y, 'classes': ['negative', 'neutral', 'positive'], 'vocab': vocab}
        return dataset
    
    def load_nlp(self, version):
        df = pd.read_csv('https://raw.githubusercontent.com/spe301/AI-generated-AI/main/Data/NLP{}.csv'.format(version))
        try:
            df = df.drop(['Unnamed: 0'], axis='columns')
        except:
            pass
        return df

class DataBuilder:

    def ResultsDL(self, X, y, params, task, ts=150, epochs=50, batch_size=32, patience=5, regression=False):
        '''facilitates the Data Collection Process'''
        if task == 'NLP':
            if regression==False:
                X2, y2, _ = Wrappers().TCP(X, y)
            else:
                X2, y2, _ = Wrappers().TRP(X, y)
            func = DeepLearning().RNN 
        if task == 'CV':
            X2, _, y2, _ = DeepLearning().ModelReadyPixles(X, y, target_size=(ts, ts))
            func = DeepLearning().CNN
        if task == 'TC':
            X2 = np.array(X)
            y2 = DeepLearning().MulticlassOutput(np.array(y))
            func = DeepLearning().DeepTabularClassification
        if task == 'TR':
            X2 = np.array(X)
        y2 = np.array(y)
        func = DeepLearning().DeepTabularRegression
        try:
            df = DeepLearning().CollectPerformance(params, func, X2, y2, epochs=epochs, batch_size=batch_size, patience=patience, regression=regression)
        except:
            df = DeepLearning().CollectPerformance(params, func, X2, y2.reshape(-1), epochs=epochs, batch_size=batch_size, patience=patience, regression=regression)
        size = []
        n_features = []
        batch = []
        depth = []
        dominances = []
        for i in range(len(df)):
            size.append(X2.shape[0])
            n_features.append(X2.shape[1])
            dominances.append(max(pd.DataFrame(y2).value_counts())/len(y2))
            if task == 'CV':
                depth.append(X2.shape[3])
            df['len_dataset'] = size
            df['n_features'] = n_features
            if regression == False:
                df['dominant_class'] = dominances
            if task == 'CV':
                df['thickness'] = depth
        return df

    def ResultsNLP(self, df, gridding=False):
      dh = DataHelper()
      '''gets the nlp results dataset ready for modeling'''
      df['regularizer'] = df['regularizer'].fillna('None')
      df['stacking'] = df['stacking'].astype(int)
      df['dropout'] = df['dropout'].astype(int)
      df['bidirectional'] = df['bidirectional'].astype(int)
      act = dh.OHE(df['activation'])
      reg = dh.OHE(df['regularizer'])
      opt = dh.OHE(df['optimizer'])
      method = dh.OHE(df['method'])
      df = df.drop(['activation', 'regularizer', 'optimizer', 'method'], axis='columns')
      df = pd.concat([df, act, reg, opt, method], axis='columns')
      if gridding == True:
        return df
      df['val_loss'] = df['val_loss'].fillna(max(df['val_loss']))
      df['loss'] = df['loss'].fillna(max(df['loss']))
      kpi_list = ['accuracy', 'loss', 'val_accuracy', 'val_loss']
      kpi = df[kpi_list]
      scores = []
      for i in range(len(df)):
        ts = (1 - (kpi['loss'][i] / max(kpi['loss'])) + kpi['accuracy'][i])/2
        vs = (1 - (kpi['val_loss'][i] / max(kpi['val_loss'])) + kpi['val_accuracy'][i])/2
        score = (ts+vs) - abs(ts-vs)
        scores.append(score)
      df2 = df.drop(kpi_list, axis='columns')
      df2['quality'] = scores
      return df2

    def BuildCombos(self, params, len_dataset, n_features, dominant_class):
      '''puts all possible gridsearch combinations in a dataframe'''
      n = list(params.keys())
      lst1 = []
      lst2 = []
      lst3 = []
      lst4 = []
      lst5 = []
      lst6 = []
      lst7 = []
      lst8 = []
      lst9 = []
      lst10 = []
      lst11 = []
      lst12 = []
      for i in range(len(params[n[0]])):
        var1 = params[n[0]][i]
        for i in range(len(params[n[1]])):
          var2 = params[n[1]][i]
          for i in range(len(params[n[2]])):
            var3 = params[n[2]][i]
            for i in range(len(params[n[3]])):
              var4 = params[n[3]][i]
              for i in range(len(params[n[4]])):
                var5 = params[n[4]][i]
                for i in range(len(params[n[5]])):
                  var6 = params[n[5]][i]
                  for i in range(len(params[n[6]])):
                    var7 = params[n[6]][i]
                    for i in range(len(params[n[7]])):
                      var8 = params[n[7]][i]
                      for i in range(len(params[n[8]])):
                        var9 = params[n[8]][i]
                        for i in range(len(params[n[9]])):
                          var10 = params[n[9]][i]
                          for i in range(len(params[n[10]])):
                            var11 = params[n[10]][i]
                            for i in range(len(params[n[11]])):
                              var12 = params[n[11]][i]
                              lst1.append(var1)
                              lst2.append(var2)
                              lst3.append(var3)
                              lst4.append(var4)
                              lst5.append(var5)
                              lst6.append(var6)
                              lst7.append(var7)
                              lst8.append(var8)
                              lst9.append(var9)
                              lst10.append(var10)
                              lst11.append(var11)
                              lst12.append(var12)
      df = pd.DataFrame(lst1)
      df.columns = [n[0]]
      df[n[1]] = lst2
      df[n[2]] = lst3
      df[n[3]] = lst4
      df[n[4]] = lst5
      df[n[5]] = lst6
      df[n[6]] = lst7
      df[n[7]] = lst8
      df[n[8]] = lst9
      df[n[9]] = lst10
      df[n[10]] = lst11
      df[n[11]] = lst12
      df['len_dataset'] = [len_dataset] * len(df)
      df['n_features'] = [n_features] * len(df)
      df['dominant_class'] = [dominant_class] * len(df)
      return df



class Models:

     def ModelBuilder(self, df, task):
        wr = Wrappers()
        dh = DataHelper()
        ml = MachineLearning()
        if task == 'NLP':
          df2 = SuperBear(df)
        vanilla, grid, X, Xval, y, yval = wr.Vanilla(df2, 'quality', 'regression')
        Xs = dh.ScaleData('standard', X)
        model = ml.Optimize(vanilla, grid, Xs, y)
        return model