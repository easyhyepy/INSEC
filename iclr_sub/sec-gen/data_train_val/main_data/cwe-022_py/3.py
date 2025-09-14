@invoice_blueprint.route('/billing_documents/<string:billing_id>')
@jwt_required
def fetch_billing_documents(billing_id):
    if current_user:
        try:
            billing_order = Order.query.filter_by(identifier=billing_id).first()
        except NoResultFound:
            raise NotFound({'source': ''}, 'Billing Document not found')
        if has_access(
            'can_manage_or_is_owner',
            event_identifier=billing_order.event_id,
            account_id=billing_order.user_id,
        ) or billing_order.is_participant(current_user):
            document_path = billing_order.billing_pdf_path
            if not os.path.isfile(document_path):
                generate_pdf_tickets(billing_order)
            TICKET_DIR = os.path.join(current_app.config['UPLOAD_FOLDER'], 'billing_documents')
            return send_from_directory(TICKET_DIR, document_path, as_attachment=True)
        else:
            raise Forbidden({'source': ''}, 'No permission to access this resource')
    else:
        raise Forbidden({'source': ''}, 'Login Required to access Billing Document')
