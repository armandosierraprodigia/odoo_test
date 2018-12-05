from odoo import api, fields, models, exceptions


class Payment_Method(models.Model):
    _inherit = "account.payment"

    @api.constrains('l10n_mx_edi_payment_method_id')
    def _check_valid_payment_method(self):
        if not self.l10n_mx_edi_payment_method_id:
            raise exceptions.ValidationError(
                "Es necesario seleccionar la forma de pago")

        print(self.l10n_mx_edi_payment_method_id.code)
        if self.l10n_mx_edi_payment_method_id.code == "NA":
            raise exceptions.ValidationError(
                "Es necesario seleccionar la forma de pago diferente a indefinido")

    # @api.onchange('l10n_mx_edi_payment_method_id')
    # def __onchcange_Payment_method(self):
    #     if self.l10n_mx_edi_payment_method_id:
    #         if self.l10n_mx_edi_payment_method_id.id == 99
    #         raise exceptions.ValidationError(
    #             "Es necesario seleccionar la forma de pago diferente a indefinido")
