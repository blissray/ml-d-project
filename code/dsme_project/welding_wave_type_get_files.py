import pandas as pd
import os
import numpy as np
from sklearn import preprocessing

DATA_DIR = "data/welding_wave"
filenames = os.listdir(DATA_DIR)
df_list = []
type_list = []
for filename in filenames:
    hz = filename.split("_")[0]
    gap_id = filename.split("_")[1]
    gap_type = gap_id[:4]

    type_list.append([hz, gap_type])
    df_list.append(
        pd.read_csv(os.path.join(DATA_DIR, filename), delimiter="\t", header=None,
                   names =["time_order", "ampere", "volt"] ))

modifed_df_list = []
for df, (hz, gap_type)in zip(df_list, type_list):
    df["hz"] = hz
    df["gap_type"] = gap_type
    df["gap_type"] = gap_type

    modifed_df_list.append(df)

all_df = pd.concat(modifed_df_list).reset_index(drop=True)
X_df = all_df.copy()

shift_big_list = []
rolling_big_list = []
window_size = 11

for hz in ["2000Hz", "4000Hz"]:
    for gap_type in ["Gap0", "Gap2", "Gap4"]:
        target_df = X_df[(X_df["hz"] == hz) & (X_df["gap_type"] == gap_type)][['ampere', 'volt']]
        shift_small_list = []
        rolling_small_list = []
        for i in range(1, window_size):
            names = target_df.columns
            df = target_df.shift(i)
            df.columns = [name + "_shift_" + str(i) for name in names]
            shift_small_list.append(df)

            af = target_df.rolling(i).mean()
            af.columns = [name + "_rolling_" + str(i) for name in names]
            rolling_small_list.append(af)

        shift_big_list.append(pd.concat(shift_small_list, axis=1))
        rolling_big_list.append(pd.concat(rolling_small_list, axis=1))


X_df = pd.merge(X_df, pd.concat(shift_big_list).dropna(), how="inner" , left_index=True, right_index=True)
X_df = pd.merge(X_df, pd.concat(rolling_big_list).dropna(), how="inner" , left_index=True, right_index=True)


X_df["hz"] = X_df.hz.replace({"2000Hz" : 0, "4000Hz" : 1})

le = preprocessing.LabelEncoder()
le.fit(X_df.gap_type.unique())
y = le.transform(X_df.pop("gap_type").values)
X = X_df.values

x_filename = "welding_wave_X.pickle"
X_df.to_pickle(x_filename)
print("{0} is created".format(x_filename))

y_filename = "welding_wave_y.npy"
np.save(y_filename, y)
print("{0} is created".format(y_filename))
