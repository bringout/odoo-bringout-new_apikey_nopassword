# odoo module new api key for user with oidc specification

## The goal 

This module have to change current odoo view in base module @odoo16/odoo/addons/base/views/res_user_views.xml so 

if user activate api_key_wizard

```
    @check_identity
    def api_key_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.users.apikeys.description',
            'name': 'New API Key',
            'target': 'new',
            'views': [(False, 'form')],
        }
```

it should override default check identity:

```
def check_identity(fn):
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

        if request.session.get('identity-check-last', 0) > time.time() - 10 * 60:
            # update identity-check-last like github?
            return fn(self)

        w = self.sudo().env['res.users.identitycheck'].create({
            'request': json.dumps([
                { # strip non-jsonable keys (e.g. mapped to recordsets like binary_field_real_user)
                    k: v for k, v in self.env.context.items()
                    if _jsonable(v)
                },
                self._name,
                self.ids,
                fn.__name__
            ])
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.users.identitycheck',
            'res_id': w.id,
            'name': _("Security Control"),
            'target': 'new',
            'views': [(False, 'form')],
        }
    wrapped.__has_check_identity = True
    return wrapped
```

so it always skip "Security control" res.users.identitycheck


```
class CheckIdentity(models.TransientModel):
    """ Wizard used to re-check the user's credentials (password)

    Might be useful before the more security-sensitive operations, users might be
    leaving their computer unlocked & unattended. Re-checking credentials mitigates
    some of the risk of a third party using such an unattended device to manipulate
    the account.
    """
    _name = 'res.users.identitycheck'
    _description = "Password Check Wizard"

    request = fields.Char(readonly=True, groups=fields.NO_ACCESS)
    password = fields.Char()

    def run_check(self):
        assert request, "This method can only be accessed over HTTP"
        try:
            self.create_uid._check_credentials(self.password, {'interactive': True})
        except AccessDenied:
            raise UserError(_("Incorrect Password, try again or click on Forgot Password to reset your password."))
        finally:
            self.password = False

        request.session['identity-check-last'] = time.time()
        ctx, model, ids, method = json.loads(self.sudo().request)
        method = getattr(self.env(context=ctx)[model].browse(ids), method)
        assert getattr(method, '__has_check_identity', False)
        return method()

```

```
class APIKeyDescription(models.TransientModel):
    _name = 'res.users.apikeys.description'
    _description = 'API Key Description'

    name = fields.Char("Description", required=True)

    @check_identity
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

    def check_access_make_key(self):
        if not self.user_has_groups('base.group_user'):
            raise AccessError(_("Only internal users can create API keys"))

```

## Install details

### module location

Module location: backend/custom_addons/new_apikey_nopassword

### module install

Change flake.nix shellHook: include module in odoo conf 

### add scripts/odoo_install.sh

create or update scripts/odoo_install.sh to install this module into odoo database, using nix develop construct
```
nix develop -c bash -c "python ..."
```

