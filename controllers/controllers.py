# -*- coding: utf-8 -*-
# from flectra import http


# class AdraAccountExtended(http.Controller):
#     @http.route('/adra_account_extended/adra_account_extended/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/adra_account_extended/adra_account_extended/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('adra_account_extended.listing', {
#             'root': '/adra_account_extended/adra_account_extended',
#             'objects': http.request.env['adra_account_extended.adra_account_extended'].search([]),
#         })

#     @http.route('/adra_account_extended/adra_account_extended/objects/<model("adra_account_extended.adra_account_extended"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('adra_account_extended.object', {
#             'object': obj
#         })
