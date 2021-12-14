
from .response import Success, Error

REGISTER_SUC = Success(1000, 'Register Success')
REGISTER_ERR = Error(2000, 'Register Error')

LOGIN_SUC = Success(1001, 'Login Success')
LOGIN_ERR = Error(2001, 'Login Error')

UPLOAD_SUC = Success(1002, 'Upload Success')
UPLOAD_ERR = Error(2002, 'Upload Error')

STOCK_SELECTED_SUC = Success(1003, 'Stock Selected Update Success')
STOCK_SELECTED_ERR = Error(2003, 'Stock Selected Update Error')

STOCK_SELECT_SUC = Success(1004, 'Stock Predict Info Get Success')
STOCK_SELECT_ERR = Error(2004, 'Stock Predict Info Get Error')

STOCK_INFO_SUC = Success(1005, 'Stock Info Get Success')
STOCK_INFO_ERR = Error(2005, 'Stock Info Get Error')

STOCK_SCORE_SUC = Success(1006, 'Stock Score Get Success')
STOCK_SCORE_ERR = Error(2006, 'Stock Score Get Error')

USERINFO_MODIFY_SUC = Success(1007, 'UserInfo Modify Success')
USERINFO_MODIFY_ERR = Error(2007, 'UserInfo Modify Error')

EMOTION_ANALYSIS_SUC = Success(1008, 'Emotion Analysis Get Success')
EMOTION_ANALYSIS_ERR = Error(2008, 'Emotion Analysis Get Error')
