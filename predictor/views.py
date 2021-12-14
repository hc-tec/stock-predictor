import csv
from datetime import datetime
from rest_framework.views import APIView

from . import models
from .utils.func import md5
from .utils.response import validData
from .utils.slove.solve_stock import main as solve_stock
from .utils.score import cal as stock_score
from .utils.financial_text_analysis.result import data as emotion_analysis
from .utils import (status_code, serializer, authentication)

class Register(APIView):

    """
    用户注册
    """

    authentication_classes = [authentication.UserAnthenticate]

    @validData(status_code.REGISTER_SUC, status_code.REGISTER_ERR, valid=False)
    def post(self, req):
        user_name = req.data.get('user_name')
        password = req.data.get('password')
        avatar = req.data.get('avatar')
        password = md5(password)

        assert models.User.objects.filter(user_name=user_name) \
                   .first() is None, '此用户已存在'

        User = models.User.objects.create(user_name=user_name, password=password, avatar=avatar)

        token = md5(user_name)
        models.UserToken.objects.create(user=User, token=token)

    @validData(status_code.USERINFO_MODIFY_SUC, status_code.USERINFO_MODIFY_ERR, valid=False)
    def put(self, req):
        user = req.user
        assert user is not None, 'User is not exist'
        userInfo = {}
        userInfo['user_name'] = req.data.get('user_name')
        userInfo['password'] = req.data.get('password')
        userInfo['avatar'] = req.data.get('avatar')
        if userInfo['password']:
            userInfo['password'] = md5(userInfo['password'])
        else:
            del userInfo['password']
        user.__dict__.update(**userInfo)
        user.save()

class Login(APIView):

    """
    登录
    """

    @validData(status_code.LOGIN_SUC, status_code.LOGIN_ERR, valid=True)
    def post(self, req):
        user_name = req.data.get('user_name')
        password = req.data.get('password')
        password = md5(password)
        Userlist = models.User.objects.filter(user_name=user_name)
        User = list(filter(lambda x: x.__dict__['password'] == password, Userlist))

        assert User not in (None, []), '此用户不存在'
        # python 对象 -> 通用性数据格式, eg: json
        # 序列化
        ser = serializer.UserInfoSerializer(instance=User[0], many=False)

        return ser.data

class AutoLogin(APIView):

    """
    自动登录，持久化
    """

    authentication_classes = [authentication.UserAnthenticate, ]

    @validData(status_code.LOGIN_SUC, status_code.LOGIN_ERR, valid=False)
    def post(self, req, *args, **kwargs):

        User = req.user

        assert User is not None, '无效 token'

        ser = serializer.UserInfoSerializer(instance=User, many=False)
        return ser.data

class Stock(APIView):
    """
    用户收藏\选中的股票
    """

    authentication_classes = [authentication.UserAnthenticate]

    @validData(status_code.STOCK_INFO_SUC, status_code.STOCK_INFO_ERR)
    def get(self, req):
        """
        获取用户收藏的股票
        """
        user = req.user
        stocks = models.Stock.objects.filter(user=user)
        ser = serializer.StockSerializer(instance=stocks, many=True)
        return ser.data

    @validData(status_code.STOCK_SELECTED_SUC, status_code.STOCK_SELECTED_ERR)
    def patch(self, req):
        """
        更新用户收藏的股票
        """

        stock_id = req.data.get('stock_id')

        user = req.user
        # 创建 stock
        stock = models.Stock.objects.create(stock_id=stock_id)
        # 添加用户
        stock.user.add(user)

    @validData(status_code.STOCK_SELECT_SUC, status_code.STOCK_SELECT_ERR, valid=True)
    def post(self, req):
        """
        获取股票的详细信息
        """

        user = req.user
        assert user is not None, 'Please Login First'

        stock_id = req.data.get('stock_id')

        # 通过调用训练模型 API 获取股票详细信息
        data = solve_stock(stock_id)
        data['stock_price_data'] = self.get_stock_data(data['stock_info_path'])
        del data['stock_info_path']
        return data

    def get_stock_data(self, file_path):
        stock_data = []
        with open(file_path, 'r') as file:
            contents = csv.reader(file) # type: list
            for content in contents:
                isValidData = content[0].find('2') != -1 \
                            or content[0].find('1') != -1
                if not isValidData:
                    continue
                date_raw = content[0]
                # 时间转换为时间戳
                date_ts = datetime.strptime(date_raw, '%Y-%m-%d').timestamp() * 1000
                other_data = list(map(float, content[1:6]))
                stock_data.append([date_ts, *other_data])
        return stock_data

class StockScore(APIView):
    authentication_classes = [authentication.UserAnthenticate]

    @validData(status_code.STOCK_SCORE_SUC, status_code.STOCK_SCORE_ERR)
    def get(self, req):
        # 股票打分
        stock_id = req.query_params.get('stock_id')
        roe = stock_score.cal_ROE(stock_id) # 盈利能力
        ep = stock_score.cal_EP(stock_id) # 收益增长率
        pe = stock_score.cal_PE(stock_id) # 市盈率
        al = stock_score.cal_AL(stock_id) # 财务状况
        pb = stock_score.cal_PB(stock_id) # 市净率
        ttm = stock_score.cal_PE_TTM(stock_id) # 市盈率

        return list(map(lambda x:round(x*10, 2), [roe[1], ep[1], pe[1], al[1], pb[1], ttm[1]]))

class EmotionAnalysis(APIView):
    authentication_classes = [authentication.UserAnthenticate]

    @validData(status_code.EMOTION_ANALYSIS_SUC, status_code.EMOTION_ANALYSIS_ERR)
    def get(self, req):
        stock_id = req.query_params.get('stock_id')
        # data = emotion_analysis(stock_id)
        # return round(data, 2)
        return 0.5

