# TASK 2: IMPORT LIBRARIES/DATASETS AND PERFORM EXPLORATORY DATA ANALYSIS

import pandas as pd  # Data Manipulation
import matplotlib.pyplot as plt  # Data Visualization
import seaborn as sns  # Data Visualization
import plotly.express as px  # Interactive Data Visualization
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay, roc_curve, roc_auc_score
from sklearn.calibration import CalibratedClassifierCV  # For probability score output

# Read the CSV file
telecom_df = pd.read_csv('telecom_churn.csv')

# Load the top 5 and bottom 5 instances
print(telecom_df.head())
print(telecom_df.tail())

# Check the shape of the dataframe and display the feature columns
print(telecom_df.shape)
print(telecom_df.columns)

# Obtain the summary of the dataframe
print(telecom_df.info())
print(telecom_df.describe())

# TASK 3: PERFORM DATA VISUALIZATION

telecom_df.hist(figsize=(15, 15))
# plt.show()

print(telecom_df)
print(telecom_df['class'].value_counts())

# Plot pie Chart to get the information about the percentage of Telecom Customers churning using Plotly histogram
fig = go.Figure(data=[go.Pie(labels=['Retained (0)', 'Exited (1)'], values=telecom_df['class'].value_counts())])
# fig.show()

# Plot histogram graph for the international plan service used by the Telecom customers with respect to churned/Retained
fig = px.histogram(telecom_df, x='international_plan', color='class')
# fig.show()

# Correlation Matrix
corr_matrix = telecom_df.corr()
plt.figure(figsize=(15, 15))
sns.heatmap(corr_matrix, annot=True, fmt='0.2f')
plt.title("Correlation Matrix of Telecom Customers", fontsize=20)
# plt.show()
# It is clearly shown that "voice_mail_plan" and "number_vmail_messages" are highly correlated.
# It is clearly shown that "total day charge" and "total daily minutes" are highly correlated.

# Churn by day charges
plt.figure()
ax = sns.kdeplot(telecom_df.total_day_charge[(telecom_df["class"] == 0)],
                 color="Red", fill=True)
ax = sns.kdeplot(telecom_df.total_day_charge[(telecom_df["class"] == 1)],
                 color="Blue", fill=True)
ax.legend(["Retain", "Churn"], loc="upper right")
ax.set_ylabel("Density")
ax.set_xlabel("Day Charges")
ax.set_title("Distribution of day charges by churn")
# plt.show()

# Churn by evening charges
plt.figure()
ax = sns.kdeplot(telecom_df.total_eve_charge[(telecom_df["class"] == 0)],
                 color="Red", fill=True)
ax = sns.kdeplot(telecom_df.total_eve_charge[(telecom_df["class"] == 1)],
                 color="Blue", fill=True)
ax.legend(["Retain", "Churn"], loc="upper right")
ax.set_ylabel("Density")
ax.set_xlabel("Evening Charges")
ax.set_title("Distribution of evening charges by churn")
# plt.show()

# Plot histogram graph for the voice mail plan service used by the Telecom customers with respect to churned/retained
fig = px.histogram(telecom_df, x='voice_mail_plan', color='class')
# fig.show()


# TASK 4: IDENTIFY FEATURE IMPORTANCE & PREPARE THE DATA BEFORE MODEL TRAINING

# Unnecessary features would decrease the training speed, the model interpretability and the generalization
# performance on the test data. Therefore, finding and selecting the most useful features in the dataset is crucial.
# Assigning input features to X and output (Churn) to y

# area_code and phone_number features are irrelevant to proceed further to train the model
X = telecom_df.drop(["class", "area_code", "phone_number"], axis="columns")
y = telecom_df["class"]
print(X)
print(y)
print(X.shape)
print(y.shape)

# Perform train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
print(X_train.shape)
print(X_test.shape)

rf = RandomForestClassifier()
rf.fit(X_train, y_train)

# Plot the feature importance
feat_scores = pd.DataFrame({"Fraction of variables affected": rf.feature_importances_}, index=X.columns)
feat_scores = feat_scores.sort_values(by="Fraction of variables affected")
feat_scores.plot(kind="barh", figsize=(10, 5))
sns.despine()
# plt.show()
# The above graph is generated by Random Forest algorithm The graph indicates that "total_day_minutes"
# tops the list of important features followed by "total_day_minutes" and so on.


# TASK 5: TRAIN AND EVALUATE A LOGISTIC REGRESSION CLASSIFIER¶

model_LR = LogisticRegression()
model_LR.fit(X_train, y_train)
y_predict = model_LR.predict(X_test)

# precision is the ratio of TP/(TP+FP)
# recall is the ratio of TP/(TP+FN)
# F-beta score can be interpreted as a weighted harmonic mean of the precision and recall
# where an F-beta score reaches its best value at 1 and worst score at 0.
print(classification_report(y_test, y_predict))
ConfusionMatrixDisplay(confusion_matrix(y_test, y_predict)).plot()
# plt.show()


# TASK 6: TRAIN AND EVALUATE A SUPPORT VECTOR MACHINE CLASSIFIER

model_svm = LinearSVC(max_iter=10000)
model_svm = CalibratedClassifierCV(model_svm)
model_svm.fit(X_train, y_train)
y_predict = model_svm.predict(X_test)

print(classification_report(y_test, y_predict))
ConfusionMatrixDisplay(confusion_matrix(y_test, y_predict)).plot()
# plt.show()


# TASK 7: TRAIN AND EVALUATE A RANDOM FOREST CLASSIFIER

model_rf = RandomForestClassifier()
model_rf.fit(X_train, y_train)
y_predict = model_rf.predict(X_test)

print(classification_report(y_test, y_predict))
ConfusionMatrixDisplay(confusion_matrix(y_test, y_predict)).plot()
# plt.show()


# TASK 8: TRAIN AND EVALUATE A K-NEAREST NEIGHBOUR (KNN)

model_knn = KNeighborsClassifier()
model_knn.fit(X_train, y_train)
y_predict = model_knn.predict(X_test)

print(classification_report(y_test, y_predict))
ConfusionMatrixDisplay(confusion_matrix(y_test, y_predict)).plot()
# plt.show()


# TASK 9: TRAIN AND EVALUATE A NAIVE BAYES CLASSIFIER

model_gnb = GaussianNB()
model_gnb.fit(X_train, y_train)
y_predict = model_gnb.predict(X_test)

print(classification_report(y_test, y_predict))
ConfusionMatrixDisplay(confusion_matrix(y_test, y_predict)).plot()
# plt.show()


# TASK 10: PLOT ROC CURVES FOR THE 5 MODELS AND FIND AUC SCORES¶

# ROC curve
fpr1, tpr1, thresh1 = roc_curve(y_test, model_LR.predict_proba(X_test)[:, 1])
print(fpr1)
print(tpr1)
print(thresh1)
fpr2, tpr2, thresh2 = roc_curve(y_test, model_svm.predict_proba(X_test)[:, 1])
fpr3, tpr3, thresh3 = roc_curve(y_test, model_rf.predict_proba(X_test)[:, 1])
fpr4, tpr4, thresh4 = roc_curve(y_test, model_knn.predict_proba(X_test)[:, 1])
fpr5, tpr5, thresh5 = roc_curve(y_test, model_gnb.predict_proba(X_test)[:, 1])

# AUC score
auc_score1 = roc_auc_score(y_test, model_LR.predict_proba(X_test)[:, 1])
auc_score2 = roc_auc_score(y_test, model_svm.predict_proba(X_test)[:, 1])
auc_score3 = roc_auc_score(y_test, model_rf.predict_proba(X_test)[:, 1])
auc_score4 = roc_auc_score(y_test, model_knn.predict_proba(X_test)[:, 1])
auc_score5 = roc_auc_score(y_test, model_gnb.predict_proba(X_test)[:, 1])
print("Logistic Regression: ", auc_score1)  # Logistic Regression
print("Support Vector Machine: ", auc_score2)  # Support Vector Machine
print("Random Forest: ", auc_score3)  # Random Forest
print("K-Nearest Neighbors: ", auc_score4)  # K-Nearest Neighbors
print("Naive Bayes: ", auc_score5)  # Naive Bayes

plt.figure()
plt.plot(fpr1, tpr1, linestyle="--", color="orange", label="Logistic Regression")
plt.plot(fpr2, tpr2, linestyle="--", color="red", label="SVM")
plt.plot(fpr3, tpr3, linestyle="--", color="green", label="Random Forest")
plt.plot(fpr4, tpr4, linestyle="--", color="yellow", label="KNN")
plt.plot(fpr5, tpr5, linestyle="--", color="white", label="Naive bayes")
plt.title('Receiver Operator Characteristics (ROC)')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive rate')
plt.legend(loc='best')
plt.savefig('ROC', dpi=300)
plt.show()
