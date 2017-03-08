# -*- coding: utf-8 -*-
#__author__ = 'koufana'

from openerp.osv import osv
from openerp import models, fields, api, _
from openerp.osv.orm import except_orm
from datetime import date
import time
import math
import logging


class fleet_vehicle(models.Model):

    _name = 'fleet.vehicle'
    _inherit = 'fleet.vehicle'
    _description = 'Information on a vehicle'
    
    @api.model
    def create(self, vals):
        if(not vals["department_id"] and not vals["department_id"]) :
            raise osv.except_osv(_('Define Department or project!'), _('Define Department or project.'))
        acount_obj=self.env['account.analytic.account']
        parent_id = 0
        if(vals["project_id"]) :
            project_obj=self.env['project.project']
            project = project_obj.browse(vals["project_id"])[0]
            parent_id = project.analytic_account_id.id
        else :
            d_obj=self.env['hr.department']
            d = d_obj.browse(vals["department_id"])[0]
            parent_id = d.analytic_account_id.id
        fleet_id = super(fleet_vehicle, self).create(vals)
        account_id=acount_obj.create({'name':fleet_id.license_plate,'parent_id':parent_id})
        fleet_id.write({'analytic_account_id':account_id.id})
        return fleet_id
    
    @api.multi
    def write(self, vals):
        acount_obj=self.env['account.analytic.account']
        department_id = self.department_id
        project_id = self.project_id
        res = super(fleet_vehicle, self).write(vals)
        if(not self.department_id and not self.project_id):
            raise osv.except_osv(_('Define Department or project!'), _('Define Department or project.'))
            
        if not self.analytic_account_id:
            if(self.project_id) :
                project_obj=self.env['project.project']
                project = project_obj.browse(self.project_id.id)[0]
                parent_id = project.analytic_account_id.id
            else :
                d_obj=self.env['hr.department']
                d = d_obj.browse(self.department_id.id)[0]
                parent_id = d.analytic_account_id.id
            account_id=acount_obj.create({'name':self.license_plate,'parent_id':parent_id})
            super(fleet_vehicle, self).write({'analytic_account_id':account_id.id})
        else :
            if(self.project_id) :
                project_obj=self.env['project.project']
                project = project_obj.browse(self.project_id.id)[0]
                parent_id = project.analytic_account_id.id
            elif(self.department_id) :
                d_obj=self.env['hr.department']
                d = d_obj.browse(self.department_id.id)[0]
                parent_id = d.analytic_account_id.id
            aid = acount_obj.search([('name','=',self.license_plate),('parent_id','=',parent_id)])
            if(aid) :
                account_id = aid
                super(fleet_vehicle, self).write({'analytic_account_id':account_id.id})
            else :
                if(self._count_analytic_journal <= 0):
                    account_id=acount_obj.create({'name':self.license_plate,'parent_id':parent_id})
                    super(fleet_vehicle, self).write({'analytic_account_id':account_id.id})
                else:
                    self.analytic_account_id.write({'name':self.license_plate,'parent_id':parent_id})
            self.analytic_account_id.write({'name':self.license_plate})
        return res
    
    
    @api.multi
    def _count_analytic_journal(self):
        account_line_obj = self.env['account.analytic.line']
        self.analytic_journal_count=account_line_obj.search_count([('account_id', '=', self.analytic_account_id.id)])
        
    
    project_id = fields.Many2one('project.project', 'Project')
    department_id = fields.Many2one('hr.department', 'Department')
    analytic_account_id = fields.Many2one('account.analytic.account', 'Account Analytic account')
    analytic_journal_count = fields.Integer(compute = _count_analytic_journal, string='Analytic Journal', multi=True)
    