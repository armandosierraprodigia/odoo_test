from odoo import api, fields, models, exceptions


class Quotation(models.Model):
    _inherit = "sale.order"

    course_id = fields.Many2one('test.course', 'Course')

    valid_course = fields.Boolean(default=False)

    @api.onchange('course_id')
    def _verify_valid_seats(self):
        if self.course_id:
            if not self.course_id.responsible_id:
                self.valid_course = False
                return {
                    'warning': {
                        'title': "Course selected",
                        'message': "This course dont have a responsible so first select one",
                    },
                }
            else:
                self.valid_course = True

    @api.constrains('course_id')
    def _check_valid_course(self):
        for r in self:
            if self.course_id:
                if not r.valid_course:
                    raise exceptions.ValidationError(
                        "The selected course is invalid")

    # overwrite of parent method to do some validations
    # this is commented because  @api.constrains can do that validation
    # @api.model
    # def create(self, values):
    #     if values["course_id"]:
    #         if "valid_course" in values:
    #             if not values['valid_course']:
    #                 raise exceptions.ValidationError(
    #                     "A selected course is invalid")
    #             else:
    #                 return super(Quotation, self).create(values)
    #         else:
    #             return super(Quotation, self).create(values)
    #     else:
    #         return super(Quotation, self).create(values)
