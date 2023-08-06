'''
Created on 19 Feb 2021

@author: jacklok
'''
from orderedset import OrderedSet

REWARD_BASE_ON_VISIT            = 'visit'
REWARD_BASE_ON_SPENDING         = 'spending'
REWARD_BASE_ON_PREPAID          = 'prepaid'
REWARD_BASE_ON_MEMBER           = 'member'
REWARD_BASE_ON_REFER            = 'refer'

REWARD_BASE_SET                 = (REWARD_BASE_ON_VISIT, REWARD_BASE_ON_SPENDING, REWARD_BASE_ON_PREPAID, REWARD_BASE_ON_MEMBER, REWARD_BASE_ON_REFER)

REWARD_FORMAT_POINT             = 'point'
REWARD_FORMAT_STAMP             = 'stamp'
REWARD_FORMAT_CASH              = 'cash'
REWARD_FORMAT_VOUCHER           = 'voucher'
REWARD_FORMAT_DISCOUNT          = 'discount'
REWARD_FORMAT_MIXED             = 'mixed'

REWARD_FORMAT_SET               = (REWARD_FORMAT_POINT, REWARD_FORMAT_STAMP, REWARD_FORMAT_CASH, REWARD_FORMAT_VOUCHER, REWARD_FORMAT_MIXED)

PROGRAM_STATUS_REWARD_BASE          = 'reward_base'
PROGRAM_STATUS_REWARD_FORMAT        = 'reward_format'
PROGRAM_STATUS_REWARD_SCHEME        = 'reward_scheme'
PROGRAM_STATUS_REWARD_DETAILS       = 'reward_details'
PROGRAM_STATUS_UPLOAD_MATERIAL      = 'upload_material'
PROGRAM_STATUS_REVIEW               = 'review'
PROGRAM_STATUS_PUBLISH              = 'published'

PROGRAM_STATUS                  = OrderedSet([PROGRAM_STATUS_REWARD_BASE, 
                                              PROGRAM_STATUS_REWARD_FORMAT, 
                                              PROGRAM_STATUS_REWARD_SCHEME, 
                                              #PROGRAM_STATUS_REWARD_DETAILS, 
                                              #PROGRAM_STATUS_UPLOAD_MATERIAL,
                                              #PROGRAM_STATUS_REVIEW, 
                                              PROGRAM_STATUS_PUBLISH
                                              ])


VOUCHER_STATUS_BASE                 = 'voucher_base'
VOUCHER_STATUS_CONFIGURATION        = 'voucher_configuration'
VOUCHER_STATUS_UPLOAD_MATERIAL      = 'upload_material'
VOUCHER_STATUS_PUBLISH              = 'published'

VOUCHER_STATUS                  = OrderedSet([VOUCHER_STATUS_BASE, 
                                              VOUCHER_STATUS_CONFIGURATION,
                                              VOUCHER_STATUS_UPLOAD_MATERIAL, 
                                              VOUCHER_STATUS_PUBLISH
                                              ])

PRORRAM_NEXT_STEP_AND_COMPLELTED_STATUS_MAPPING = {
                                                    PROGRAM_STATUS_REWARD_BASE: 2
                                                    }


def get_program_completed_status_index(completed_status):
    return PROGRAM_STATUS.index(completed_status)

def get_voucher_completed_status_index(completed_status):
    return VOUCHER_STATUS.index(completed_status) 

def is_program_current_status_reach(checking_status, completed_status):
    completed_status_index  = get_program_completed_status_index(completed_status)
    checking_status_index   = get_program_completed_status_index(checking_status)
    
    print('completed_status_index=%s'%completed_status_index)
    print('checking_status_index=%s'%checking_status_index)
    
    return checking_status_index<=completed_status_index+1

def is_voucher_current_status_reach(checking_status, completed_status):
    completed_status_index  = get_voucher_completed_status_index(completed_status)
    checking_status_index   = get_voucher_completed_status_index(checking_status)
    
    print('completed_status_index=%s'%completed_status_index)
    print('checking_status_index=%s'%checking_status_index)
    
    return checking_status_index<=completed_status_index+1

def is_valid_to_update_program_status(checking_status, completed_status):
    completed_status_index  = get_program_completed_status_index(completed_status)
    checking_status_index   = get_program_completed_status_index(checking_status)
    
    return checking_status_index<=completed_status_index+1

def is_valid_to_update_voucher_status(checking_status, completed_status):
    completed_status_index  = get_voucher_completed_status_index(completed_status)
    checking_status_index   = get_voucher_completed_status_index(checking_status)
    
    return checking_status_index<=completed_status_index+1


def is_existing_program_status_higher_than_updating_status(checking_status, completed_status):
    completed_status_index  = get_program_completed_status_index(completed_status)
    checking_status_index   = get_program_completed_status_index(checking_status)
    
    return checking_status_index<completed_status_index

def is_existing_voucher_status_higher_than_updating_status(checking_status, completed_status):
    completed_status_index  = get_voucher_completed_status_index(completed_status)
    checking_status_index   = get_voucher_completed_status_index(checking_status)
    
    return checking_status_index<completed_status_index

def is_existing_program_status_final_state(completed_status):
    completed_status_index  = get_program_completed_status_index(completed_status)
    
    return completed_status_index==len(PROGRAM_STATUS)-2

def is_existing_voucher_status_final_state(completed_status):
    completed_status_index  = get_voucher_completed_status_index(completed_status)
    
    return completed_status_index==len(PROGRAM_STATUS)-2    
    

