from openerp import models,fields,api


class JdrChar(models.Model):
    """ Class for Personage"""
    _name = "jdr.perso"
    _description = "Personage"

    name = fields.Char(string="Name")
    race_id = fields.Many2one(string="Race",comodel_name="jdr.race")
    old_race_id = fields.Many2one(string="Old Race", comodel_name="jdr.race")
    stat_ids = fields.One2many(comodel_name="jdr.value.stats", inverse_name="perso_id", string="Stats")

    fo = fields.Integer(string="FO")
    int = fields.Integer(string="INT")
    dex = fields.Integer(string="DEX")
    cha = fields.Integer(string="CHA")
    con = fields.Integer(string="CON")

    @api.onchange('stats')
    def _on_change_stats(self):
        self.fo = 0
        self.int = 0
        self.dex = 0
        self.cha = 0
        self.con = 0
        if self.stat_ids:
            for stat in self.stat_ids:
                if stat.carac_id:
                    if stat.carac_id.short_name.lower() == 'fo':
                        self.fo += stat.number
                    if stat.carac_id.short_name.lower() == 'int':
                        self.int += stat.number
                    if stat.carac_id.short_name.lower() == 'dex':
                        self.dex += stat.number
                    if stat.carac_id.short_name.lower() == 'cha':
                        self.cha += stat.number
                    if stat.carac_id.short_name.lower() == 'con':
                        self.con += stat.number

    @api.onchange('race_id')
    def _on_change_race(self):
        value_to_set = []
        removed_value = []
        jdr_value_stat = self.env['jdr.value.stats']
        if self.race_id:
            for race_stat in self.race_id.stats:
                value_to_set.append(copy_race.id)
        if self.old_race_id and self.old_race_id.stats:
            for perso_stat in self.stat_ids:
                for old_race_stat in self.old_race_id.stats:
                    if perso_stat.number == old_race_stat.number and perso_stat.carac_id == old_race_stat.carac_id and not removed_value:
                        removed_value.append(old_race_stat.id)
                    else:
                        value_to_set.append(perso_stat.id)
        else:
            for perso_stat in self.stat_ids:
                value_to_set.append(perso_stat.id)
        self.old_race_id = self.race_id
        self.stat_ids = value_to_set


class JdrRace(models.Model):
    """ Class for race"""
    _name = "jdr.race"
    _description = "Races"

    name = fields.Char(string="Name",required=True)
    image = fields.Binary("Photo", attachment=True)
    start_age = fields.Integer(string="Start age",required=True)
    life_expectancy = fields.Integer(string="Life expectancy",required=True)
    min_size = fields.Float(string="Minimum size",required=True)
    max_size = fields.Float(string="Maximum size",required=True)
    min_weight = fields.Integer(string="Minimum weight",required=True)
    max_weight = fields.Integer(string="Maximum weight",required=True)
    stats = fields.One2many(comodel_name="jdr.value.stats",inverse_name="race_id",string="Stats")


class JdrValueStats(models.Model):
    """ Class for personage and race stats 'Only use in O2M"""
    _name = "jdr.value.stats"
    _description = 'Global Stats'
    _rec_name = "carac_id"

    carac_id = fields.Many2one(string="Stats",comodel_name="jdr.stats")
    number = fields.Integer(string='Number')
    race_id = fields.Many2one(comodel_name="jdr.race", string="Race")
    perso_id = fields.Many2one(comodel_name="jdr.perso", string="Personage")


# class JdrPersoStats(models.Model):
#     _name = "jdr.perso.stats"
#     _description = 'Perso stats'
#     _inherit = 'jdr.value.stats'
#
#     perso_id = fields.Many2one(comodel_name="jdr.perso", string="Personage")
#
#
# class JdrPersoStats(models.Model):
#     _name = "jdr.race.stats"
#     _description = 'Race stats'
#     _inherit = 'jdr.value.stats'
#
#     race_id = fields.Many2one(comodel_name="jdr.race", string="Race")


class JdrStats(models.Model):
    """ Class for all stats"""
    _name = "jdr.stats"
    _description = 'Stats'
    _rec_name = "short_name"

    name = fields.Char(string="Name")
    short_name = fields.Char(string='Abbreviation')


class JdrChacteristic(models.Model):
    """ Class for all skills"""
    _name = "jdr.carac"
    _description = 'Characteristics'

    name = fields.Char(string="Name")
    description = fields.Text(string='Description')
