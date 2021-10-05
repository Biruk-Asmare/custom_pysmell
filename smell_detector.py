#make sure this library is installed
#pip install GitPython

import pandas as pd
import re
from subprocess import check_output
import os
import astChecker
import customast
from config import smells_metrics_thresholds
import io
import git


#takes the repo folder path and commit_id to checkout
def checkout_commit(path, commit_id):
        g_repo = git.Git(path)
        g_repo.init()
        g_repo.checkout(commit_id)
def walk_directory(rootdir):
  for root, _, files in os.walk(rootdir):
    for name in files:
        if (os.path.splitext(name)[1][1:] == 'py'):
            yield os.path.join(root,name)
def compute_project_metrics(path, commit_sha):
    detected_smells = []
    for curr_fname in walk_directory(path):
        try:
            astContent = customast.parse_file(curr_fname)
        except:
            continue
        myast = astChecker.MyAst()
        myast.fileName = curr_fname
        myast.visit(astContent)
        for item in myast.result:
            if item[0] == 1:
                if int(item[3])>=smells_metrics_thresholds['LongParameterList'][0]:
                    detected_smells.append([path,commit_sha,item[1],item[2],'LongParameterList'])
                    continue
            elif item[0] == 2:
                if int(item[3])>=smells_metrics_thresholds['LongMethod'][0]:
                    detected_smells.append([path,commit_sha,item[1],item[2],'LongMethod'])
                    continue
            elif item[0] == 3:
                if int(item[3])>=smells_metrics_thresholds['LongScopeChaining'][0]:
                    detected_smells.append([path,commit_sha,item[1],item[2],'LongScopeChaining'])
                    continue
            elif item[0] == 4:
                if int(item[3])>=smells_metrics_thresholds['LongBaseClassList'][0]:
                    detected_smells.append([path,commit_sha,item[1],item[2],'LongBaseClassList'])
                    continue
            elif item[0] == 5:
                if int(item[3])>=smells_metrics_thresholds['LargeClass'][0]:
                    detected_smells.append([path,commit_sha,item[1],item[2],'LargeClass'])
                    continue
            elif item[0] == 6:
                m1 = smells_metrics_thresholds['MultiplyNestedContainer'][0]
                m2 = smells_metrics_thresholds['MultiplyNestedContainer'][1]
                m3 = smells_metrics_thresholds['MultiplyNestedContainer'][2]
                if (len(item)==4 and int(item[3])>=m1) or (len(item)>4 and int(item[3])>=m2 and int(item[4])>=m3):
                    detected_smells.append([path,commit_sha,item[1],item[2],'MultiplyNestedContainer'])
                    continue
            elif item[0] == 9:
                m1 = smells_metrics_thresholds['LongLambdaFunction'][0]
                m2 = smells_metrics_thresholds['LongLambdaFunction'][1]
                m3 = smells_metrics_thresholds['LongLambdaFunction'][2]
                if int(item[3])>=m1 and (int(item[4])>=m2 or int(item[5])>=m3):
                    detected_smells.append([path,commit_sha,item[1],item[2],'LongLambdaFunction'])
                    continue
            elif item[0] == 10:
                m1 = smells_metrics_thresholds['LongTernaryConditionalExpression'][0]
                m2 = smells_metrics_thresholds['LongTernaryConditionalExpression'][1]
                if int(item[3])>=m1 or int(item[3])>=m2:
                    detected_smells.append([path,commit_sha,item[1],item[2],'LongTernaryConditionalExpression'])
                    continue
            elif item[0] == 11:
                m1 = smells_metrics_thresholds['ComplexContainerComprehension'][0]
                m2 = smells_metrics_thresholds['ComplexContainerComprehension'][1]
                m3 = smells_metrics_thresholds['ComplexContainerComprehension'][2]
                if (int(item[3])>=m1 and int(item[5])>=m3) or int(item[4])>=m2:
                    detected_smells.append([path,commit_sha,item[1],item[2],'ComplexContainerComprehension'])
                    continue
            elif item[0] == 13:
                if int(item[3])>smells_metrics_thresholds['LongMessageChain'][0]:
                    detected_smells.append([path,commit_sha,item[1],item[2],'LongMessageChain'])
                    continue
    return detected_smells



def extract_smells_from_project(project_path, project_name, commit_id):
    
    try:
        checkout_commit(project_path, commit_id)
    except:
        print('nothing to do')
    smells = compute_project_metrics(path=project_path, commit_sha=commit_id)
    df = pd.DataFrame(smells)
    df['repo_name'] = project_name
    df.columns=["repo_path","commit_id","file_name","line_no","smell","repo_name"]
   
    return df #return a dataframe of smells per project


def main():
    project_path="" #provide repo absolute path
    project_name="" #provide repo name
    commit_id="" #provide commit id to analyze
    smells= extract_smells_from_project(project_path,project_name,commit_id) 
    #TODO: iterate over all projects and commit ids and save the result to csv
    #print(smells.tail(5)) test code

main()
