from opentera.db.Base import db, BaseModel


class TeraServiceSite(db.Model, BaseModel):
    __tablename__ = 't_services_sites'
    id_service_site = db.Column(db.Integer, db.Sequence('id_service_site_sequence'), primary_key=True,
                                autoincrement=True)
    id_service = db.Column(db.Integer, db.ForeignKey('t_services.id_service', ondelete='cascade'), nullable=False)
    id_site = db.Column(db.Integer, db.ForeignKey('t_sites.id_site', ondelete='cascade'), nullable=False)

    service_site_service = db.relationship("TeraService")
    service_site_site = db.relationship("TeraSite")

    def __init__(self):
        pass

    def to_json(self, ignore_fields=None, minimal=False):
        if ignore_fields is None:
            ignore_fields = []

        ignore_fields.extend(['service_site_service', 'service_site_site'])

        if minimal:
            ignore_fields.extend([])

        return super().to_json(ignore_fields=ignore_fields)

    @staticmethod
    def get_services_for_site(id_site: int):
        return TeraServiceSite.query.filter_by(id_site=id_site).all()

    @staticmethod
    def get_sites_for_service(id_service: int):
        return TeraServiceSite.query.filter_by(id_service=id_service).all()

    @staticmethod
    def get_service_site_by_id(service_site_id: int):
        return TeraServiceSite.query.filter_by(id_service_site=service_site_id).first()

    @staticmethod
    def get_service_site_for_service_site(site_id: int, service_id: int):
        return TeraServiceSite.query.filter_by(id_site=site_id, id_service=service_id).first()

    @staticmethod
    def create_defaults(test=False):
        if test:
            from opentera.db.models.TeraService import TeraService
            from opentera.db.models.TeraSite import TeraSite

            site1 = TeraSite.get_site_by_sitename('Default Site')
            site2 = TeraSite.get_site_by_sitename('Top Secret Site')

            service_bureau = TeraService.get_service_by_key('BureauActif')

            service_site = TeraServiceSite()
            service_site.id_site = site1.id_site
            service_site.id_service = service_bureau.id_service
            db.session.add(service_site)

            service_site = TeraServiceSite()
            service_site.id_site = site2.id_site
            service_site.id_service = service_bureau.id_service
            db.session.add(service_site)

            db.session.commit()

    @staticmethod
    def delete_with_ids(service_id: int, site_id: int):
        delete_obj = TeraServiceSite.query.filter_by(id_service=service_id, id_site=site_id).first()
        if delete_obj:
            db.session.delete(delete_obj)
            db.session.commit()
