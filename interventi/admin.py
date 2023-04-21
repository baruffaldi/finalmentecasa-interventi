from import_export import resources
from import_export.admin import ImportExportModelAdmin

from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group


from .models import Operatore, Fornitore, Cliente, Intervento


class MyAdminSite(AdminSite):
    site_header = 'Interventi - Finalmente Casa'
    site_title = 'Interventi - Finalmente Casa'
    app_index_title = 'Gestione Interventi - Finalmente Casa'
    index_title = 'Gestione Interventi - Finalmente Casa'

admin_site = MyAdminSite(name='finalmentecasadmin')


class FornitoreResource(resources.ModelResource):

    class Meta:
        model = Fornitore


class OperatoreResource(resources.ModelResource):

    class Meta:
        model = Operatore


class ClienteResource(resources.ModelResource):

    class Meta:
        model = Cliente


class InterventoResource(resources.ModelResource):

    class Meta:
        model = Intervento


class FornitoreAdmin(ImportExportModelAdmin):
    resource_classes = [FornitoreResource]


class OperatoreAdmin(ImportExportModelAdmin):
    resource_classes = [OperatoreResource]


class ClienteAdmin(ImportExportModelAdmin):
    resource_classes = [ClienteResource]


class InterventoAdmin(ImportExportModelAdmin):
    resource_classes = [InterventoResource]

    #
    # --- Listing settings
    #
    list_display = ('data_onlydate', 'cliente', 'descrizione', 'totale_intervento_euro', 'totale_iva_euro', 'totale_intervento_ivato_euro')
    sortable_by = ('data_onlydate', 'cliente', 'descrizione')
    list_display_links = ['descrizione']
    list_filter = ['operatore', 'cliente', 'data', 'fattura']
    #list_editable = ['machine']
    search_fields = ['operatore__fornitore__ragione_sociale', 'operatore__cognome', 'operatore__nome', 'cliente__denominazione', 'cliente__cognome', 'cliente__nome', 'descrizione']
    date_hierarchy = 'data'
    ordering = ['data']
    show_full_result_count = True


    #
    # --- Form settings
    #
    readonly_fields = (
        'totale_materiale_euro', 'totale_iva_materiale_euro', 'totale_materiale_ivato_euro', 
        'totale_operatori_euro', 'totale_iva_operatori_euro', 'totale_operatori_ivato_euro', 
        'totale_intervento_euro', 'totale_iva_euro', 'totale_intervento_ivato_euro', 
        'created_at', 'updated_at' 
    )
    
    fieldsets = [
        ('None',    {
            #'classes': ('collapse',),
            'fields': ['data', 'cliente', 'operatore', 'descrizione', 'minuti_intervento', 'fattura']}
        ),
        ('Operatore/i', {
            'classes': ('collapse',),
            'fields': ['quantita_operatori', 'importo_operatore']}
        ),
        ('Materiale', {
            'classes': ('collapse',),
            'fields': ['quantita_materiale', 'importo_materiale']}
        ),
        ('IVA', {
            'classes': ('collapse',),
            'fields': ['iva_operatore', 'iva_materiale', 'iva_chiamata']}
        ),
        ('Calcolati', {
            #'classes': ('collapse',),
            'fields': [
                'totale_materiale_euro', 'totale_iva_materiale_euro', 'totale_materiale_ivato_euro', 
                'totale_operatori_euro', 'totale_iva_operatori_euro', 'totale_operatori_ivato_euro', 
                'totale_intervento_euro', 'totale_iva_euro', 'totale_intervento_ivato_euro'
            ]}
        ),
        ('Database', {
            'classes': ('collapse',),
            'fields': [
                'created_at', 'updated_at'
            ]}
        ),
    ]

    
    def totale_materiale_euro(self, obj):
        return f'{obj.totale_materiale} €'
    totale_materiale_euro.short_description = 'Imponibile Materiale'

    def totale_iva_materiale_euro(self, obj):
        return f'{obj.totale_iva_materiale} €'
    totale_iva_materiale_euro.short_description = 'IVA Materiale'

    def totale_materiale_ivato_euro(self, obj):
        return f'{obj.totale_materiale_ivato} €'
    totale_materiale_ivato_euro.short_description = 'Totale Materiale'

    
    def totale_operatori_euro(self, obj):
        return f'{obj.totale_operatori} €'
    totale_operatori_euro.short_description = 'Imponibile Operatori'

    def totale_iva_operatori_euro(self, obj):
        return f'{obj.totale_iva_operatori} €'
    totale_iva_operatori_euro.short_description = 'IVA Operatori'

    def totale_operatori_ivato_euro(self, obj):
        return f'{obj.totale_operatori_ivato} €'
    totale_operatori_ivato_euro.short_description = 'Totale Operatori'

    
    def totale_intervento_euro(self, obj):
        return f'{obj.totale_intervento} €'
    totale_intervento_euro.short_description = 'Totale Intervento'

    def totale_iva_euro(self, obj):
        return f'{obj.totale_iva} €'
    totale_iva_euro.short_description = 'Totale IVA'

    def totale_intervento_ivato_euro(self, obj):
        return f'{obj.totale_intervento_ivato} €'
    totale_intervento_ivato_euro.short_description = 'Totale'


admin_site.register(User)
admin_site.register(Group)


admin_site.register(Fornitore, FornitoreAdmin)
admin_site.register(Operatore, OperatoreAdmin)
admin_site.register(Cliente, ClienteAdmin)
admin_site.register(Intervento, InterventoAdmin)