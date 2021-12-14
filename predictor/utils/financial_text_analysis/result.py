from . import SQL
from snownlp import SnowNLP
import pandas as pd
import math
import traceback
pd.set_option('display.max_columns',None)


def quantilizeSentiments(data,date):
    pos=neg=0
    # print(len(data[date]))
    for comment in data[date]:
        try:#受到snownlp中算法限制，这里可能会因为出现了snownlp中没有的词而报错，所以添加了try-except语句
            nlp = SnowNLP(comment['comment'])
            sentimentScore = nlp.sentiments
        except:
            print(traceback.format_exc())
            continue
        if(sentimentScore>0.6):
            fans=SQL.selectFansByUserId(comment['user_id'])
            pos+=1+math.log(comment['like_count']+fans[0][0]+1,2)
        if(sentimentScore<0.4):
            fans=SQL.selectFansByUserId(comment['user_id'])
            neg+=1+math.log(comment['like_count']+fans[0][0]+1,2)
    # print("负："+str(neg)+"  正："+str(pos))
    return (pos/(pos+neg+0.0001)-0.5)*math.log(len(data[date])+1,2)

# def max_min_normalization(x,max,min):#将数据标准化
#     return (x-min)/(max-min+1)

def data(share_code):#计算情绪指数
    # if share_code[0] == '6':
    #     share_code = 'sh' + share_code
    # else:
    #     share_code = 'sz' + share_code
    a = SQL.selectCommentOrderByDate(share_code,0)
    #把评论数据变成以date为key，所有在date日发表的关于share_code股票评论为value的值的dict
    preDate = a[0][4]
    commentList = []
    comments = {}
    for i in a:
        if not i[4] == preDate:
            comments[preDate] = commentList
            commentList = [{"comment": i[2], "like_count": i[3], "user_id": i[5]}]
            preDate = i[4]
        else:
            commentList.append({"comment": i[2], "like_count": i[3], "user_id": i[5]})
    comments[preDate] = commentList
    dateList=list(comments.keys())
    for i in range(len(dateList)):
        score = quantilizeSentiments(comments, dateList[i])#第i日的评论情绪得分
    sentimentindex=score
    # print(sentimentindex)
    return sentimentindex #返回情绪指数



if __name__ == '__main__':
    result=data('zssh000001') #传入股票代码参数
    print(result) #打印情绪指数结果
