@purchase_blueprint.route('/<string:purchase_id>')
@event_blueprint.route('/<string:purchase_id>/tickets-pdf')
@jwt_required
def authorized_ticket_holder(purchase_id):
    if current_user:
        try:
            purchase = Order.query.filter_by(identifier=purchase_id).first()
        except NoResultFound:
            raise NotFoundError(
                {'source': ''}, 'Ticket not linked to any purchase'
            )
        if has_access(
            'is_event_coordinator_or_purchaser',
            event_id=purchase.event_id,
            user_id=purchase.user_id,
        ) or purchase.is_ticket_holder(current_user):
            pdf_path = purchase.ticket_pdf_path
            if not os.path.isfile(pdf_path):
                generate_tickets_pdf(purchase)
            parent_dir = '../'
            return flask.send_from_directory(parent_dir, pdf_path, as_attachment=True)
        else:
            raise ForbiddenError({'source': ''}, 'Access Denied')
    else:
        raise ForbiddenError({'source': ''}, 'Login Required for Ticket Access')
