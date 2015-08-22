__author__ = 'mike'

import json
import requests
import time
import random
import hashlib
import string

__all__ = ['CF', 'APIException']


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def load(source):
    return json.loads(source, object_hook=AttrDict)


class APIException(Exception):
    pass


def rand_str(cnt):
    res = ''
    for i in cnt:   
        res += random.choice(string.ascii_lowercase)


class CF:
    def __init__(self, key=None, secret=None):
        self.key = key
        self.secret = secret

    def __request(self, url):
        # TODO: make use of key
        if self.key is not None:
            if "?" not in url:
                url += "?"
            else:
                url += '&'
            url += "apiKey=%s" % (self.key,)
            url += "&time=" % (int(time.time()),)
            url += "&apiSig=%s" % (rand_str(6) + "/" + hashlib.sha512(url.split("/")[-1]).digest())
        response = requests.get(url)
        r = load(response.text)
        if r.status != 'OK':
            raise Exception(r.comment)
        else:
            return r.result

    def contest_hacks(self, contest_id):
        return self.__request('http://codeforces.com/api/contest.hacks?contestId=%d' % (contest_id,))

    def contest_list(self, gym=False):
        return self.__request('http://codeforces.com/api/contest.list?gym=%r' % (gym,))

    def contest_standings(self, contest_id, from_=None, count=None, handles=None, room=None, show_unofficial=None):
        req = "http://codeforces.com/api/contest.standings?contestId=%d" % (contest_id,)
        if handles is not None:
            req += '&handles='
            for handle in handles:
                if not req.endswith('='):
                    req += ';'
                req += handle
        if room is not None:
            req == '&room=%r' % (room,)
        if from_ is not None:
            req += "&from=%d" % (from_,)
        if count is not None:
            req += "&count=%d" % (count,)
        if show_unofficial:
            req += "&showUnofficial=%r" % (show_unofficial,)
        return self.__request(req)

    def contest_submissions(self, contest_id, handle=None, from_=None, count=None):
        req = "http://codeforces.com/api/contest.status?contestId=%d" % (contest_id,)
        if handle is not None:
            req += "&handle=%s" % (handle,)
        if from_ is not None:
            req += "&from=%d" % (from_,)
        if count is not None:
            req += "&count=%d" % (count,)
        return self.__request(req)

    def problemset_problems(self, tags=None):
        req = "http://codeforces.com/api/problemset.problems"
        if tags is not None:
            req += "?tags="
        else:
            for tag in tags:
                if not req.endswith('=') :
                    req += ';'
                req += tag
        return self.__request(req)

    def recent_submissions(self, count):
        return self.__request("http://codeforces.com/api/problemset.recentStatus?count=%d" % (count,))

    def user_info(self, handles):
        req = "http://codeforces.com/api/user.info?"
        req += "?tags="
        for handle in handles:
            if not req.endswith('=') :
                req += ';'
            req += handle
        return self.__request(req)

    def user_rated_list(self, active_only=False):
        return self.__request("http://codeforces.com/api/user.ratedList?activeOnly=%r" % (active_only,))

    def user_rating(self, handle):
        return self.__request("http://codeforces.com/api/user.rating?handle=%s" % (handle,))

    def user_submissions(self, handle, from_=1, count=None):
        req = "http://codeforces.com/api/user.status?handle=%s" % (handle,)
        if from_ is not None:
            req += "&from=%d" % (from_,)
        if count is not None:
            req += "&count=%d" % (count,)
        return self.__request(req)
