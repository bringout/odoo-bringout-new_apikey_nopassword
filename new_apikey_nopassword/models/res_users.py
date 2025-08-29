# -*- coding: utf-8 -*-

from functools import wraps

from odoo import models, _
from odoo.addons.base.models.res_users import check_identity
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError
from odoo.http import request


def nocheck_identity(fn):
    """ Wrapped method should be an *action method* (called from a button
    type=object), and requires extra security to be executed. This decorator
    checks if the identity (password) has been checked in the last 10mn, and
    pops up an identity check wizard if not.

    Prevents access outside of interactive contexts (aka with a request)
    """
    @wraps(fn)
    def wrapped(self):
        if not request:
            raise UserError(_("This method can only be accessed over HTTP"))
    
        return fn(self)

    wrapped.__has_check_identity = True
    return wrapped

class ResUsers(models.Model):
    _inherit = 'res.users'

    @nocheck_identity
    def api_key_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.users.apikeys.description',
            'name': 'New API Key',
            'target': 'new',
            'views': [(False, 'form')],
        }


class APIKeyDescription(models.TransientModel):
    _inherit = 'res.users.apikeys.description'

    @nocheck_identity
    def make_key(self):
        # only create keys for users who can delete their keys
        self.check_access_make_key()

        description = self.sudo()
        k = self.env['res.users.apikeys']._generate(None, self.sudo().name)
        description.unlink()

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.users.apikeys.show',
            'name': _('API Key Ready'),
            'views': [(False, 'form')],
            'target': 'new',
            'context': {
                'default_key': k,
            }
        }


class APIKeys(models.Model):
    _inherit = 'res.users.apikeys'

    @nocheck_identity
    def remove(self):
        return self._remove()