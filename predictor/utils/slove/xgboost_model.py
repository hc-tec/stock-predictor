import xgboost as xgb


def get_xgb_model():
    return {"booster": ["gbtree"],
            "eta": [.1, .3, .6, .9],
            "gamma": [0, 1, 10],
            "n_estimators": [50],
            "max_depth": [6],
            "grow_policy": ['depthwise'],
            'reg_alpha': [1e-5, 1e-2, 0.1, 1, 100],
            }, xgb.XGBClassifier(use_label_encoder=False)
