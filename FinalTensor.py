#TensorFlow/ Machine Learning Portion
#Sources:
#https://stackabuse.com/one-hot-encoding-in-python-with-pandas-and-scikit-learn/
#https://financial-engineering.medium.com/tensorflow-2-0-load-pandas-dataframe-to-tensorflow-202c5d48966b

from __future__ import absolute_import, division, print_function, unicode_literals
import pandas as pd
import tensorflow as tf

#Read in CSV FILE with Pandas
csv_file1 = "D:\Documents\CS461/FINALvalidating15.csv"
csv_file2 = "D:\Documents\CS461/FINALtesting15.csv"
df = pd.read_csv(csv_file1)
df1 = pd.read_csv(csv_file2)

#Pop the Dependent End Column
learn = df.pop('Response')
test = df1.pop('Response')

#Format Independent and Dependent Variables
def input_evaluation_set():
    features = {'Gender': df(['Gender']),
                'Age':  df(['Age']),
                'Driving_License':  df(['Driving_Licence']),
                'Region_Code':  df(['Region_Code']),
                'Previously_Insured': df(['Previously_Insured']),
                'Vehicle_Age': df(['Vehicle_Age']),
                'Vehicle_Damage': df(['Vehicle_Damage']),
                'Annual_Premium': df(['Annual_Premium']),
                'Policy_Sales_Channel': df(['Policy_Sales_Channel']),
                'Vintage': df(['Vintage']),
                }
    labels = df(['Response'])
    return features, labels

#Assign variables to dataset
dataset = tf.data.Dataset.from_tensor_slices((df.values, learn.values))
train_dataset = dataset.shuffle(len(df)).batch(250)

#Create layers in Model and Compile Parameters
def get_compiled_model():
  model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
  ])
  model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
  return model

model = get_compiled_model()
model.fit(train_dataset, epochs=5)

#Compare Model from First part to TensorFlow Estimator Function
def input_fn(features, labels, training=True, batch_size=250):
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))
    if training:
        dataset = dataset.shuffle(1000).repeat()
    return dataset.batch(batch_size)

my_feature_columns = []
for key in df.keys():
    my_feature_columns.append(tf.feature_column.numeric_column(key=key))

classifier = tf.estimator.DNNClassifier(feature_columns=my_feature_columns,hidden_units=[300, 100],n_classes=3)
classifier.train(input_fn=lambda: input_fn(df, learn, training=True),steps=1064)
eval_result = classifier.evaluate(input_fn=lambda: input_fn(df1, test, training=False))

print('\nTest set accuracy: {accuracy:0.3f}\n'.format(**eval_result))


