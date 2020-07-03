import subprocess
import sys


if __name__ == "__main__":
    input_file = sys.argv[0]
    output_file = sys.argv[1]
    workdir_path = "C:/Users/H395978/knime-workspace/Monty2_APR"
    print(f'Input file is located at {input_file}')
    print(f'Output file is located at {output_file}')

    #subprocess.call(["dir"], shell=True)
    subprocess.call([f"knime.exe -consoleLog -noexit -nosplash -application org.knime.product.KNIME_BATCH_APPLICATION -workflow.variable=filepath,{input_file},String -workflow.variable=outputpath,{output_file},String -workflowDir={workdir_path}"], shell=True)



