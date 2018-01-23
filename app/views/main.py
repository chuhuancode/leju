from flask import Blueprint, render_template, session
from flask.json import jsonify
from flask import jsonify
from flask_admin.contrib.fileadmin import FileAdmin

from app.config import base_dir
from app.extensions import db, admin
from app.models import Topics, Personal, Design, Posts, Styles, Diary, Information, Topics_udcontent, Topics_one, \
    Udcontent, UnderDiscussion, Collects, Users


main = Blueprint('main', __name__)


# 首页模板
@main.route('/', methods=['POST','GET'])
def indexs():
    return render_template('user/index.html')


#  网站icon图标
@main.route('/favicon.ico', methods=['POST','GET'])
def favicon():
    return 'http://127.0.0.1:5000/static/upload/icon.ico'


# 首页图
@main.route('/list/', methods=['POST','GET'])
def index():
    # banner图
    tid = Topics.query.order_by(Topics.count)[:3]
    banner = []
    for i in tid:
        banner.append({"id": i.id, "imgUrl": i.top_img})

    # 优秀设计
    tlist = Topics.query.filter().all()
    wellDesign = []
    for i in tlist:
        u = Personal.query.filter_by(id=i.pid).first()
        wellDesign.append({"id": i.id, "imgurl": u.icon, "top_img": i.top_img, "top_title": i.top_title,
                           "username": u.nickname, "house_type": i.house_type,
                           "usable_area": i.usable_area})
    return jsonify({'ret': 'true', 'data': {'banner': banner, 'wellDesign': wellDesign}})


#  点进文章
@main.route('/topic/excellent/<int:kw>', methods=['POST','GET'])
def topic_excellent(kw):
    l = Topics.query.filter_by(id=kw).first()
    p = Personal.query.filter_by(id=l.pid).first()
    data = [{
        'headimg': l.top_img,
        'userimg': p.icon,
        'address': p.address,
        'username': p.nickname,
        'house_type': l.house_type,
        'usable_area': l.usable_area,
        'ratchadapisek': l.ratchadapisek,
        'decorate_cost': l.decorate_cost,
        'top_title': l.top_title,
        'top_content': l.top_content,
        'comment': l.comment,
        'floor_plan_img': l.floor_plan,
        'house_type_content': l.house_type_content
    }]
    return jsonify({'ret': 'true', 'data':data})


# 搜索
@main.route('/search/<kw>', methods=['GET','POST'])
def search(kw):
    sid = Topics.query.filter(Topics.top_title.ilike('%'+ kw +'%'))
    message = []
    for i in sid:
        u = Personal.query.filter_by(id=i.pid).first()
        message.append({"id": i.id, "imgurl": u.icon, "top_img": i.top_img, "top_title": i.top_title,
                           "username": u.nickname, "house_type": i.house_type,
                           "usable_area": i.usable_area})
    return jsonify({'ret': 'true', 'data': {'message': message}})


# 学装修
@main.route('/decorate/', methods=['GET'])
def decorate():
    list = Topics.query.order_by(db.desc(Topics.id)).all()
    decorate = []
    for i in list:
        u = Personal.query.filter_by(id=i.pid).first()
        decorate.append({"id": i.id,
                         "headImg": u.icon,
                         "imgUrl": i.top_img,
                         "desc": i.top_title,
                         "username": u.nickname,
                         "house_type": i.house_type,
                         "usable_area": i.usable_area
                         })
    return jsonify({'ret': 'true', 'data': {'decorate': decorate}})


# 找设计
@main.route('/design/', methods=['GET'])
def design():
    list = Design.query.order_by(db.desc(Design.id))
    desion = []
    for i in list:
        u = Personal.query.filter_by(id=i.pid).first()
        desion.append({
            "id": i.id,
            "imgUrl": i.logo,
            "logo": u.icon,
            "title": i.title,
            "company": i.company,
            "address": i.address
        })
    return jsonify({'ret': 'true', 'data': {'findDesign': desion}})


#  问题列表
@main.route('/problem/', methods=['GET'])
def problem():
    user = session.get('user_id')
    print(user)
    if user != None:
        list = Posts.query.order_by(db.desc(Posts.id))
        question = []
        response = []
        for i in list:
            #  回答该问题用户的数量
            replyCount = Posts.query.filter_by(pid=i.id).count()
            if i.rid != 0:
                u = Personal.query.filter_by(id=i.p_id).first()
                question.append({
                    "id": i.id,
                    "imgUrl": u.icon,
                    "username": u.nickname,
                    "question": i.title,
                    "replyCount": replyCount,
                    "browseCount": i.counts,
                    "response": response,
                    "time": i.create_time,
                    "style": i.type
                })
            else:
                u1 = Personal.query.filter_by(id=i.p_id).first()
                response.append({
                    "username": u1.nickname,
                    "headImg": u1.icon,
                    "content": i.content,
                    "id": u1.id
                })
        return jsonify({'ret': 'true', 'data': {'question': question}})
    else:
        return 'Have no right to access', 404


# 问题详情
# @main.route('/problem/list/', methods=['GET'])
# def problem_list():
#     user = session.get('user_id')
#     if user != None:
#         if 'problem_id' not in request.values:
#             return jsonify({'ret': 'true', 'data': {'state': '0'}})  # 无效的请求
#         # 获取问题的id
#         problem_id = Posts.query.order_by(id=request.values.get('problem_id'))


# 灵感
@main.route('/static/<kw>', methods=['GET','POST'])
def static(kw):
    data = []
    dic = {
        'recommend': 'recommend',
        'sample': '简约',
        'chinese': '中式',
        'europ': '欧式',
        'america': '美式',
        'vield': '田园',
        'mix': '混搭',
    }
    if kw != 'recommend':
        sid = Styles.query.filter_by(type=dic[kw]).all()
        for i in sid:
            lists = Personal.query.filter_by(id=i.pid).first()
            data.append({
                "id": i.id,
                "imgUrl": i.imgUrl,
                "describe": i.describe,
                "headImg": lists.icon,
                "username": lists.nickname,
                "pid": lists.id
            })
        return jsonify({'ret': 'true', 'data': data })
    else:
        sid1 = Styles.query.order_by(db.desc(Styles.id)).all()
        for i in sid1:
            lists = Personal.query.filter_by(id=i.pid).first()
            data.append({
                "id": i.id,
                "imgUrl": i.imgUrl,
                "describe": i.describe,
                "headImg": lists.icon,
                "username": lists.nickname,
                "pid": lists.id
            })
        return jsonify({'ret': 'true', 'data': data})


# 看日记
@main.route('/diary/', methods=['GET','POST'])
def diary():
    user = session.get('user_id')
    print(user)
    data = []
    if user != None:
        name = Personal.query.filter_by(id=user).first()
        pid = Diary.query.filter_by(pid=user).all()
        for i in pid:
            data.append({
                'id': i.id,
                'title': i.titel,
                'imgurl': i.imgurl,
                'house_money': i.house_money,
                'usable_area': i.usable_area,
                'house_type': i.house_type,
                'house_style': i.house_style,
                'user_img': name.icon
            })
        return jsonify({'ret': 'true', 'data': data})
    return jsonify({'ret': 'true', 'data': '0'})  # 缺少参数


# 系统发送的消息
@main.route('/information/', methods=['GET','POST'])
def information():
    user = session.get('user_id')
    data = []
    if user != None:
        info = Information.query.order_by(db.desc(Information.id)).all()
        for i in info:
            data.append({
                'id': i.id,
                'imgurl': i.imgurl,
                'title': i.title,
                'time': i.time
            })
        return jsonify({'ret': 'true', 'data': data})
    return jsonify({'ret': 'true', 'data': '0'}) # 参数错误


# 话题
@main.route('/topic/', methods=['GET','POST'])
def topic():
    ud = UnderDiscussion.query.order_by(db.desc(UnderDiscussion.id))[:3]
    topic1 =Topics_one.query.order_by(db.desc(Topics_one.id))[:2]
    discuss = []
    topic2 = []
    # 正在评论
    for i in ud:
        discuss.append({
            "id": i.id,
            "imgUrl": i.imgurl,
            "desc": i.title
        })
    # 话题的标题和内容
    for k in topic1:
        imgurl = []
        topic2.append({
            "id": k.id,
            "title": k.title,
            "desc": k.content,
            "imgUrl":imgurl,
            "discusscount":Topics_udcontent.query.filter_by(topics_one_id=k.id).count()
        })
        # 获取评论人的信息
        u = Topics_udcontent.query.filter_by(topics_one_id=k.id).all()
        for j in u:
            x = Personal.query.filter_by(id=j.pid).first()
            imgurl.append({
                'id': x.id,
                'imgUrl': x.icon
            })
    return jsonify({'ret': 'true', 'data': {'discuss': discuss, 'topic': topic2}})


#  正在讨论查看更多
@main.route('/topic/discuss/', methods=['GET','POST'])
def topic_discuss():
    ud = UnderDiscussion.query.order_by(db.desc(UnderDiscussion.id))
    discuss = []
    # 正在评论
    for i in ud:
        discuss.append({
            "id": i.id,
            "imgUrl": i.imgurl,
            "desc": i.title
        })
    return jsonify({'ret': 'true', 'data': discuss})


#  话题查看更多
@main.route('/topic/list/', methods=['GET','POST'])
def topic_list():
    topic1 = Topics_one.query.order_by(db.desc(Topics_one.id))
    topic2 = []
    for i in topic1:
        imgurl = []
        topic2.append({
            "id": i.id,
            "title": i.title,
            "desc": i.content,
            "imgUrl": imgurl,
            "discusscount": Topics_udcontent.query.filter_by(topics_one_id=i.id).count()
        })
        # 获取评论人的信息
        u = Topics_udcontent.query.filter_by(topics_one_id=i.id).all()
        for j in u:
            x = Personal.query.filter_by(id=j.pid).first()
            imgurl.append({
                'id': x.id,
                'imgUrl': x.icon
            })
    return jsonify({'ret': 'true', 'data': topic2})


# 话题点进页面
@main.route('/topic/subpage/<int:kw>', methods=['GET', 'POST'])
def topic_subpage(kw):
    title = Topics_one.query.filter_by(id=kw).first()
    lists = Topics_udcontent.query.filter_by(topics_one_id=kw).all()
    replaycontent = []
    data = {
        "topicsubpage": {
            "title": title.title,
            "desc": title.content,
            "replaycount": Topics_udcontent.query.filter_by(topics_one_id=title.id).count()
        },
        "replaycontent": replaycontent
    }
    for i in lists:
        uid = Personal.query.filter_by(id=i.pid).first()
        replaycontent.append({
            "id": uid.id,
            "username": uid.nickname,
            "imgUrl": uid.icon,
            "city": uid.address,
            "desc": i.content,
            "img": [i.imgurl1, i.imgurl2, i.imgurl3]
        })
    return jsonify({'ret': 'true', 'data': data})


# 正在讨论点进页面
@main.route('/topic/discuss1/<int:kw>', methods=['GET', 'POST'])
def topic_discuss1(kw):
    l = UnderDiscussion.query.filter_by(id=kw).first()
    l1 = Udcontent.query.filter_by(ud_id=l.id).all()
    replaycontent = []
    data = {
        "topicsubpage": {
            "title": l.title,
            "desc": l.content,
            "replaycount": Udcontent.query.filter_by(ud_id=l.id).count()
        },
        "replaycontent": replaycontent
    }
    for i in l1:
        uid = Personal.query.filter_by(id=i.pid).first()
        replaycontent.append({
            "id": uid.id,
            "username": uid.nickname,
            "imgUrl": uid.icon,
            "city": uid.address,
            "desc": i.content
        })
    return jsonify({'ret': 'true', 'data': data})


from flask.ext.admin.contrib.sqla import ModelView


admin.add_view(ModelView(Personal, db.session, name='个人资料'))
admin.add_view(ModelView(Collects, db.session, name='收藏'))
admin.add_view(ModelView(Design, db.session, name='设计'))
admin.add_view(ModelView(Diary, db.session, name='日记'))
admin.add_view(ModelView(Information, db.session, name='系统消息'))
admin.add_view(ModelView(Posts, db.session, name='问题'))
admin.add_view(ModelView(Styles, db.session, name='灵感'))
admin.add_view(ModelView(Topics, db.session, name='文章'))
admin.add_view(ModelView(Topics_one, db.session, name='讨论标题'))
admin.add_view(ModelView(Topics_udcontent, db.session, name='讨论内容'))
admin.add_view(ModelView(UnderDiscussion, db.session, name='话题标题'))
admin.add_view(ModelView(Udcontent, db.session, name='话题内容'))
admin.add_view(ModelView(Users, db.session, name='用户密码'))
admin.add_view(FileAdmin(base_dir, '/static/upload/', name='文件管理'))