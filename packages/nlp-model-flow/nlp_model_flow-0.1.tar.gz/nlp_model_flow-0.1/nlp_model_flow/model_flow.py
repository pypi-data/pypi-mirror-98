from .nlp_analysis import text_analysis 
class models(text_analysis):
    
    def __init__(self,df,target_col):
            self.df = df
            self.target_col = target_col
            self.X = self.df.drop(self.target_col, axis=1)
            self.y = self.df[self.target_col]
            
            text_analysis.__init__(self,self.df,self.target_col)
            
            
    def lreg(self,X=None,y=None):
        """Function to calculate linear regression.
        Args: 
        x (df,optional): x df
        y (df,optional): target feature 
        prints:
        RMSE and r2 for model
        for cross validation: mean score and std
        returns: 
        array: pred results column
        array: y_test column"""
        if X is not None:self.X = X
        if y is not None:self.y = y
            
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.3, random_state=42)
        lm = LinearRegression()
        lm.fit(self.X_train, self.y_train)
        self.pred = lm.predict(self.X_test)
#         self.y_test = y_test
        self.mse = metrics.mean_squared_error(self.y_test, self.pred)
        self.r_square = metrics.r2_score(self.y_test, self.pred)

        print('-------------------\n\nRoot Mean squere error is {}\n'.format("%.3f"%self.mse**(1/2)))
        print('R^2 is {}\n\n----------------------\n\n'.format("%.4f"%self.r_square))
        
        Rcross = cross_val_score(lm, self.X, self.y, cv=10)
        print(f'Cross_val score:\nMean: {"%.2f"%Rcross.mean()}\nStandard deviation: {"%.2f"% Rcross.std()}')
        return self.pred,self.y_test
            
            
    def stats(self,drop=None):
        if drop is not None:
            try:
                self.X_stats = self.X.drop(drop,axis=1)
            except KeyError:
                print('columns not in axis')
                self.X_stats = self.X
        else:
            self.X_stats=self.X
                
        X2 = sm.add_constant(self.X_stats)
        est = sm.OLS(self.y, X2)
        est2 = est.fit()
        print(est2.summary())
#         X2.drop('const',axis=1,inplace=True)
        return X2
    
    def best_features(self,p_max_Val=0.05,activate_model = False,df=None):
        removed_cols = []
        if df is not None:
            self.set_Att('finalDF',df,override=True)
        else:
            self.set_Att('finalDF',self.df)
            
        self._split()#creates X amd y varibals
         
            
        self.p_max_Val = p_max_Val
        self.X_df_fixed = sm.add_constant(self.X)
        est = sm.OLS(self.y, self.X_df_fixed)
        est2 = est.fit()

        max_p_col = est2.pvalues[est2.pvalues==est2.pvalues[est2.pvalues.index!='const'].max()].index.values[0]

        p_val = est2.pvalues[est2.pvalues==est2.pvalues[est2.pvalues.index!='const'].max()].values[0]
        
        while p_val>self.p_max_Val:
            
            
            self.X_df_fixed = self.X_df_fixed.drop(max_p_col,axis=1)
            est = sm.OLS(self.y, self.X_df_fixed)
            est2 = est.fit()
#             print(f'---\nremoved {max_p_col} at p_val of {p_val}\n')
            removed_cols.append(f'---\nremoved {max_p_col} at p_val of {p_val}\n')
            

            p_val = est2.pvalues[est2.pvalues==est2.pvalues[est2.pvalues.index!='const'].max()].values[0]

            max_p_col = est2.pvalues[est2.pvalues==est2.pvalues[est2.pvalues.index!='const'].max()].index.values[0]
            self.X_df_fixed = sm.add_constant(self.X_df_fixed)
        print(est2.summary())
        summery = est2.summary()
        
        if activate_model:
            self.pred,self.y_test = self.lreg(X=self.X_df_fixed)
            return self.pred,self.y_test,summery,removed_cols
        else:
            self.X_df_fixed.drop('const',axis=1,inplace=True)
            return self.X_df_fixed,summery
        
    def plot_results(self,plot = 'reg'):
        """Function to plot model results.
        Args: 
        plot (str,optional): default reg for scatter plot.change to 'dist' for distribution plot
        n"""
        if not hasattr(self, 'pred'):
            self.pred,self.y_test = self.lreg(X=self.X_df_fixed)
        if plot == 'reg':     
            plt.figure(figsize=(10,5))
            sns.regplot(x=self.y_test, y=self.pred, color=sns.color_palette()[0])
#             plt.xlim(0, self.X.max())
            plt.title(f'Predict Model\nRmse:{"%.2f"%self.mse**(1/2)}  r_square:{"%.2f"%self.r_square}', fontsize=14)
            plt.xlabel('Test Data', fontsize=12)
            plt.ylabel('Predictions', fontsize=12);
        elif plot=='dist':
            DistributionPlot(self.y_test, self.pred, 'Actual Values', 'Predicted Values','Predicted Distribution Value')
        
    def _split(self):
        self.finalDFint = self.finalDF.select_dtypes(exclude=['object','category'])
        self.X = self.finalDFint.drop(self.target_col, axis=1)
        self.y = self.finalDFint[self.target_col]
     
    def set_Att(self,val=None,inval=None,override = False):
        
        if hasattr(self, val) and not override :
#             print(f'attribute already set:{getattr(self, val)}')
            print(f'attribute already set')
        else:
            setattr(self, val, inval)
#             print(f'attibute set to :{getattr(self, val)}')
    
    def scale_df(self,df = None,cols=None,standard = True):
        if df is not None:
            self.finalDF_scaled=df#.drop(self.target_col,axis=1)
        else:
#             df = self.finalDF
            self.finalDF_scaled = self.finalDF#.drop(self.target_col,axis=1)
        if cols is not None: self.finalDF_scaled = self.finalDF_scaled[cols]
        
        # Get column names first
        names = self.finalDF_scaled.columns
        # Create the Scaler object
        scaler = preprocessing.StandardScaler()
        # Fit your data on the scaler object
        self.finalDF_scaled = scaler.fit_transform(self.finalDF_scaled)
        self.finalDF_scaled = pd.DataFrame(self.finalDF_scaled, columns=names)
#         self.finalDF_scaled = pd.concat([self.finalDF_scaled,df[self.target_col]],join='inner',axis=1)
        self.X_scale = self.finalDF_scaled.drop(self.target_col,axis=1)
        self.y_scale = self.finalDF_scaled[self.target_col]
        return self.finalDF_scaled
    
    def svr_model(self,grid=True,kernel_grid = 'rbf', kernel='rbf',c=[1,10,25],epsilon=[0.01, 0.05,0.1],degree=[1,2,4]):
        """Function to run svr model.
            first performs grid search, than runs SVR on best parameters.
        Args: 
        grid (bool,optional): default 'True' to run grd search for optimal values.
        change to 'False' only if want to change kernel for final model and after running first with True.
        kernel_grid (str,optional):to check parameters with different kernels {'linear', 'poly', 'rbf', 'sigmoid'}
                kernel (str,optional): default 'rbf'. for diefferent kernel asstimation change to{'linear', 'poly', 'rbf', 'sigmoid'}
        c,epsilon,degree (list,optional): list parameters for grid search
             'C': [1, 50,100,1000,2000,3000],
            'epsilon': [0.001,0.01, 0.05, 0.1, 0.5, 1],
            'degree':[3,6]
            
        Returns:
        y_test, prediction"""
        
        if grid:
            gsc = GridSearchCV(
            estimator=SVR(kernel=kernel_grid),
            param_grid={
                'C': c,
                'epsilon': epsilon,
                'degree':degree},
                 cv=5, scoring='neg_mean_squared_error', verbose=0, n_jobs=-1)
            grid_result = gsc.fit(self.X_scale, self.y_scale)
            self.best_params = grid_result.best_params_
            
        X_train, X_test, y_train, self.y_test = train_test_split(self.X_scale, self.y_scale, test_size=0.3, random_state=42)
        best_svr = SVR(kernel=kernel, C=self.best_params["C"], epsilon=self.best_params["epsilon"],degree=self.best_params["degree"],
                   coef0=0.1, shrinking=True,
                   tol=0.001, cache_size=200, verbose=False, max_iter=-1)
        best_svr.fit(X_train, y_train)
        self.pred = best_svr.predict(X_test)
        # evaluate
        self.mse = metrics.mean_squared_error(self.y_test, self.pred)
        self.r_square = metrics.r2_score(self.y_test, self.pred)
        print(self.best_params)
        print('Root Mean squere error is {}'.format("%.2f"%self.mse**(1/2)))
        print('R^2 is {}'.format("%.3f"%self.r_square))
        
        return self.y_test, self.pred
