# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api, exceptions


class Course(models.Model):
    _name = 'test.course'

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description", required=False)

    responsible_id = fields.Many2one(
        'res.users', ondelete='set null', string="Responsible", index=True)
    session_ids = fields.One2many(
        'test.session', 'course_id', string="Sessions")
    session_count = fields.Integer(compute="_get_session_count")

    @api.multi
    def send_mail_template(self):
        template = self.env.ref('test.example_email_template')
        self.env['mail.template'].browse(template.id).send_mail(self.id)

    @api.depends('session_ids')
    def _get_session_count(self):
        for r in self:
            if not r.session_ids:
                r.session_count = 0
            else:
                r.session_count = len(r.session_ids)

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"compy if {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy if {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name!= description)',
         "The title if the course should not be the description"),
        ('name_unique',
         'UNIQUE(name)',
         "the course title must be unique")
    ]


class Session(models.Model):
    _name = "test.session"

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(
        digits=(6, 2), help="Duration in days", default=1.0)
    seats = fields.Integer(string="Number of seats", default=1)
    active = fields.Boolean(default=True)
    instructor_id = fields.Many2one('res.partner', string="Instructor",
                                    domain=['|', ('instructor', '=', True),
                                            ('category_id.name', 'ilike', "Teacher")])
    course_id = fields.Many2one('test.course',
                                ondelete='cascade', string="course", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')
    end_date = fields.Date(string="End Date", store=True,
                           compute='_get_end_date', inverse='_set_end_date')

    hours = fields.Float(string="Duration in hours",
                         compute='_get_hours', inverse='_set_hours')

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            raise exceptions.UserError(
                'the number of acailable seats may not be negative')

        if self.seats < len(self.attendee_ids):
            raise exceptions.UserError(
                'Increase seats or remove excess attendees')

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue

            # add duration to start_date, but: Monday + 5 days = saturday, so
            # substract one second to get on friday instead
            start = fields.Datetime.from_string(r.start_date)
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = start + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue

            # compute the difference between dates, but friday - monday = 4 days
            # so add one day to get 5 days instead
            start_date = fields.Datetime.from_string(r.start_date)
            end_date = fields.Datetime.from_string(r.end_date)
            r.duration = (end_date - start_date).days+1

    @api.depends('duration')
    def _get_hours(self):
        for r in self:
            r.hours = r.duration * 24

    def _set_hours(self):
        for r in self:
            r.duration = r.hours / 24

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError(
                    "A session's instructor can't be an attendees")

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"compy if {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy if {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(Session, self).copy(default)

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "the session title must be unique")
    ]
