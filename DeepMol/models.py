
from rdkit import RDLogger
import logging
import warnings
from deepmol.loaders import SDFLoader
from sklearn.metrics import roc_auc_score, accuracy_score
from deepmol.metrics import Metric

warnings.filterwarnings("ignore")
logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)
RDLogger.DisableLog('rdApp.*')
from deepmol.splitters import RandomSplitter

dataset = SDFLoader("./data/CHEMBL217_conformers.sdf", id_field="_ID", labels_fields=["_Class"]).create_dataset()
random_splitter = RandomSplitter()
train_dataset, test_dataset = random_splitter.train_test_split(dataset, frac_train=0.8)
train_dataset.get_shape()
from deepmol.compound_featurization import MorganFingerprint

MorganFingerprint(n_jobs=10).featurize(train_dataset, inplace=True)
MorganFingerprint(n_jobs=10).featurize(test_dataset, inplace=True)
from deepmol.models import SklearnModel
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier()
model = SklearnModel(model=rf)
model.fit(train_dataset)
model.predict(test_dataset)
model.evaluate(test_dataset, metrics=[Metric(metric=roc_auc_score), Metric(metric=accuracy_score)])
model.save("my_model")
model = SklearnModel.load("my_model")
model.evaluate(test_dataset, metrics=[Metric(metric=roc_auc_score), Metric(metric=accuracy_score)])
MorganFingerprint(n_jobs=10).featurize(train_dataset, inplace=True)
MorganFingerprint(n_jobs=10).featurize(test_dataset, inplace=True)
from keras.layers import Dense, Dropout
from keras import Sequential

def create_model(input_dim, optimizer='adam', dropout=0.5):
    # create model
    model = Sequential()
    model.add(Dense(12, input_dim=input_dim, activation='relu'))
    model.add(Dropout(dropout))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    # Compile model
    model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    return model

from deepmol.models import KerasModel

input_dim = train_dataset.X.shape[1]
model = KerasModel(create_model, epochs = 5, verbose=1, optimizer='adam', input_dim=input_dim)
model = model.fit(train_dataset)
model.predict(test_dataset)
model.evaluate(test_dataset, metrics=[Metric(metric=roc_auc_score), Metric(metric=accuracy_score)])
model.save("my_model")
model = KerasModel.load("my_model")
model.evaluate(test_dataset, metrics=[Metric(metric=roc_auc_score), Metric(metric=accuracy_score)])
from deepmol.compound_featurization import ConvMolFeat

ConvMolFeat(n_jobs=10).featurize(train_dataset, inplace=True)
ConvMolFeat(n_jobs=10).featurize(test_dataset, inplace=True)
from deepchem.models import GraphConvModel
from deepmol.models import DeepChemModel

model = DeepChemModel(model=GraphConvModel(graph_conv_layers=[32, 32], dense_layer_size=128, n_tasks=1), epochs=5, verbose=1)
model.fit(train_dataset)
model.predict(test_dataset)
model.evaluate(test_dataset, metrics=[Metric(metric=roc_auc_score), Metric(metric=accuracy_score)])
model.save("my_model")
model = DeepChemModel.load("my_model")
model.evaluate(test_dataset, metrics=[Metric(metric=roc_auc_score), Metric(metric=accuracy_score)])
