@login_required
def export_interface_data(self):
    selected_project = request.form.get('selected_interface_type')
    chosen_project = Project.query.filter_by(name=str(selected_project), is_active=False).first()

    if chosen_project is None:
        logger.info(MessageEnum.project_not_found.value[1])
        flash(MessageEnum.project_not_found.value[1])
        return redirect(url_for('home.interface_management'))

    interface_records = Interface.query.filter_by(project_id=chosen_project.id, is_active=False).all()
    current_directory = os.getcwd()
    current_month = time.strftime("%Y%m", time.localtime(time.time()))
    uploads_directory = current_directory + '/app/upload'
    export_file_path = os.path.join(uploads_directory, (current_month + '.xls'))

    if not os.path.exists(export_file_path):
        os.system('touch %s' % export_file_path)

    export_result = create_export(file_path=export_file_path, interface_list=interface_records)

    if export_result['status_code'] == 1:
        flash(MessageEnum.export_error.value[1] + ' Reason: %s' % export_result['error_message'])
        return redirect(url_for('home.interface_management'))

    response = make_response(send_from_directory(directory=uploads_directory, filename=current_month + '.xls', as_attachment=True))
    return response