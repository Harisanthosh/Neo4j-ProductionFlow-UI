@echo off

echo KNIME Workflow automater

cd C:\Users\H395978\AppData\Local\Programs\Thesis\Knime\knime_4.1.1

pause

set /p id=Enter SAP ME Input Log file path: 
echo %id%

set /p output=Enter Output Log file location: 
echo %output%

knime.exe -consoleLog -noexit -nosave -nosplash -application org.knime.product.KNIME_BATCH_APPLICATION -workflow.variable=filepath,%id%,String -workflow.variable=outputpath,%output%,String -workflowDir="C:\Users\H395978\knime-workspace\Monty2_APR"


::knime.exe -consoleLog -noexit -nosplash -application org.knime.product.KNIME_BATCH_APPLICATION -workflow.variable=filepath,"C:/Users/H395978/AppData/Local/Programs/Thesis/stamm/JanMonty2TrainDataset.csv",String -workflow.variable=outputpath,"C:/Users/H395978/Documents/outputlog.csv",String -workflowDir="C:\Users\H395978\knime-workspace\Monty2_APR"
