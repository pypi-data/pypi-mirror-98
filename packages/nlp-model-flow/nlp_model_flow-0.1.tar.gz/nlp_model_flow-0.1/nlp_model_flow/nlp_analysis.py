from itertools import islice
import random
import statsmodels.api as sm
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFE
from sklearn.linear_model import RidgeCV, LassoCV, Ridge, Lasso
from sklearn import metrics
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import PolynomialFeatures

class text_analysis():
    
    """ Text analysis class for preperationm, common words analysis, visualization and testing 
        The main analysis that is presented is the ability to use numeric sequentially column to split the df by ranges
        (defined by user) and create analysis of text patterns according to te groups.
        
    
    Attributes:
        df (pandas df with text related columns) main df for analysis
        target_col (str) representing the numeric sequentially column to be used to split the data
        num_divisions (int, optional) amount of equel size seperated groups for the df used to activate division()
        
        initiates division and cat_by_range functions"""
    
    def __init__(self,df,target_col):
        self.df = df
        self.target_col = target_col
        self.expression = df[target_col]
        self.maxVal,self.minVal = self.expression.max(),self.expression.min()

        self.col_name = f'{target_col}_bin' 

 
        
    def _calc_division(self,num_divisions,quantile):
        
        """Function to calculate ranges and bin values.
        Args: 
        num_divisions (int): amount of equel size seperated groups for the df used to activate division()
        """
        if num_divisions: self.num_divisions = num_divisions
            
        spaces = 100/self.num_divisions
        
        if quantile:
            self.binVals = np.round(np.arange(0,100+spaces,spaces))/100 #borders of division from 100%
            self.binVals_1 = self.binVals[1:]
            self.edges = [self.df[self.target_col].quantile(i) for i in self.binVals] #use quantiles for division to get even number of values
            self.bin_names = [str(int(i*100)) for i in self.binVals_1]
            self.name = ['df_quantile_'+str(i) for i in self.bin_names] #create list of items
        else:
            self.edges = np.linspace(self.minVal-1,self.maxVal+1,num_divisions+1)
            self.binVals = np.round(np.arange(spaces,100+spaces,spaces))
            self.bin_names = [str(int(i))+'%' for i in self.binVals]
            self.name = ['df'+str(int(i)) for i in self.binVals] #create list of items
        
        
    def cat_by_range(self,col_name=None,num_divisions=3,quantile=False):

        """Function to add category columns values by range.
        Args: 
        col_name (str,optional): name of created column
        eturns: 
        float: standard deviation of the data set"""
        self.num_divisions = num_divisions
        self._calc_division(self.num_divisions,quantile) 
        
        if col_name: self.col_name = col_name


        self.df[self.col_name] = pd.cut(self.expression, bins=self.edges, labels=self.bin_names)
        self.df_divided_list = [self.df[self.df[self.col_name]==i] for i in self.bin_names]

        self.ranged_df = pd.concat(list(self.df_divided_list))

        for x,y in zip(self.name,self.df_divided_list):
            globals()[x]=y
            exec(f'self.{x}={x}')

        
        return self.ranged_df,self.df_divided_list
    

    
    def _corpus_handling(self,df,column,words_drop=None):
        try:
            #remove all None letters and lower all words
            Corpus = re.sub('[^a-zA-Z]+',' ',str(df[column].values)).lower()
            #if there are words to drop, drop them - but only if full word
            if words_drop:
                for i in words_drop:
                    Corpus = re.sub(r'\b'+i+r'\b','', Corpus).strip()
                    
            allemenities_data=nltk.word_tokenize(Corpus)
            filtered=[word for word in allemenities_data if word not in stopwords.words('english')] 
            wnl = nltk.WordNetLemmatizer() 
            allemenities_data=[wnl.lemmatize(data) for data in filtered]
            allemenities_sep_words=' '.join(allemenities_data)
            self.allemenities_sep_words = allemenities_sep_words
            return self.allemenities_sep_words
        except KeyError:
            print('wrong column name')
    
    def _word_cloud_gen(self,col,words_drop):#inheritance of class???
#         
#         self.currentCol = col
#         self.words_drop = words_drop

        self.varibals = [i.replace('df','cloud') for i in self.name] #create name for new cloud varibals
        self.clouds = [WordCloud(width = 500, height = 100,background_color=random.choice(['gray','white','black','ivory']), max_words=1000,\
                                 contour_width=3,contour_color='firebrick')\
                       .generate(self._corpus_handling(df,col,words_drop)) for df in (self.df_divided_list)]
        for x,y in zip(self.varibals,self.clouds):
            globals()[x]=y
            exec(f'self.{x}={x}')
            
        return self.clouds
    
    def _check(self,col,words_drop):
        self.words_drop=None
        if col is not None: self.currentCol=col
        if words_drop is not None:self.words_drop=words_drop
        if col is not None or words_drop is not None: self._word_cloud_gen(self.currentCol,self.words_drop)
  
            
                
    def show_wordClouds(self,col=None,words_drop=None):
        
        self._check(col,words_drop)
        Nplots = len(self.clouds)
        rows = np.ceil(Nplots/3)
        cols = 3
        
        for i,j in enumerate(self.clouds,start=1):
            plt.figure(figsize=[20,11])
            plt.axis("off")
            plt.subplot(Nplots,1,i)
            plt.title(f'{self.currentCol} columns top words: {self.varibals[i-1]} division range')
            plt.imshow(j, interpolation='bilinear',)#plt.figure(figsize=[15,10])



    def select_top_words(self,col = None,words_drop=None,n=None):
        if n is None:n=15
        self._check(col,words_drop)   
        
        #only after last
        self.top_word_dict = {}

        self.top_words_cloud  = [list(islice(cloud.words_.items(), n)) for cloud in self.clouds]
        
        for var,cloud in zip(self.varibals,self.top_words_cloud):
            self.top_word_dict[var] = cloud
            
        self.df_top_words = pd.DataFrame.from_dict(self.top_word_dict)
        return self.df_top_words
                                      
    

    def scores_calc(self,n=None,dfms=None):
        
                
        if n is not None: self.select_top_words(n=n,col=self.currentCol)
            
        col=self.currentCol        
        dfms = self.df_divided_list
        index = list(self.top_word_dict.keys())
        top_dict = self.top_word_dict
        
            
        for i in range(len(dfms)):
            dfms[i][f'{col}_text_Score'] = dfms[i].apply(lambda x:self.scores(x[col],top_dict[index[i]]),axis=1)

        self.finalDF= pd.concat(dfms)
        
        
        return self.finalDF
    
    def scores(self,col,cloud,score = 10):
            corpus = re.sub('[^a-zA-Z]+',' ',col).lower()
            for i in range(len(cloud)):
                if cloud[i][0] in corpus:
                    score+=cloud[i][1]*10**2
            return np.round(score)
    
    def best_k_top_words(self,k = None):
        if k is None: k=[10,15,20,25,30,40]
        col = self.currentCol
        kTop = []
        score = 0
        for i in k:
            df = self.scores_calc(n=i)#,col=self.currentCol)
            corr = abs(df[self.target_col].corr(df[f'{col}_text_Score']))
            if corr>score:
                score=corr
                kTop.append([i,df[self.target_col].corr(df[f'{col}_text_Score'])])
            else:               
                print(f'best k is {kTop[-1]} with score of {score}')
                break
       
                
                    

        self.finalDF = self.scores_calc(kTop[-1][0])                            
        print (kTop)
        return self.finalDF
                         
            
    def corr_mat(self):
        corr_matrix = self.finalDF.corr().abs()
        print(corr_matrix[self.target_col].sort_values(ascending=False).head(20))
        

    def __repr__(self):
        
        print('here are the steps needed for analysis:\n_______________________________________\n')
        print('1: instantiate the instance')
        print('2: activate cat_by_range(choose num divisions)')
        print('3: if you want to see the word cloud - run show_wordClouds()')
        print('4: if you want to see the list as df - run select_top_words()')
        print('  *keep in mind - after running the command - you should remove words that arant relavant')
        print('  **you only have to add varibals to one of 3 or 4 mathods. unless you want to change them (the one gets them from the other')
        print('5: for selecting the top k number of words for best correlation value, use best_k_top_words')
        return 'good luck'
