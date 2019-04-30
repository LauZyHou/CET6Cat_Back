import time

from pymongo import MongoClient


class CET6CatDB:
    """连接MongoDB用"""
    conn = MongoClient('127.0.0.1', 27017)
    # collection:错误单词
    fault_words = conn.cet6cat.fault_words
    # collection:学习情况(看视频,逛论坛,读文章,看作文)
    study_num = conn.cet6cat.study_num
    # collection:翻译记录
    translate = conn.cet6cat.translate


class StudyNumDump:
    """在MongoDB中存储学习记录"""

    @staticmethod
    def dump(kind, uid):
        """记录uid用户在本周kind类型资源的学习次数"""
        # 从格林威治时间到当前经过的周次
        old_week = now_week = int(time.time()) // 604800
        # 当前用户在MongoDB中记录资源数的文档
        doc = CET6CatDB.study_num.find_one({'uid': uid})
        video_lst = [0 for i in range(6)]
        forum_lst = video_lst[:]
        reading_lst = video_lst[:]
        essay_lst = video_lst[:]
        # doc为空时立即在数据库中创建
        if not doc:
            CET6CatDB.study_num.insert({
                'uid': uid,
                # 当前周,用于判定周次变化,周次变化了,则写入时要清0
                'week': now_week,
                'video': video_lst,
                'forum': forum_lst,
                'reading': reading_lst,
                'essay': essay_lst})
        # doc不为空时要查询出更新前的资源情况,以及数据库中记录的周次
        else:
            video_lst = doc['video']
            forum_lst = doc['forum']
            reading_lst = doc['reading']
            essay_lst = doc['essay']
            old_week = doc['week']
        # 判断周是否改变了
        if old_week != now_week:
            # 两者相差多少周
            week_num_between = now_week - old_week
            # 一种优化策略,当相差周次>=6时,其实整张表都要刷掉,不妨就设置为6
            if week_num_between >= 6:
                week_num_between = 6
            # 刷表,从old_week往后刷如此多的周,这段时间用户没学习,刷为0
            for i in range(1, week_num_between + 1):
                idx = (old_week + i) % 6
                video_lst[idx] = forum_lst[idx] = reading_lst[idx] = essay_lst[idx] = 0
        # 在当前周写入数据
        set_dict = {'week': now_week,
                    'video': video_lst,
                    'forum': forum_lst,
                    'reading': reading_lst,
                    'essay': essay_lst}
        set_dict[kind][now_week % 6] += 1
        # 资源数和当前周次更新到数据库
        CET6CatDB.study_num.update({'uid': uid}, {"$set": set_dict})
