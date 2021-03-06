import h2o
import pandas as pd
from datetime import datetime, timedelta
import tkinter as tk



model_path = 'C:/Users/H395978/AppData/Local/Programs/Thesis/stamm/ml_models/h20_regression_trees'
#saved_model = h2o.load_model(model_path)
#Make sure h2o.init() is executed in a separate terminal
h2o.connect()
cols = ['Sum(WAITING_TIME_SECS)','Unique concatenate(SHOP_ORDER_BO)','Mean(QTY_DONE)','Unique count(OPERATION)','Unique count(WORK_CENTER)','Unique count*(RESRCE)','Unique concatenate*(ITEM)','Last(SFC_DONE)','Mean(QTY_RELEASED)','Mean(QTY_ORDERED)','Unique count(SHOP_ORDER_BO)','Unique count*(ITEM)','Mean(QTY)']
vals = ['13886.768','ShopOrderBO:0001,5238406','0.03','27','10','21','80000988','true','2376','2376','1','1','1']
df = pd.DataFrame([vals],columns=cols)
hf = h2o.H2OFrame(df)
#num1 = int(input('Enter the number of SFCs to release:'))
global num1
def show_entry_fields():
    global num1
    num1 = e2.get()
    print(f"Number of SFC's are {num1}")
    #Importing to work further, for making single shot predictions it is not needed
    mojo_model = h2o.import_mojo(model_path)
    #print(mojo_model)
    predict = mojo_model.predict(hf)
    orig_time = f"{datetime.now():%d-%m-%Y %H:%M:%S}"
    print(predict)
    predicted_val = datetime.now() + timedelta(seconds=int(predict))
    predicted_time = f"{predicted_val:%d-%m-%Y %H:%M:%S}"
    print(f'The Start time for the SFC is {orig_time}')
    print(f'The estimated time of completion for the first SFC is {predicted_time}')
    full_time = predict * int(num1)
    full_val = datetime.now() + timedelta(seconds=int(full_time))
    shoporder_time = f"{full_val:%d-%m-%Y %H:%M:%S}"
    print(f'The estimated time of completion for the last SFC for the Shop Order is {shoporder_time}')

def estimate_shoporder(qty):
    print(f"Number of SFC's are {qty}")
    #Importing to work further, for making single shot predictions it is not needed
    mojo_model = h2o.import_mojo(model_path)
    #print(mojo_model)
    predict = mojo_model.predict(hf)
    orig_time = f"{datetime.now():%d-%m-%Y %H:%M:%S}"
    print(predict)
    predicted_val = datetime.now() + timedelta(seconds=int(predict))
    predicted_time = f"{predicted_val:%d-%m-%Y %H:%M:%S}"
    print(f'The Start time for the SFC is {orig_time}')
    print(f'The estimated time of completion for the first SFC is {predicted_time}')
    full_time = predict * int(qty)
    full_val = datetime.now() + timedelta(seconds=int(full_time))
    shoporder_time = f"{full_val:%d-%m-%Y %H:%M:%S}"
    print(f'The estimated time of completion for the last SFC for the Shop Order is {shoporder_time}')
    return shoporder_time



if __name__ == "__main__":
    master = tk.Tk()
    # tk.Label(master,
    #          text="First Name").grid(row=0)
    tk.Label(master,
             text="Number of SFC's to Release").grid(row=1)

    e2 = tk.Entry(master)

    e2.grid(row=1, column=1)
    tk.Button(master,
              text='Show', command=show_entry_fields).grid(row=3,
                                                           column=1,
                                                           sticky=tk.W,
                                                           pady=4)
    tk.mainloop()
#mojo_model.varimp_plot()
#h2o.print_mojo(model_path, format='json', tree_index=None)

#Direct model prediction
#h2o.mojo_predict_pandas(df, model_path, verbose=False, setInvNumNA=False)
#h2o.mojo_predict_pandas(df, model_path, genmodel_jar_path=None, classpath=None, java_options=None, verbose=False, setInvNumNA=False)
