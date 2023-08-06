'''
Created on 19 Feb 2021

@author: jacklok
'''
from google.cloud import ndb
from trexmodel.models.datastore.ndb_models import BaseNModel, DictModel
from trexmodel.models.datastore.user_models import User
import trexmodel.conf as model_conf
from trexlib.utils.string_util import random_number, is_not_empty
from trexmodel.models.datastore.merchant_models import MerchantAcct, Outlet,\
    MerchantUser
from trexmodel.models.datastore.coporate_models import CorporateAcct
import logging
from trexlib.utils.common.cache_util import cache
from trexmodel import conf, program_conf
from datetime import datetime

from six import string_types



logger = logging.getLogger('model')


class ProgramBase(BaseNModel, DictModel):
    reward_base             = ndb.StringProperty(required=True, choices=set(program_conf.REWARD_BASE_SET))
    reward_format           = ndb.StringProperty(required=False, choices=set(program_conf.REWARD_FORMAT_SET))
    completed_status        = ndb.StringProperty(required=True, choices=set(program_conf.PROGRAM_STATUS))
    
    start_date              = ndb.DateProperty(required=True)
    end_date                = ndb.DateProperty(required=True)
    desc                    = ndb.StringProperty(required=False)
    program_settings        = ndb.JsonProperty(required=True)
    created_datetime        = ndb.DateTimeProperty(required=True, auto_now_add=True)
    modified_datetime       = ndb.DateTimeProperty(required=True, auto_now=True)
    published_datetime      = ndb.DateTimeProperty(required=False)
    archived_datetime       = ndb.DateTimeProperty(required=False)
    
    
    created_by              = ndb.KeyProperty(name="created_by", kind=MerchantUser)
    created_by_username     = ndb.StringProperty(required=False)
    modified_by             = ndb.KeyProperty(name="modified_by", kind=MerchantUser)
    modified_by_username    = ndb.StringProperty(required=False)
    enabled                 = ndb.BooleanProperty(default=True)
    archived                = ndb.BooleanProperty(default=False)
    
    dict_properties         = ['reward_base', 'reward_format', 'completed_status', 'start_date', 'end_date', 'desc', 'program_settings', 
                               'created_datetime', 'modified_datetime',  'enabled','completed_status','is_enabled', 'is_disabled', 'is_review_state', 
                               'is_published', 'archived',
                               'created_by_username', 'modified_by_username']
    
    @property
    def is_enabled(self):
        return self.enabled
    
    @property
    def is_disabled(self):
        return self.enabled==False
    
    @property
    def is_archived(self):
        return self.archived
    
    @property
    def is_published(self):
        return self.completed_status == program_conf.PROGRAM_STATUS_PUBLISH
    
    @property
    def is_review_state(self):
        return program_conf.is_existing_program_status_final_state(self.completed_status)
    
class MerchantProgram(ProgramBase):
    #merchant_acct           = ndb.KeyProperty(name="merchant_acct", kind=MerchantAcct) 
    
    
    @staticmethod
    def create(merchant_acct, reward_base=None, desc=None, start_date=None, end_date=None, created_by=None):
        created_by_username = None
        if is_not_empty(created_by):
            if isinstance(created_by, MerchantUser):
                created_by_username = created_by.username
        
        
        merchant_program =  MerchantProgram(
                                        parent              = merchant_acct.create_ndb_key(),
                                        reward_base         = reward_base,
                                        desc                = desc,
                                        start_date          = start_date,
                                        end_date            = end_date,
                                        created_by          = created_by.create_ndb_key(),
                                        created_by_username = created_by_username,
                                        completed_status    = program_conf.PROGRAM_STATUS_REWARD_BASE,
                                        program_settings    = {},
                                        )
        
        merchant_program.put()
        return merchant_program
    
    @property
    def is_multitier_scheme(self):
        return self.program_settings.get('is_multitier_scheme')
    
    @property
    def spending_currency(self):
        return self.program_settings.get('scheme').get('spending_currency')
    
    @property
    def reward_amount(self):
        return self.program_settings.get('scheme').get('reward_amount')
    
    @property
    def merchant_acct(self):
        return MerchantAcct.fetch(self.key.parent().urlsafe())
    
    def to_program_configuration(self):
        program_configuration = {
                                'program_key'       : self.key_in_str,
                                'reward_base'       : self.reward_base,
                                'reward_format'     : self.reward_format,
                                'start_date'        : self.start_date.strftime('%d-%m-%Y'),
                                'end_date'          : self.end_date.strftime('%d-%m-%Y'),    
                                'program_settings'  : self.program_settings,
                                }
        
        return program_configuration
    
    @staticmethod
    def update_program_base_data(merchant_program, reward_base=None, desc=None,start_date=None, end_date=None, modified_by=None):
        
        modified_by_username = None
        
        if is_not_empty(modified_by):
            if isinstance(modified_by, MerchantUser):
                modified_by_username = modified_by.username
        
        merchant_program.reward_base            = reward_base
        merchant_program.desc                   = desc
        merchant_program.start_date             = start_date
        merchant_program.end_date               = end_date
        merchant_program.modified_by            = modified_by.create_ndb_key()
        merchant_program.modified_by_username   = modified_by_username
        merchant_program.completed_status       = program_conf.PROGRAM_STATUS_REWARD_BASE
        
        
        merchant_program.put()
        
        return merchant_program
    
    @staticmethod
    def update_prorgram_reward_format_data(merchant_program, reward_format=None, modified_by=None):
        modified_by_username = None
        
        if is_not_empty(modified_by):
            if isinstance(modified_by, MerchantUser):
                modified_by_username = modified_by.username
        
        merchant_program.reward_format          = reward_format
        merchant_program.modified_by            = modified_by.create_ndb_key()
        merchant_program.modified_by_username   = modified_by_username
        merchant_program.completed_status       = program_conf.PROGRAM_STATUS_REWARD_FORMAT
        
        
        merchant_program.put()
        
        return merchant_program
    
    @staticmethod
    def update_prorgram_reward_scheme_data(merchant_program, is_multitier_scheme=False, reward_scheme_dict={}, modified_by=None):
        modified_by_username = None
        
        if is_not_empty(modified_by):
            if isinstance(modified_by, MerchantUser):
                modified_by_username = modified_by.username
        
        program_settings = {
                            'is_multitier_scheme'   : is_multitier_scheme,
                            'scheme'                : reward_scheme_dict
                            }
                
        merchant_program.modified_by            = modified_by.create_ndb_key()
        merchant_program.modified_by_username   = modified_by_username
        merchant_program.completed_status       = program_conf.PROGRAM_STATUS_REWARD_SCHEME
        merchant_program.program_settings       = program_settings
        
        
        merchant_program.put()
        
        return merchant_program
    
    @staticmethod
    def publish_program(program):
        program.completed_status = program_conf.PROGRAM_STATUS_PUBLISH
        program.published_datetime = datetime.now()
        program.put()
        
        
        merchant_acct = program.merchant_acct
        merchant_acct.update_published_program(program.to_program_configuration())
        
    @staticmethod
    def archive_program(program):
        program.archived = True
        program.archived_datetime = datetime.now()
        program.put()
        
        merchant_acct = program.merchant_acct
        merchant_acct.remove_archieve_program(program.key_in_str)    
    
    @staticmethod
    def enable(program):
        program.enabled = True
        program.put()
        
    @staticmethod
    def disable(program):
        program.enabled = False
        program.put()    
    
    @staticmethod
    def list_by_merchant_account(merchant_acct):
        return MerchantProgram.query(ndb.AND(MerchantProgram.archived!=True), ancestor=merchant_acct.create_ndb_key()).fetch(limit=model_conf.MAX_FETCH_RECORD)
    
    @staticmethod
    def list_archived_by_merchant_account(merchant_acct):
        return MerchantProgram.query(ndb.AND(MerchantProgram.archived==True), ancestor=merchant_acct.create_ndb_key()).fetch(limit=model_conf.MAX_FETCH_RECORD)

class BrandProgram(ProgramBase): 
    #corporate_acct           = ndb.KeyProperty(name="corporate_acct", kind=CorporateAcct)
    pass
    
 
    
       


