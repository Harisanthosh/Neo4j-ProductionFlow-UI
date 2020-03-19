import h2o
import pandas as pd

model_path = 'C:/Users/H395978/AppData/Local/Programs/Thesis/stamm/ml_models/h20_regression_trees'
#saved_model = h2o.load_model(model_path)
#Make sure h2o.init() is executed in a separate terminal
h2o.connect()
cols = ['Sum(WAITING_TIME_SECS)','Unique concatenate(SHOP_ORDER_BO)','Mean(QTY_DONE)','Unique count(WORK_CENTER)','Unique count*(RESRCE)','Unique concatenate*(ITEM)','Last(SFC_DONE)','Mean(QTY_RELEASED)','Mean(QTY_ORDERED)','Unique count(SHOP_ORDER_BO)','Unique count*(ITEM)','Mean(QTY)']
vals = ['13886.768','ShopOrderBO:0001,5238406','0.03','10','21','80000988','true','2376','2376','1','1','1']
df = pd.DataFrame([vals],columns=cols)
hf = h2o.H2OFrame(df)
#Importing to work further, for making single shot predictions it is not needed
mojo_model = h2o.import_mojo(model_path)
print(mojo_model)
predict = mojo_model.predict(hf)
print(predict)
#mojo_model.varimp_plot()
#h2o.print_mojo(model_path, format='json', tree_index=None)

#Direct model prediction
#h2o.mojo_predict_pandas(df, model_path, verbose=False, setInvNumNA=False)
#h2o.mojo_predict_pandas(df, model_path, genmodel_jar_path=None, classpath=None, java_options=None, verbose=False, setInvNumNA=False)
