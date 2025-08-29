from django.utils.translation import gettext_lazy as _
from pretix.base.payment import BasePaymentProvider, PaymentException

class DpayPaymentProvider(BasePaymentProvider):
    identifier = 'dpay'
    verbose_name = _('DPay Payment')
    public_name = _('DPay')
    is_enabled = True

    def __init__(self, event, *args, **kwargs):
        super().__init__(event, *args, **kwargs)
        self.api_key = self.settings.get('api_key', '')
        
    def payment_is_valid_session(self, request):
        """
        Valida si la sesión de pago es válida.
        En lugar de llamar a super(), implementamos la lógica específica para DPay.
        """
        print(f"payment_is_valid_session recibe este request: {request}")
        
        # Aquí implementas tu lógica de validación específica para DPay
        # Por ejemplo, verificar si hay datos de pago en la sesión
        session_data = request.session.get(f'payment_{self.identifier}', {})
        
        # Ejemplo de validación básica
        if not self.api_key:
            print("API key no configurada para DPay")
            return False
            
        # Puedes agregar más validaciones específicas aquí
        # Por ejemplo, verificar tokens, estados de transacción, etc.
        
        # Para desarrollo/testing, retornamos True
        # En producción, implementa tu lógica de validación real
        return True

    def payment_form_render(self, request) -> str:
        """
        Renderiza el formulario de pago
        """
        print(f"payment_form_render recibe este request: {request}")
        
        # TODO: implementar vista real de formulario de pago
        html_form = '''
        <div class="dpay-payment-form">
            <h4>DPay Payment</h4>
            <p>Formulario de pago de DPay</p>
            <input type="hidden" name="payment_provider" value="dpay" />
            <!-- Aquí agregarás los campos específicos de DPay -->
        </div>
        '''
        
        return html_form

    def execute_payment(self, request, payment):
        """
        Ejecuta el proceso de pago
        """
        if not self.api_key:
            raise PaymentException(_('Credenciales para DPay no han sido configuradas.'))
            
        print(f"Ejecutando pago con DPay para payment ID: {payment.pk}")
        
        try:
            # TODO: Aquí implementarías la lógica real de conexión con DPay API
            # Por ahora simulamos un pago exitoso
            
            # Simular procesamiento de pago
            payment.info = _('Pago procesado via DPay.')
            payment.state = 'confirmed'  # Cambié de 'paid' a 'confirmed' que es más apropiado
            payment.save()
            
            print(f"Pago completado exitosamente para payment ID: {payment.pk}")
            
        except Exception as e:
            print(f"Error en execute_payment: {e}")
            raise PaymentException(_('Error procesando pago con DPay: {error}').format(error=str(e)))

    def payment_pending_render(self, request, payment):
        """
        Renderiza la vista cuando el pago está pendiente
        """
        return _('Tu pago con DPay está siendo procesado.')

    def payment_control_render(self, request, payment):
        """
        Renderiza información del pago en el panel de control
        """
        if payment.info:
            return f"<p><strong>DPay:</strong> {payment.info}</p>"
        return ""

    @property
    def settings_form_fields(self):
        """
        Define los campos de configuración para el plugin
        """
        from django import forms
        
        fields = {}
        
        fields['api_key'] = forms.CharField(
            label=_('API Key'),
            help_text=_('Tu clave API de DPay'),
            required=True,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tu API Key de DPay'
            })
        )
        
        fields['sandbox_mode'] = forms.BooleanField(
            label=_('Modo Sandbox'),
            help_text=_('Activar para usar el ambiente de pruebas de DPay'),
            required=False,
            initial=True
        )
        
        fields['webhook_secret'] = forms.CharField(
            label=_('Webhook Secret'),
            help_text=_('Secreto para validar webhooks de DPay'),
            required=False,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Opcional: Secret para webhooks'
            })
        )
        
        return fields

    @property
    def is_meta(self):
        """
        Indica si este proveedor es un meta-proveedor
        """
        return False

    def payment_prepare(self, request, payment):
        """
        Prepara el pago antes de ejecutarlo
        """
        # Aquí puedes agregar lógica de preparación si es necesaria
        pass

    def payment_can_retry(self, payment):
        """
        Indica si un pago fallido puede reintentarse
        """
        return payment.state in ['failed', 'canceled']

    def payment_refund_supported(self, payment):
        """
        Indica si este pago puede ser reembolsado
        """
        return payment.state == 'confirmed'

    def execute_refund(self, refund):
        """
        Ejecuta un reembolso
        """
        # TODO: Implementar lógica de reembolso con DPay API
        refund.state = 'done'
        refund.save()