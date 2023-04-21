from django.db import models

from django.utils.translation import gettext_lazy as _

class Fornitore(models.Model):
    class Meta:
        verbose_name_plural = "Fornitori"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ragione_sociale = models.CharField(max_length=200)

    def __str__(self):
        return self.ragione_sociale


class Operatore(models.Model):
    class Meta:
        verbose_name_plural = "Operatori"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fornitore = models.ForeignKey(Fornitore, on_delete=models.CASCADE)
    cognome = models.CharField(max_length=200)
    nome = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.cognome} {self.nome} [{self.fornitore}]'


class Cliente(models.Model):
    class Meta:
        verbose_name_plural = "Clienti"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class TipologiaCliente(models.TextChoices):
        NON_DEFINITA = 'ND', _('Non Definita')
        CONDOMINIO = 'CD', _('Condominio')
        PERSONA = 'PS', _('Persona')
        AZIENDA = 'AZ', _('Azienda')

    tipologia_cliente = models.CharField(
        max_length=2,
        choices=TipologiaCliente.choices,
        default=TipologiaCliente.NON_DEFINITA,
    )
    
    aoo = models.IntegerField(null=True, blank=True, default=0)

    denominazione = models.CharField(max_length=200, null=True, blank=True)
    cognome = models.CharField(max_length=200, null=True, blank=True)
    nome = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        nome = ""
        
        if self.tipologia_cliente == 'CD':
            nome = f'{self.aoo} - {self.denominazione}'

        elif self.tipologia_cliente == 'PS':
            nome = "Sig./Sig.ra "
        
        if self.cognome:
            nome += f' {self.cognome} '
        
        if self.nome:
            nome += f' {self.nome}'
        
        return nome


class Intervento(models.Model):
    class Meta:
        verbose_name_plural = "Interventi"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    data = models.DateTimeField(null=True, blank=True)

    def data_onlydate(self):
        return self.data.date()
    data_onlydate.admin_order_field = 'data'
    data_onlydate.short_description = 'Data'
    data_onlydate.allow_tags = True

    operatore = models.ForeignKey(Operatore, on_delete=models.CASCADE, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)

    descrizione = models.TextField(max_length=200)

    minuti_intervento = models.IntegerField(default=0)

    quantita_operatori = models.IntegerField(default=1)
    importo_operatore = models.IntegerField(default=25)
    iva_operatore = models.IntegerField(default=22)
    
    quantita_materiale = models.IntegerField(default=0)
    importo_materiale = models.IntegerField(default=0)
    iva_materiale = models.IntegerField(default=22)
    
    importo_chiamata = models.IntegerField(default=25)
    iva_chiamata = models.IntegerField(default=22)
    
    class Fattura(models.TextChoices):
        NON_FATTURABILE = 'NF', _('Non Fatturabile')
        DA_FATTURARE = 'DF', _('Da Fatturare')
        FATTURATO = 'FT', _('Fatturato')

    fattura = models.CharField(
        max_length=2,
        choices=Fattura.choices,
        default=Fattura.DA_FATTURARE,
    )

    def __str__(self):
        return f'{self.data.date()} {self.cliente}: {self.descrizione}'


    @property
    def totale_materiale(self):
        return float("{:0.2f}".format(self.quantita_materiale * self.importo_materiale))
    #totale_materiale.admin_order_field = 'totale_materiale'
    #totale_materiale.short_description = 'Materiale'
    #totale_materiale.allow_tags = True


    @property
    def totale_iva_materiale(self):
        return float("{:0.2f}".format(self.quantita_materiale * self.importo_materiale / 100 * 22))
    #totale_iva_materiale.admin_order_field = 'name'
    #totale_iva_materiale.short_description = 'IVA Materiale'
    #totale_iva_materiale.allow_tags = True


    @property
    def totale_materiale_ivato(self):
        return float("{:0.2f}".format(self.totale_materiale + self.totale_iva_materiale))
    #totale_materiale_ivato.admin_order_field = 'name'
    #totale_materiale_ivato.short_description = 'Tot. Materiale'
    #totale_materiale_ivato.allow_tags = True


    @property
    def totale_operatori(self):
        return float("{:0.2f}".format(self.quantita_operatori * (self.importo_operatore / 60 * self.minuti_intervento)))
    #totale_operatori.admin_order_field = 'name'
    #totale_operatori.short_description = 'Operatori'
    #totale_operatori.allow_tags = True


    @property
    def totale_iva_operatori(self):
        return float("{:0.2f}".format(self.totale_operatori / 100 * 22))
    #totale_iva_operatori.admin_order_field = 'name'
    #totale_iva_operatori.short_description = 'IVA Operatori'
    #totale_iva_operatori.allow_tags = True


    @property
    def totale_operatori_ivato(self):
        return float("{:0.2f}".format(self.totale_operatori + self.totale_iva_operatori))
    #totale_operatori_ivato.admin_order_field = 'name'
    #totale_operatori_ivato.short_description = 'Tot. Operatori'
    #totale_operatori_ivato.allow_tags = True


    @property
    def totale_intervento(self):
        return float("{:0.2f}".format(self.totale_materiale + self.totale_operatori))
    #totale_intervento.admin_order_field = 'name'
    #totale_intervento.short_description = 'Tot. Intervento'
    #totale_intervento.allow_tags = True


    @property
    def totale_iva(self):
        return float("{:0.2f}".format(self.totale_iva_materiale + self.totale_iva_operatori))
    #totale_iva.admin_order_field = 'name'
    #totale_iva.short_description = 'Tot. IVA'
    #totale_iva.allow_tags = True


    @property
    def totale_intervento_ivato(self):
        return float("{:0.2f}".format(self.totale_iva + self.totale_intervento))
    #totale_intervento_ivato.admin_order_field = 'name'
    #totale_intervento_ivato.short_description = 'Tot. Intervento'
    #totale_intervento_ivato.allow_tags = True

