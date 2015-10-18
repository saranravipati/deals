#!/usr/bin/env python

from __future__ import division
import os
import sys
import logging
import MySQLdb
import itertools
import time
import json
import re
import gc
import urllib
from datetime import datetime as dt, timedelta, date
from copy import deepcopy
from math import radians, cos, sin, asin, sqrt
from decimal import Decimal
from collections import OrderedDict
from urlparse import urlparse, urljoin
import base64
import hmac, hashlib
import uuid
from random import randint

from xlrd import open_workbook, xldate_as_tuple
from xlrd.biffh import XLRDError

from django.http import HttpResponse, HttpResponseRedirect
from django.db.models.base import ModelBase
from django.db.models.query import QuerySet
from django.core.exceptions import FieldError, MultipleObjectsReturned
from django.db.models.fields import FieldDoesNotExist
from django.db import IntegrityError, connection
from django.db.models import Q
from django.contrib.sessions.models import Session
from django.http.request import QueryDict
from django.utils import timezone
from django.db.models import ManyToManyField, ForeignKey, IntegerField, \
                                      DecimalField, FloatField, OneToOneField, \
                                      DateTimeField, BooleanField
from django.forms.models import model_to_dict
import bookstore.settings as settings
from django.core.mail import send_mail,EmailMessage

from store.models import *

from dateutil import tz


class BaseClass():

    def get_log_file_path(self, file_name):
        if not file_name.endswith('.log'):
            file_name = file_name.strip() + '.log'

        base_dir = '/var/log/'
        log_dir = os.path.join(base_dir, 'blackbuck')
        self.ensure_dir_exists(log_dir)
        log_file = os.path.join(log_dir, file_name)
        return log_file

    def ensure_dir_exists(self, dir_name):
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)

    def init_logger(self, file_name, debug_mode = False):
        file_path = self.get_log_file_path(file_name)
        log = logging.getLogger(file_path)
        if file_name != 'stats':
            handler   = logging.handlers.RotatingFileHandler(file_path, maxBytes=52428800, backupCount=1000)
            formatter = logging.Formatter('%(asctime)s.%(msecs)d: %(filename)s: %(lineno)d: %(funcName)s: %(levelname)s: %(message)s', "%Y%m%dT%H%M%S")
        else :
            handler = logging.FileHandler(file_path,mode='a')
            formatter = logging.Formatter('%(message)s')

        handler.setFormatter(formatter)
        log.addHandler(handler)
        if debug_mode:
            log.setLevel(logging.DEBUG)
        else:
            log.setLevel(logging.INFO)
        return log

    def close_log_handlers(self, log):
        handlers = log.handlers[:]
        for handler in handlers:
            handler.close()
            log.removeHandler(handler)

    def execute_command(self, cmd):
        from subprocess import Popen, PIPE
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        output, errors = p.communicate()
        if p.returncode:
            return False, errors
        else:
            return True, ''

    def create_cursor(self, server, db, user='root', cursorclass="", timeout_value=5):
        try:
            from MySQLdb.cursors import Cursor, DictCursor, SSCursor, SSDictCursor
            cursor_dict = {'dict': DictCursor, 'ssdict': SSDictCursor, 'ss': SSCursor}
            cursor_class = cursor_dict.get(cursorclass, Cursor)

            conn = MySQLdb.connect(
                        host=server, user=user, db=db,
                        connect_timeout=timeout_value, cursorclass=cursor_class,
                        charset="utf8", use_unicode=True
            )
            if db: conn.autocommit(True)
            cursor = conn.cursor()

        except (KeyboardInterrupt, SystemExit):
            status_msg = "Failed to Create cursor, Ip: %s Db: %s User: %s" % (server, db, user)
            self.log.error("%s, Error: %s", status_msg, traceback.format_exc())
            raise
        except Exception:
            status_msg = "Failed to Create cursor, Ip: %s Db: %s User: %s" % (server, db, user)
            self.log.error("%s, Error: %s", status_msg, traceback.format_exc())
            raise

        return conn, cursor

    def dictfetchall(self, cursor):
        "Returns all rows from a cursor as a dict"
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

    def xcode(self, text, encoding='utf8', mode='strict'):
        if isinstance(text, unicode) or isinstance(text, str):
            return text.strip().encode(encoding, mode) if isinstance(text, unicode) else text.strip()
        else:
            return text

    def read_xls(self, input_file):
        xls_data = []
        resp_status, status_msg = 0, ''
        try:
            xls_workbook = open_workbook(input_file)
            sheet = xls_workbook.sheet_by_index(0)
        except Exception, e:
            return 1, self.get_error_msg(e), xls_data

        # read header values into the list
        keys = [sheet.cell(0, col_index).value for col_index in xrange(sheet.ncols)]
        for row_index in xrange(1, sheet.nrows):
            data_dict = {}
            row_values = [row_val.value for row_val in sheet.row(row_index) if row_val.value]
            if not len(row_values) > 1:
                #Breaking the loop as empty Row
                break

            for col_index in xrange(sheet.ncols):
                value = sheet.cell(row_index, col_index).value
                data_dict[keys[col_index]] = value

            xls_data.append(data_dict)
        return resp_status, status_msg, xls_data

    def split_list(self, l, n):
        final_list = []
        for i in xrange(0, len(l), n):
            final_list.append(l[i:i+n])
        return final_list

    #Converts from Timezone Datetime as in CONVERT_TIME_ZONE settings to UTC Datetime
    def timezone_to_utc(self, dt_obj, tzinfo=settings.CONVERT_TIME_ZONE):
        to_zone   = tz.tzutc()
        from_zone = tz.gettz(tzinfo)
        dt_obj    = dt_obj.replace(tzinfo=from_zone)
        central   = dt_obj.astimezone(to_zone)
        return central

    #Converts a UTC Datetime to Timezone Datetime as in CONVERT_TIME_ZONE settings
    def utc_to_timezone(self, dt_obj, tzinfo=settings.CONVERT_TIME_ZONE):
        from_zone = tz.tzlocal()
        to_zone   = tz.gettz(tzinfo)
        dt_obj    = dt_obj.replace(tzinfo=from_zone)
        central   = dt_obj.astimezone(to_zone)
        return central

    def timezone_now(self, tzinfo=settings.CONVERT_TIME_ZONE, midnight=False):
        '''
        Gives the current IST time
        '''
        to_zone = tz.gettz(tzinfo)
        date = dt.now(to_zone)
        if midnight and date:
            date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        return date

    def current_time(self, epoch=False, midnight=False):
        '''
        Gives the current UTC time
        '''
        curr_time = timezone.now()
        if midnight:
            curr_time = curr_time.replace(hour=0, minute=0, second=0, microsecond=0)
        if epoch:
            curr_time = self.datetime_to_epoc(curr_time)
        return curr_time

    #Converts Datetime Obj to date str
    #If ignore_tzinfo is False, It converts the Datetime to Timezone as in CONVERT_TIME_ZONE settings
    def date_obj_to_str(self, date_obj, pattern='%d %B, %Y - %I:%M %p', date_pattern='%d %B, %Y',
                                                    tzinfo=settings.CONVERT_TIME_ZONE, ignore_tzinfo=False):
        if not date_obj:
            return ''

        if not isinstance(date_obj, dt):
            if isinstance(date_obj, date):
                pattern = date_pattern
            else:
                return ''

        if not ignore_tzinfo:
            date_obj = self.utc_to_timezone(date_obj, tzinfo=tzinfo)

        try:
            return date_obj.strftime(pattern)
        except:
            return ''

    #Converts a date str to Datetime Obj
    #If ignore_tzinfo is False, It converts the Datetime to Timezone as in CONVERT_TIME_ZONE settings
    def date_str_to_date_obj(self, date_str, patterns_list=['%m/%d/%Y %I:%M %p', '%d %B, %Y - %I:%M %p'],
                            tzinfo=settings.CONVERT_TIME_ZONE, ignore_tzinfo=False):
        dt_obj      = ''
        is_matched  = set()

        if not date_str or not patterns_list:
            return dt_obj

        if not isinstance(patterns_list, list):
            patterns_list = [patterns_list]

        for pattern in patterns_list:
            try:
                date_str = self.xcode(date_str)
                pattern  = self.xcode(pattern)
                dt_obj   = dt.strptime(date_str, pattern)
                if not ignore_tzinfo:
                    dt_obj = self.timezone_to_utc(dt_obj, tzinfo=tzinfo)

                is_matched.add(True)
                break
            except ValueError:
                is_matched.add(False)

        if len(is_matched) == 1 and False in is_matched:
            msg = "Failed to match all the patterns, Str: %s -- Patterns List: %s" % (date_str, patterns_list)

        return dt_obj

    #Converts a date str to Timezone str as in CONVERT_TIME_ZONE settings
    def datestr_to_timezone(self, datestr):
        date_obj = self.date_str_to_date_obj(datestr, patterns_list='%d %B, %Y - %I:%M %p', ignore_tzinfo=True)
        date_str = self.date_obj_to_str(date_obj)
        return date_str

    #Converts a Datetime obj to epoc of milliseconds
    #If ignore_tzinfo is False, It converts the Datetime to Timezone as in CONVERT_TIME_ZONE settings
    def datetime_to_epoc(self, date_obj, tzinfo=settings.CONVERT_TIME_ZONE, ignore_tzinfo=True):
        if not ignore_tzinfo:
            date_obj = self.utc_to_timezone(date_obj, tzinfo=tzinfo)

        return time.mktime(date_obj.timetuple()) * 1000.0

    #Converts epoc of milliseconds to Datetime obj
    def epoc_to_datetime(self, epoc_time, return_str=False):
	res_date = dt.fromtimestamp(epoc_time/1000.0)
        res_date = timezone.make_aware(res_date, timezone.get_current_timezone())
        if return_str:
            res_date = res_date.strftime('%Y-%m-%d %H:%M:%S')
	return res_date

    def parse_timedelta(self, timedel_obj):
        if not isinstance(timedel_obj, timedelta):
            return 'Null'

        time_dict = {}
        time_dict['days']   = timedel_obj.days
        time_dict['hours']  = timedel_obj.seconds//3600
        time_dict['minutes'] = (timedel_obj.seconds//60)%60
        time_dict['seconds'] = timedel_obj.seconds

        days, time_str = '', []
        for key, value in time_dict.items():
            if not value or key == 'seconds':
                continue

            if key == 'days':
                days = '%sDy ' % value
            else:
                time_str.append(str(value))

        time_str = ":".join(time_str)
        if days:
            time_str = days + time_str

        if time_dict['hours']:
            time_str += ' Hrs'
        elif time_str:
            time_str += ' Mins'

        if not time_str:
            if time_dict['seconds']:
                time_str = '%s Sec' % time_dict['seconds']
            else:
                time_str = 'Null'

        return time_str

    #Converts a str of Decimal/int/float to resp data type
    #Ie: '234' to 234 or '234.34' to 234.34
    def get_digit(self, value):
        if not value:
            return 0

        if isinstance(value, Decimal) or isinstance(value, int) \
                        or isinstance(value, float) or isinstance(value, long):
            return value

        if isinstance(value, Decimal):
            value = float(value)
        elif value.isdigit():
            value = int(value)
        else:
            try:
                value = float(value)
            except ValueError:
                value = 0
        return value

    #Get a particular Field values from the Model obj passed
    def get_field_value(self, model_obj, fields, delim='', pk=''):
        #Note only query set should be passed
        if not isinstance(fields, list):
            fields = [fields]

        try:
            _values = []
            value_dic = model_obj.__dict__
            for field in fields:
                _values.append(value_dic[field])

            if delim:
                _values = delim.join(_values)

            if pk:
                values = {}
                values[value_dic[pk]] = _values
            else:
                values = _values
        except KeyError:
            values = ''

        return values

    def get_queryset_field_value(self, query_set, fields, delim='', pk=''):
        #Note only query set should be passed
        if not isinstance(fields, list):
            fields = [fields]

        if pk:
            values = {}
        else:
            values = []

        if isinstance(query_set, QuerySet):
            try:
                for i in query_set.values():
                    _values = []
                    for field in fields:
                        _values.append(i[field])
                    if delim:
                        _values = delim.join(_values)

                    if pk:
                        values[i[pk]] =  _values
                    else:
                        values.append(_values)
            except KeyError:
                values = values

        return values

    def get_all_entries(self, model_obj, sort_by=''):
        entries = []
        if isinstance(model_obj, ModelBase):
            entries = model_obj.objects.all()
            if sort_by:
                entries = entries.order_by(sort_by)
        return entries

    def get_obj_distinct_value(self, model_obj, field, sort_by=''):
        entries = []
        if isinstance(model_obj, ModelBase):
            entries = model_obj.objects.values(field).distinct()
            if sort_by:
                entries = entries.order_by(sort_by)
        return entries

    #Get a exact match of the given model obj, using the value passed
    #If 'value' passed it looks for all entries matching dict keys/values
    #If 'value' passed is not dict, it looks for the value in Id field
    def get_exact_match(self, model_obj, value='', value_dict={}):
        if not value and not value_dict:
            return ''

        try:
            if value_dict:
                res_obj = model_obj.objects.get(**value_dict)
            else:
                res_obj = model_obj.objects.get(id=value)
        except FieldError:
            res_obj = ''
        except model_obj.DoesNotExist:
            res_obj = ''
        except:
            res_obj = ''
        return res_obj

    def get_Q_obj(self, field, value, cond=''):
        q_obj = Q()
        if isinstance(value, list):
            cond = 'in'

        if not cond:
            q_obj = Q(**{"%s" % field: value})
        elif cond == 'regex':
            q_obj = Q(**{"%s__iregex" % field: value})
        else:
            q_obj = Q(**{"%s__%s" % (field, cond): value})

        return q_obj


    def get_distinct_values(self, objs_dict, fields):
        distinct_fields = {}
        if not isinstance(objs_dict, list):
            objs_dict = [objs_dict]

        if not isinstance(fields, list):
            fields = [fields]

        for obj_dict in objs_dict:
            for field in fields:
                if isinstance(field, dict):
                    for pr_field, val_dict in field.items():
                        obj_values  = obj_dict.get(pr_field, {})
                        for key_field, val_field in val_dict.items():
                            key_value = obj_values.get(key_field)
                            if not key_value:
                                continue

                            if isinstance(val_field, dict):
                                distinct_fields.update(self.get_distinct_values(key_value, val_field))
                            else:
                                if isinstance(val_field, list):
                                    value = " ".join(obj_values.get(_val, '')for _val in val_field).strip()
                                else:
                                    value = obj_values.get(val_field, '')
                                distinct_fields[str(key_value)] = str(value)
                else:
                    if isinstance(field, list):
                        value = " ".join(obj_dict.get(_val, '')for _val in field).strip()
                    else:
                        value = obj_dict.get(field, '')
                    distinct_fields[str(field)] = str(value)

        return distinct_fields

    def get_error_msg(self, e):
        error_msg = e.message
        if not error_msg and len(e.args) == 2:
            error_msg = e.args[-1]
        return error_msg

    def get_model_specific_dict(self, data, model_class):
        status_msg, result_dict = "", {}
        if not model_class:
            return "Model CLass can\'t be empty!", result_dict

        if not data:
            return "Data can\'t be empty!", result_dict

        if not isinstance(data, QueryDict) and not isinstance(data, dict):
            return "Data should be QueryDict or Dict", result_dict

        if not isinstance(model_class, list):
            model_class = [model_class]

        data_keys = set(data.keys())
        for _model in model_class:
            if not isinstance(_model, ModelBase):
                status_msg = 'Given "model_class" is not Django Model Instance'
                return status_msg, result_dict

        for _model in model_class:
            model_dict = result_dict.setdefault(_model, {})
            for key in data_keys:
                if isinstance(data, dict):
                    values_list = data[key]
                    if not isinstance(values_list, list) and not isinstance(values_list, tuple):
                        values_list = [values_list]
                else:
                    values_list = data.getlist(key)

                try:
                    field = _model._meta.get_field(key)
                except FieldDoesNotExist:
                    continue

                if isinstance(field, IntegerField) or isinstance(field, DecimalField) \
                            or isinstance(field, FloatField)  or isinstance(field, ForeignKey) \
                            or isinstance(field, OneToOneField):
                    if len(values_list) > 1:
                        status_msg = "Given Field %s is not ManyToMany field" % key
                        status_msg += ", but has multiple values"
                        return status_msg, result_dict

                values = ','.join(str(i) for i in values_list)
                model_dict[key] = values

        return status_msg, result_dict

    def create_model_entry(self, model_class, data, update=False, append_m2m=False):
        status, status_msg, model_obj = 0, '', ''
        if not isinstance(model_class, ModelBase):
            status_msg = 'Given "model_class" is not Django Model Instance'
            return 1, status_msg, model_obj

        if not isinstance(data, dict):
            status_msg = 'Given data should be dictionary'
            return 1, status_msg, model_obj

        if not data:
            status_msg = 'Given data is empty Dict'
            return 1, status_msg, model_obj

        many_to_many = {}
        data_copy = deepcopy(data)
        unique_fields = self.get_unique_fields(model_class)
        required_fields = self.get_required_fileds(model_class)

        for key, value in data_copy.items():
            try:
                field = model_class._meta.get_field(key)
            except FieldDoesNotExist:
                _value = data.pop(key)
                continue

            if isinstance(field, DateTimeField):
                if not isinstance(value, dt):
                    patterns_list = ['%m/%d/%Y %I:%M %p', '%m/%d/%Y %H:%M', '%Y/%m/%d %H:%M']
                    date_obj = self.date_str_to_date_obj(value, patterns_list=patterns_list)
                    if not date_obj and key in required_fields:
                        status_msg = '%s is Required field, But failed to ' % key
                        status_msg += 'match date pattern: %s' % value
                        return 1, status_msg, model_obj
                    elif not date_obj:
                        continue
                    data[key] = date_obj
            elif isinstance(field, IntegerField) or isinstance(field, DecimalField) \
                                               or isinstance(field, FloatField):
                if isinstance(value, str) or isinstance(value, unicode):
                    data[key] = self.get_digit(value)
                elif value:
                    data[key] = value
            elif isinstance(field, BooleanField):
                if self.get_digit(data[key]):
                    data[key] = True
                else:
                    data[key] = False
            elif isinstance(field, ManyToManyField):
                # can't add m2m until parent is saved
                if not value and update == False:
                    _value = data.pop(key)
                    continue

                many_to_many[field] = value
                _value = data.pop(key)
            elif isinstance(field, ForeignKey) or isinstance(field, OneToOneField):
                if not value:
                    _value = data.pop(key)
                    continue

                if not isinstance(value, field.rel.to):
                    args_dict = {field.rel.to._meta.pk.name: value}
                    try:
                        data[key] = field.rel.to.objects.get(**args_dict)
                    except field.rel.to.DoesNotExist:
                        _value = data.pop(key)

        unique_field_objs = {}
        for field in unique_fields:
            if data.has_key(field) and update:
                unique_field_objs[field] = data.pop(field)

        try:
            if data.has_key('id'):
                model_id  = data.pop('id')
                model_obj = self.get_exact_match(model_class, model_id)
                if not model_obj:
                    status_msg = "Failed to get entry with the given Id and given Model Class"
                    return 1, status_msg, model_obj
                created = False
            else:
                if not update:
                    model_obj = model_class.objects.create(**data)
                    created = True
                elif unique_field_objs and update:
                    model_obj, created = model_class.objects.get_or_create(defaults=data, **unique_field_objs)
                else:
                    model_obj, created = model_class.objects.get_or_create(**data)

            if not created and update:
                for attr, value in data.iteritems():
                    try:
                        setattr(model_obj, attr, value)
                    except:
                        pass
                model_obj.save()
        except TypeError as e:
            return 1, self.get_error_msg(e), model_obj
        except ValueError as e:
            return 1, self.get_error_msg(e), model_obj
        except IntegrityError as e:
            return 1, self.get_error_msg(e), model_obj
        except Exception, e:
            return 1, self.get_error_msg(e), model_obj

        for field, value in many_to_many.items():
            if isinstance(value, field.rel.to):
                values = [value]
            elif update and not value:
                values = []
            elif isinstance(value, int) or isinstance(value, float):
                values = [value]
            elif isinstance(value, str) or isinstance(value, unicode):
                values = [i.strip() for i in value.split(',')]
            elif isinstance(value, list) or isinstance(value, tuple) or isinstance(value, QuerySet):
                values = value
            else:
                continue

            if update and not append_m2m:
                getattr(model_obj, field.name).clear()

            for value in values:
              if isinstance(value, field.rel.to):
                  mm_obj = value
              else:
                  args_dict = {field.rel.to._meta.pk.name: value}
                  try:
                      mm_obj = field.rel.to.objects.get(**args_dict)
                  except field.rel.to.DoesNotExist:
                      continue

              getattr(model_obj, field.name).add(mm_obj)

        model_obj.save()
        return status, status_msg, model_obj

    def get_unique_fields(self, model_class):
        unique_fields = []
        if not isinstance(model_class, ModelBase):
            return unique_fields

        pr_field = model_class._meta.pk
        uf = [i.name for i in model_class._meta.fields if i.unique and i != pr_field]
        unique_fields.extend(uf)

        ut = [unq_field for unique_set in model_class._meta.unique_together for unq_field in unique_set]
        unique_fields.extend(ut)
        return unique_fields

    def is_required_field(self, field_obj):
        pr_field = field_obj.model._meta.pk
        if not field_obj.blank and field_obj != pr_field \
                            and not field_obj.get_default():
            return True
        else:
            return False

    def get_required_fileds(self, model_class):
        if not isinstance(model_class, ModelBase):
            return []

        pr_field = model_class._meta.pk
        return [i.name for i in model_class._meta.fields if not i.blank and i != pr_field]

    def queryset_iterator(self, queryset, chunksize=1000):
        pk = 0
        last_pk = queryset.order_by('-pk')[0].pk
        queryset = queryset.order_by('pk')
        while pk < last_pk:
            for row in queryset.filter(pk__gt=pk)[:chunksize]:
                pk = row.pk
                yield row
            gc.collect()


    def parse_model_dict(self, act_dict):
        resl_dict = {}
        for key, value in act_dict.iteritems():
            if isinstance(value, dict):
                resl_dict.update(self.parse_model_dict(value))
            elif isinstance(value, list):
                if key == 'role':
                    values = []
                    for _val in value:
                        values.extend(_val.values())
                    resl_dict[key] = ", ".join(values)
                else:
                    resl_dict[key] = value
            else:
                resl_dict[key] = value
        return resl_dict

    def parse_request_body(self, request):
        try:
            parsed_data = json.loads(request.body)
        except:
            try:
                parsed_data = eval(request.body)
            except:
                parsed_data = {}

        return parsed_data

    def parse_json_data(self, data):
        try:
            parsed_data = json.loads(data)
        except:
            try:
                parsed_data = eval(data)
            except:
                parsed_data = {}

        return parsed_data

    def check_missing_fields(self, request_body, mandatory_fields):
        '''
        Function to check missing and blank fields in the request_body dict
        '''
        status_msg, resp_status = '', 0
        missing_fields = []
        blank_fields = []
        for fl in mandatory_fields:
            try:
                if (request_body[fl] == ""):
                    blank_fields.append(fl)
            except KeyError:
                missing_fields.append(fl)

        if blank_fields:
            status_msg = "%s fields can't be blank" % (str(blank_fields))
            resp_status = 1
        if missing_fields:
            status_msg += "%s fields are missing" % (str(missing_fields))
            resp_status = 1

        return status_msg, resp_status

    def sanitize_string(self, data):
        if not data:
            return data
        data = str(data)
        data = data.upper()

        #Remove whitespaces
        data_l = [elem.strip() for elem in data.split(' ')]
        data = ''.join(data_l)

        data = data.replace('.','')
        data = data.replace(',','')
        data = data.replace('-','')
        data = data.replace('_','')
        data = data.replace(';','')
        return data

    def get_list(self, obj):
        obj_list = []
        if isinstance(obj, str) or isinstance(obj, unicode):
            obj_list = [i.strip() for i in obj.split(',') if i]
        elif isinstance(obj, list):
            obj_list = obj
        else:
            obj_list = [obj]
        return obj_list

    def is_mobile_request(self, request):
        status = False
        ua = request.META.get('HTTP_USER_AGENT', '')
        if not ua:
            return status

        is_android = re.search('android', ua, re.IGNORECASE)
        is_iphone  = re.search('iphone', ua, re.IGNORECASE)
        is_ipad    = re.search('ipad', ua, re.IGNORECASE)
        if is_android or is_iphone or is_ipad:
            status = True

        return status

    def get_time_diff_str(self, dt1, dt2, f_post_fix=False):
        '''
        Returns time difference between dt1 and dt2 in format - 2 days, 15 hours
        If post_fix is True, then time diff is calculated w.r.t. dt2
        '''
        if dt1 > dt2:
            t_delta = dt1 - dt2
            post_fix = ' later'
        else:
            t_delta = dt2 - dt1
            post_fix = ' ago'
        days_diff = (t_delta).days
        hours_diff = (t_delta).seconds / 3600
        time_diff = []
        if days_diff:
            if days_diff == 1:
                day_string = "day"
            else:
                day_string = "days"
            time_diff.append("%d %s" % (abs(days_diff), day_string))
        if hours_diff:
            if hours_diff == 1:
                hours_string = "hour"
            else:
                hours_string = "hours"
            time_diff.append("%d %s" % (abs(hours_diff), hours_string))

        time_diff_str = ', '.join(time_diff)
        if f_post_fix:
            time_diff_str += post_fix
        return time_diff_str

    def random_with_N_digits(self, n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return randint(range_start, range_end)

    def get_enum(self, model_class, field_name, choice_text):
        '''
        This function returns the enum value for the given text from the model_class.field
        '''
        enum_val = ''
        try:
            choices = model_class._meta.get_field(field_name).choices
        except FieldDoesNotExist:
            pass
        else:
            for choice in choices:
                if choice[1] == choice_text:
                    enum_val = choice[0]
        return enum_val

    def get_text_for_enum(self, model_class, field_name, enum_val):
        '''
        This function returns the text for given enum value for the model_class.field
        '''
        choice_text = ''
        try:
            choices = model_class._meta.get_field(field_name).choices
        except FieldDoesNotExist:
            pass
        else:
            for choice in choices:
                if choice[0] == enum_val:
                    choice_text = choice[1]
        return choice_text

    def delete_entry(self, model_class, model_id):
        '''
        This function deletes an entry from the given model_class with given id
        '''
        table = "base_%s" % model_class.__name__.lower()

        cursor = connection.cursor()
        try:
            query = "DELETE FROM %s WHERE id = %s" % (table, model_id)
            cursor.execute(query)
        finally:
            cursor.close()

    def get_request_domain_url(self, request):
        status_msg, domain_url = '', ''
        absolute_uri = request.build_absolute_uri()
        if not absolute_uri:
            status_msg = "Failed to get Absolute Url from Request"
            return status_msg, domain_url

        parsed_uri = urlparse(absolute_uri)
        domain_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        return status_msg, domain_url

    def parse_unhandled_types(self, response_dict, date_to_epoch=False):
        for key, value in response_dict.items():
            if isinstance(value, dict):
                response_dict[key] = self.parse_unhandled_types(value, date_to_epoch=date_to_epoch)

            if isinstance(value, datetime) or isinstance(value, date):
                if isinstance(value, datetime) and date_to_epoch==True:
                    response_dict[key] = self.datetime_to_epoc(value)
                else:
                    response_dict[key] = self.date_obj_to_str(value)

            if isinstance(value, Decimal):
                response_dict[key] = str(value)

            if isinstance(value, list) or isinstance(value, tuple):
                new_values = [] 
                for _value in value:
                    if isinstance(_value, dict):
                        new_values.append(self.parse_unhandled_types(_value, date_to_epoch=date_to_epoch))
                    elif isinstance(_value, datetime) or isinstance(_value, date):
                        if isinstance(_value, datetime) and date_to_epoch==True:
                            new_values.append(self.datetime_to_epoc(_value))
                        else:
                            new_values.append(self.date_obj_to_str(_value))
                    elif isinstance(_value, Decimal):
                        new_values.append(str(_value))
                    else:
                        new_values.append(_value)

                if isinstance(value, list):
                    response_dict[key] = new_values
                else:
                    response_dict[key] = tuple(new_values)

        return response_dict

def main():
    pass

if __name__ == '__main__':
    main()
