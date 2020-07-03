@echo off

echo KNIME Workflow automater

cd C:\Users\H395978\AppData\Local\Programs\Thesis\Knime\knime_4.1.1

pause

set /p id=Enter the preprocessed SAP ME Input Log file path: 
echo %id%

knime.exe -consoleLog -noexit -nosplash -application org.knime.product.KNIME_BATCH_APPLICATION -workflow.variable=model_input_path,%id%,String -workflowDir="C:\Users\H395978\knime-workspace\Monty2_APR_Forecaster"

::knime.exe -consoleLog -noexit -nosplash -application org.knime.product.KNIME_BATCH_APPLICATION -workflow.variable=filepath,%id%,String -workflow.variable=outputpath,%output%,String -workflowDir="C:\Users\H395978\knime-workspace\Monty2_APR"


