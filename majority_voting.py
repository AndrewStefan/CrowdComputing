# calculate the majority voting of anotators for each open question answer and Fleiss' kappa

import pandas as pd
from nltk import agreement
pd.set_option('display.max_rows', 500)

def output_score_lst(file_name):
  score_lst = []
  f = open(file_name, "r")
  for x in f:
    no_end_whitespace = x.rstrip()
    last_char = no_end_whitespace[-1]
    if (last_char.isdigit()):
      score_lst.append((no_end_whitespace[:-1],int(last_char)))
  return score_lst

score_lst_Andrei = output_score_lst("annotations_Andrei.csv")
score_lst_Connor = output_score_lst("annotations_Connor.csv")
score_lst_Thanos = output_score_lst("annotations_Thanos.csv")

score_lst_Andrei.append(('Anything (that we cannot perceive) that can do simple or advanced tasks artificially.\t2\n',2))
score_lst_Thanos.append(('Anything (that we cannot perceive) that can do simple or advanced tasks artificially.\t2\n',1))

score_df = pd.DataFrame(
    {'Question': [x[0] for x in score_lst_Andrei],
      'Andrei': [x[1] for x in score_lst_Andrei],
     'Connor': [x[1] for x in score_lst_Connor],
     'Thanos': [x[1] for x in score_lst_Thanos]
    })

# output majority voting csv
score_df.mode(axis=1)[0]
score_df['Majority Voting'] = score_df.mode(axis=1)[0]
score_df.to_csv('majority_voting.csv', index=False)

# calculate Fleiss' kappa
final_majority_voting = pd.read_csv("final_majority_voting.csv")

andrei_annotation = final_majority_voting.Andrei.values.tolist()
connor_annotation = final_majority_voting.Connor.values.tolist()
thanos_annotation = final_majority_voting.Thanos.values.tolist()

rater1 = andrei_annotation
rater2 = connor_annotation
rater3 = thanos_annotation

taskdata=[[0,str(i),str(rater1[i])] for i in range(0,len(rater1))]+[[1,str(i),str(rater2[i])] for i in range(0,len(rater2))]+[[2,str(i),str(rater3[i])] for i in range(0,len(rater3))]
ratingtask = agreement.AnnotationTask(data=taskdata)
print("fleiss " + str(ratingtask.multi_kappa()))