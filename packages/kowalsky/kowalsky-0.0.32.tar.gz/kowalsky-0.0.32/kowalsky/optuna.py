import optuna
from lightgbm import LGBMRegressor
from lightgbm import LGBMClassifier
from xgboost import XGBRegressor
from xgboost import XGBClassifier
from optuna.samplers import TPESampler
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import ExtraTreeRegressor
from sklearn.tree import ExtraTreeClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import AdaBoostRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor
from mlens.ensemble import SuperLearner
from sklearn.svm import SVR
from sklearn.svm import SVC
from catboost import CatBoostClassifier
from catboost import CatBoostRegressor
from .metrics import get_score_fn
from kowalsky.logs.utils import LivePyPlot
import math
from .df import read_dataset


def rf_params(trial):
    return {
        'min_samples_leaf': trial.suggest_int("min_samples_leaf", 1, 15),
        'min_samples_split': trial.suggest_uniform("min_samples_split", 0.05, 1.0),
        'n_estimators': trial.suggest_int("n_estimators", 2, 800),
        'max_depth': trial.suggest_int("max_depth", 2, 25),
        'random_state': 666
    }


def xgboost_params(trial):
    return {
        'learning_rate': trial.suggest_uniform("learning_rate", 0.0000001, 2),
        'n_estimators': trial.suggest_int("n_estimators", 2, 800),
        'max_depth': trial.suggest_int("max_depth", 2, 25),
        'gamma': trial.suggest_uniform('gamma', 0.0000001, 1),
        'random_state': 666
    }


def lgb_params(trial):
    return {
        'learning_rate': trial.suggest_uniform('learning_rate', 0.0000001, 1),
        'n_estimators': trial.suggest_int("n_estimators", 1, 800),
        'max_depth': trial.suggest_int("max_depth", 2, 25),
        'num_leaves': trial.suggest_int("num_leaves", 2, 3000),
        'min_child_samples': trial.suggest_int('min_child_samples', 3, 200),
        'random_state': 666
    }


def dt_params(trial):
    return {
        'max_depth': trial.suggest_int("max_depth", 2, 25),
        'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
        'min_weight_fraction_leaf': trial.suggest_uniform('min_weight_fraction_leaf', 0.0, 0.5),
        'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 15),
        'random_state': 666
    }


def et_params(trial):
    return {
        'min_samples_leaf': trial.suggest_int("min_samples_leaf", 1, 15),
        'min_samples_split': trial.suggest_uniform("min_samples_split", 0.05, 1.0),
        'max_depth': trial.suggest_int("max_depth", 2, 25),
        'random_state': 666
    }


def bagg_params(trial):
    return {
        'n_estimators': trial.suggest_int('n_estimators', 2, 300),
        'max_samples': trial.suggest_int('max_samples', 1, 400),
        'random_state': 666
    }


def kn_params(trial):
    return {
        'n_neighbors': trial.suggest_int("n_neighbors", 2, 100)
    }


def ada_params(trial):
    return {
        'n_estimators': trial.suggest_int("n_estimators", 2, 800),
        'learning_rate': trial.suggest_uniform('learning_rate', 0.0001, 1.0)
    }


def svm_params(trial):
    return {
        'kernel': trial.suggest_categorical('kernel', ['linear', 'poly']),
        'tol': trial.suggest_uniform('tol', 1e-5, 1),
        'C': trial.suggest_loguniform('C', 1e-10, 1e10)
    }


def cb_params(trial):
    return {
        'learning_rate': trial.suggest_uniform('learning_rate', 0.0001, 1.0),
        'depth': trial.suggest_int("max_depth", 2, 16)
    }


models = {

    # Gradient Boosts
    'XGBR': (XGBRegressor, xgboost_params),
    'XGBC': (XGBClassifier, xgboost_params),
    'LGBR': (LGBMRegressor, lgb_params),
    'LGBC': (LGBMClassifier, lgb_params),

    # Trees
    'RFR': (RandomForestRegressor, rf_params),
    'RFC': (RandomForestClassifier, rf_params),
    'DTR': (DecisionTreeRegressor, dt_params),
    'DTC': (DecisionTreeClassifier, dt_params),
    'ETR': (ExtraTreeRegressor, et_params),
    'ETC': (ExtraTreeClassifier, et_params),

    # Ensemble
    'BC': (BaggingClassifier, bagg_params),
    'BR': (BaggingRegressor, bagg_params),
    'ADAR': (AdaBoostRegressor, ada_params),
    'ADAC': (AdaBoostClassifier, ada_params),
    'CBR': (CatBoostRegressor, cb_params),
    'CBC': (CatBoostClassifier, cb_params),

    # KNeighbors
    'KNC': (KNeighborsClassifier, kn_params),
    'KNR': (KNeighborsRegressor, kn_params),

    # SVM
    'SVR': (SVR, svm_params),
    'SVC': (SVC, svm_params),
}


def get_model(model_name, trial, custom_params_fn):
    model, params_fn = models[model_name]
    params = params_fn(trial)
    custom_params = custom_params_fn(trial)
    return model(custom_params.update(params))

class EarlyStoppingError(Exception):
    pass


class EarlyStopping:

    def __init__(self, direction, patience=100, threshold=1e-3):
        self.best = -math.inf if direction == 'maximize' else math.inf
        self.fn = max if direction == 'maximize' else min
        self.count = 0
        self.threshold = threshold
        self.patience = patience

    def __call__(self, value):
        new_value = self.fn(self.best, value)
        if abs(new_value - self.best) < self.threshold:
            self.count += 1
            if self.count > self.patience:
                raise EarlyStoppingError()
        else:
            self.count = 0
            self.best = new_value


def optimize(model_name, scorer, y_column, trials=30, sampler=TPESampler(seed=666),
             direction='maximize', patience=100, threshold=1e-3, feature_selection_support=None,
             feature_selection_cols=None, ds=None, path=None, sample_size=None, stratify=False,
             custom_params_fn=None):

    if sample_size is not None:
        ds, _ = train_test_split(ds, train_size=sample_size, stratify=ds[y_column] if stratify else None)

    X_ds, y_ds = read_dataset(ds, path, y_column, feature_selection_support, feature_selection_cols)
    X_train, X_val, y_train, y_val = train_test_split(X_ds, y_ds)

    live = LivePyPlot(direction)
    stopping = EarlyStopping(direction, patience, threshold)

    def objective(trial):
        model = get_model(model_name, trial, custom_params_fn)
        model.fit(X_train, y_train)
        preds = model.predict(X_val)
        error = get_score_fn(scorer)(y_val, preds)
        live(error)
        stopping(error)
        return error

    study = optuna.create_study(direction=direction, sampler=sampler)

    try:
        study.optimize(objective, n_trials=trials, n_jobs=-1)
    except KeyboardInterrupt:
        print("Stopped with keyboard")
    except EarlyStoppingError:
        print("Stopped with early stopping")
    live.clear()

    return study.best_params



def create_super_learner(trial, models, head_models):
    selected_model_names = []
    n_models = trial.suggest_int('n_models', 1, min(6, len(models)))
    names = list(models.keys())
    for i in range(n_models):
        model_item = trial.suggest_categorical('model_{}'.format(i), names)
        if model_item not in selected_model_names:
            selected_model_names.append(model_item)

    folds = trial.suggest_int('folds', 2, 6)
    model = SuperLearner(folds=folds)

    selected_models = [models[item] for item in selected_model_names]
    model.add(selected_models)

    head_names = list(head_models.keys())
    head = trial.suggest_categorical('head', head_names)
    model.add_meta(head_models[head])
    print(f"Try: {selected_model_names}, {head}")
    return model


def optimize_super_learner(models, head_models, scorer, y_column, trials=30, sampler=TPESampler(seed=666),
                           direction='maximize', patience=100, threshold=1e-3, feature_selection_support=None,
                           feature_selection_cols=None, ds=None, path=None):

    X_ds, y_ds = read_dataset(ds, path, y_column, feature_selection_support, feature_selection_cols)
    X_train, X_val, y_train, y_val = train_test_split(X_ds, y_ds)
    scorer_fn = get_score_fn(scorer)

    live = LivePyPlot(direction)
    stopping = EarlyStopping(direction, patience, threshold)

    def objective(trial):
        model = create_super_learner(trial, models, head_models)
        model.fit(X_train, y_train)
        preds = model.predict(X_val)
        error = scorer_fn(y_val, preds)
        live(error)
        stopping(error)
        return error

    study = optuna.create_study(direction=direction, sampler=sampler)

    try:
        study.optimize(objective, n_trials=trials, n_jobs=-1)
    except KeyboardInterrupt:
        print("Stopped with keyboard")
    except EarlyStoppingError:
        print("Stopped with early stopping")
    live.clear()

    return study.best_params
